import unittest

from alg import *


class TestSearchAlgorithms(unittest.TestCase):

    def test_binary_element_in_middle(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 5
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, 4)
        self.assertTrue(comparisons > 0)

    def test_binary_element_at_start(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 1
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, 0)

    def test_binary_element_at_end(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 10
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, 9)

    def test_binary_element_not_found(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 11
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, -1)

    def test_binary_empty_array(self):
        arr = []
        target = 1
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, -1)

    def test_binary_single_element_found(self):
        arr = [5]
        target = 5
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, 0)

    def test_binary_single_element_not_found(self):
        arr = [5]
        target = 10
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, -1)

    def test_binary_large_array(self):
        arr = list(range(1, 100001))
        target = 50000
        position, comparisons = search_binary(arr, target)
        self.assertEqual(position, 49999)

    # Тесты для линейного поиска
    def test_linear_element_in_middle(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 5
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, 4)
        self.assertTrue(comparisons > 0)

    def test_linear_element_at_start(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 1
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, 0)

    def test_linear_element_at_end(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 10
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, 9)

    def test_linear_element_not_found(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        target = 11
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, -1)

    def test_linear_empty_array(self):
        arr = []
        target = 1
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, -1)

    def test_linear_single_element_found(self):
        arr = [5]
        target = 5
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, 0)

    def test_linear_single_element_not_found(self):
        arr = [5]
        target = 10
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, -1)

    def test_linear_large_array(self):
        arr = list(range(1, 100001))
        target = 50000
        position, comparisons = search_linear(arr, target)
        self.assertEqual(position, 49999)


if __name__ == "__main__":
    unittest.main()
