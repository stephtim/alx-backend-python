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

