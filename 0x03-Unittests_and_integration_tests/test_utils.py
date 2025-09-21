#!/usr/bin/env python3
"""
test_utils.py

This module contains unit tests for the functions defined in utils.py.
It focuses on verifying the correct behavior of access_nested_map.
"""

import unittest
from typing import Any, Mapping, Sequence
from parameterized import parameterized
from utils import access_nested_map


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




#!/usr/bin/env python3
"""Unit tests for utils.py module.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json


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

#!/usr/bin/env python3
"""Unit tests for utils.py module.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


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


#!/usr/bin/env python3
"""Unit tests for utils.py module.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


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


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches result and calls underlying method once."""

        class TestClass:
            """Dummy class for testing memoize."""

            def a_method(self) -> int:
                """Return integer 42."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Return cached result of a_method via memoize."""
                return self.a_method()

        with patch.object(TestClass, "a_method",
                          return_value=42) as mock_method:
            obj = TestClass()

            # First call executes a_method
            result1 = obj.a_property
            # Second call should use cache
            result2 = obj.a_property

            self.assertEqual(
                result1,
                42,
                msg=f"\n- [Got]\n{result1}\n\n[Expected]\n42\n"
            )
            self.assertEqual(
                result2,
                42,
                msg=f"\n- [Got]\n{result2}\n\n[Expected]\n42\n"
            )
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
