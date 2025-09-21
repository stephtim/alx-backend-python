#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
Covers the org method with mocked get_json calls.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized  # used for parameterized testing


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # Patch as the innermost decorator
    def test_org(
        self,
        org_name: str,
        mock_get_json: Mock  # patch mock comes last in parameters
    ) -> None:
        """
        Test that GithubOrgClient.org returns correct value and calls get_json once
        with the expected URL, without making an actual HTTP request.
        """
        # Deferred import to avoid circular import
        from client import GithubOrgClient

        github_client = GithubOrgClient(org_name)
        mock_response_payload = {"login": org_name}
        mock_get_json.return_value = mock_response_payload

        result = github_client.org()

        self.assertEqual(result, mock_response_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == "__main__":
    unittest.main()



