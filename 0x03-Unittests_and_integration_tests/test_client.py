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

    #!/usr/bin/env python3
"""
This module contains unit tests for the GithubOrgClient class,
covering the _public_repos_url property and the has_license method.
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    This class defines test cases for the GithubOrgClient class.
    """

    def test_public_repos_url(self) -> None:
        """
        Test that GithubOrgClient._public_repos_url returns the
        expected URL based on the mocked organization payload.
        """
        test_payload: Dict[str, Any] = {
            "repos_url": "https://api.github.com/orgs/testorg/repos"
        }

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=unittest.mock.PropertyMock,
            return_value=test_payload
        ):
            client: GithubOrgClient = GithubOrgClient("testorg")
            result: str = client._public_repos_url
            expected: str = "https://api.github.com/orgs/testorg/repos"
            self.assertEqual(result, expected)

    def test_has_license(self) -> None:
        """
        Test that GithubOrgClient.has_license correctly determines
        if a repository has a given license key.
        """
        test_cases = [
            ({"license": {"key": "mit"}}, "mit", True),
            ({"license": {"key": "apache-2.0"}}, "mit", False),
            ({"license": {"key": "gpl-3.0"}}, "gpl-3.0", True),
            ({}, "mit", False),
            ({"license": None}, "mit", False),
        ]

        for repo, license_key, expected in test_cases:
            with self.subTest(repo=repo, license=license_key):
                result: bool = GithubOrgClient.has_license(repo, license_key)
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()


"""
This module contains integration tests for the GithubOrgClient class.
It verifies behavior when interacting with external APIs by mocking
the requests.get method with fixture data.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from typing import Any, Dict, List
import requests

from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    This class defines integration tests for GithubOrgClient.
    It uses fixtures and mocks requests.get to simulate API calls.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up the test environment by patching requests.get and
        configuring side effects to return fixture data.
        """
        cls.get_patcher = patch("requests.get")

        def side_effect(url: str, *args: Any, **kwargs: Any) -> Mock:
            """
            Side effect function for mocking requests.get based on URL.
            Returns a mock response object with fixture data.
            """
            mock_resp: Mock = Mock()
            if url.endswith("/orgs/testorg"):
                mock_resp.json.return_value = cls.org_payload
            elif url.endswith("/orgs/testorg/repos"):
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down the test environment by stopping the requests.get patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Test that GithubOrgClient.public_repos returns the expected
        list of repository names using fixture data.
        """
        client: GithubOrgClient = GithubOrgClient("testorg")
        result: List[str] = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """
        Test that GithubOrgClient.public_repos with a license filter
        returns only repositories that match the given license.
        """
        client: GithubOrgClient = GithubOrgClient("testorg")
        result: List[str] = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()




