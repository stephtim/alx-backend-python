#!/usr/bin/env python3
"""
test_utils.py

This module contains unit tests for the functions defined in utils.py.
It focuses on verifying the correct behavior of access_nested_map.
"""

import unittest
from unittest.mock import patch, Mock
from typing import Any, Mapping, Sequence
from parameterized import parameterized  #used for parameterized testing
import subprocess

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    TestAccessNestedMap contains test cases for the access_nested_map
    function to ensure it correctly retrieves values from nested maps.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        expected: Any
    ) -> None:
        """
        Test that access_nested_map returns the expected result
        when given valid nested mappings and paths.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: dict,
                               path: tuple,
                               expected: object) -> None:
        """Test access_nested_map returns the expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

   
    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: dict,
                                         path: tuple,
                                         expected_message: str) -> None:
        """Test access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), expected_message)


if __name__ == "__main__":
    unittest.main()


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

   
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: dict,
                               path: tuple,
                               expected: object) -> None:
        """Test access_nested_map returns the expected value."""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected,
            msg=f"\n- [Got]\n{access_nested_map(nested_map, path)}\n\n"
                f"[Expected]\n{expected}\n"
        )

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: dict,
                                         path: tuple,
                                         expected_message: str) -> None:
        """Test access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(
            str(cm.exception),
            expected_message,
            msg=f"\n- [Got]\n{str(cm.exception)}\n\n"
                f"[Expected]\n{expected_message}\n"
        )

class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self,
                      test_url: str,
                      test_payload: dict) -> None:
        """Test get_json returns expected result with mocked requests."""
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            self.assertEqual(
                result,
                test_payload,
                msg=f"\n- [Got]\n{result}\n\n"
                    f"[Expected]\n{test_payload}\n"
            )
            mock_get.assert_called_once_with(test_url)


if __name__ == "__main__":
    unittest.main()


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: dict,
                               path: tuple,
                               expected: object) -> None:
        """Test access_nested_map returns the expected value."""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected,
            msg=f"\n- [Got]\n{access_nested_map(nested_map, path)}\n\n"
                f"[Expected]\n{expected}\n"
        )

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: dict,
                                         path: tuple,
                                         expected_message: str) -> None:
        """Test access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(
            str(cm.exception),
            expected_message,
            msg=f"\n- [Got]\n{str(cm.exception)}\n\n"
                f"[Expected]\n{expected_message}\n"
        )

class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self,
                      test_url: str,
                      test_payload: dict) -> None:
        """Test get_json returns expected result with mocked requests."""
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            self.assertEqual(
                result,
                test_payload,
                msg=f"\n- [Got]\n{result}\n\n"
                    f"[Expected]\n{test_payload}\n"
            )
            mock_get.assert_called_once_with(test_url)


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: dict,
                               path: tuple,
                               expected: object) -> None:
        """Test access_nested_map returns the expected value."""
        self.assertEqual(
            access_nested_map(nested_map, path),
            expected,
            msg=f"\n- [Got]\n{access_nested_map(nested_map, path)}\n\n"
                f"[Expected]\n{expected}\n"
        )

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: dict,
                                         path: tuple,
                                         expected_message: str) -> None:
        """Test access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(
            str(cm.exception),
            expected_message,
            msg=f"\n- [Got]\n{str(cm.exception)}\n\n"
                f"[Expected]\n{expected_message}\n"
        )


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self,
                      test_url: str,
                      test_payload: dict) -> None:
        """Test get_json returns expected result with mocked requests."""
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            self.assertEqual(
                result,
                test_payload,
                msg=f"\n- [Got]\n{result}\n\n"
                    f"[Expected]\n{test_payload}\n"
            )
            mock_get.assert_called_once_with(test_url)

class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct return values from nested maps."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(str(e.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""


@parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])

@patch("utils.requests.get")
def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns expected payload with mocked requests."""
        mock_resp = Mock()
        mock_resp.json.return_value = test_payload
        mock_get.return_value = mock_resp

        result = get_json(test_url)
        self.assertEqual(result, test_payload)

        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches method results."""

        class TestClass:
            """Helper class for testing memoization."""

            def a_method(self) -> int:
                """Return a constant value for testing."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Return the result of a_method, cached after first call."""
                return self.a_method()

        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            obj = TestClass()
            self.assertEqual(obj.a_property, 42)
            self.assertEqual(obj.a_property, 42)
            mock_method.assert_called_once()


class TestCodeStyle(unittest.TestCase):
    """Tests to ensure code follows pycodestyle guidelines."""

    
    def test_pep8_conformance(self):
        """Test that all project files conform to PEP8 (pycodestyle)."""
        result = subprocess.run(
            ["pycodestyle", "--max-line-length=79",
             "utils.py", "test_utils.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
       
       
        self.assertEqual(
            result.returncode,
            0,
            msg=f"pycodestyle violations:\n{result.stdout}"
        )


if __name__ == "__main__":
    unittest.main()
