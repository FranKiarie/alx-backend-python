#!/usr/bin/env python3
"""
Unit tests for client module
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        test_payload = {"login": org_name, "id": 12345}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the expected value"""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock,
            return_value=test_payload
        ):
            client = GithubOrgClient("test")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list"""
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/test/repos"
        ) as mock_url:
            client = GithubOrgClient("test")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected boolean"""
        client = GithubOrgClient("test")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


try:
    from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
    FIXTURES = [{
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }]
except ImportError:
    # Fallback fixtures if fixtures.py doesn't exist
    FIXTURES = [{
        "org_payload": {"login": "test", "id": 12345},
        "repos_payload": [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ],
        "expected_repos": ["repo1", "repo2"],
        "apache2_repos": ["repo1"],
    }]


@parameterized_class(FIXTURES)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url):
            """Return appropriate payload based on URL"""
            mock_response = Mock()
            if "orgs" in url and "repos" not in url:
                mock_response.json.return_value = cls.org_payload
            elif "repos" in url:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos in integration"""
        client = GithubOrgClient("test")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)


if __name__ == '__main__':
    unittest.main()

