#!/usr/bin/env python3
from datetime import datetime, time
from django.http import HttpResponseForbidden
from datetime import datetime
from django.http import JsonResponse
from collections import defaultdict
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app between 6PM and 9PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict the messaging app URLs (adjust path prefix as needed)
        if request.path.startswith("/api/") or request.path.startswith("/conversations/"):

            # Get current server time
            now = datetime.now().time()

            # Define restricted hours: 18:00 (6 PM) to 21:00 (9 PM)
            start_time = time(18, 0, 0)  # 6 PM
            end_time = time(21, 0, 0)    # 9 PM

            # Deny access if current time is within restricted hours
            if start_time <= now <= end_time:
                return HttpResponseForbidden("Access to messaging is restricted between 6PM and 9PM.")

        # Proceed normally if outside restricted hours
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages a user can send
    from a single IP address within a time window (e.g., 5 messages per minute).
    """

    # Track messages per IP
    message_logs = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only count POST requests to messaging endpoints (adjust path as needed)
        if request.method == "POST" and request.path.startswith("/api/conversations/"):

            # Get the client IP
            ip_address = self.get_client_ip(request)

            # Current time
            now = datetime.now()

            # Remove entries older than 1 minute
            self.message_logs[ip_address] = [
                t for t in self.message_logs[ip_address]
                if t > now - timedelta(minutes=1)
            ]

            # Check if the limit (5 messages) is exceeded
            if len(self.message_logs[ip_address]) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded: Maximum 5 messages per minute."},
                    status=429
                )

            # Log current message timestamp
            self.message_logs[ip_address].append(now)

        # Proceed to process request
        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """Get the client IP address from request headers."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    class RolepermissionMiddleware:
    """
    Middleware to restrict access to users who are not 'admin' or 'moderator'.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip check for anonymous users
        if not request.user.is_authenticated:
            return HttpResponseForbidden("Access denied: User is not authenticated.")

        # Assume user has a 'role' attribute in the User model or profile
        # Adjust the attribute path if roles are stored differently
        user_role = getattr(request.user, "role", None)

        # Check if user role is allowed
        if user_role not in ["admin", "moderator"]:
            return HttpResponseForbidden("Access denied: User does not have the required role.")

        # Proceed to the next middleware/view
        response = self.get_response(request)
        return response