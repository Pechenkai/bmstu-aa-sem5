import unittest
from alg import standard_multiply, winograd_multiply, optimized_winograd_multiply


class TestMatrixMultiplication(unittest.TestCase):

    def test_small_matrices(self):
        # Тест для маленьких матриц 2x2
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        expected_result = [[19, 22], [43, 50]]

        self.assertEqual(standard_multiply(A, B), expected_result)
        self.assertEqual(winograd_multiply(A, B), expected_result)
        self.assertEqual(optimized_winograd_multiply(A, B), expected_result)

    def test_rectangular_matrices(self):
        # Тест для прямоугольных матриц 2x3 и 3x2
        A = [[1, 2, 3], [4, 5, 6]]
        B = [[7, 8], [9, 10], [11, 12]]
        expected_result = [[58, 64], [139, 154]]

        self.assertEqual(standard_multiply(A, B), expected_result)
        self.assertEqual(winograd_multiply(A, B), expected_result)
        self.assertEqual(optimized_winograd_multiply(A, B), expected_result)

    def test_single_row_and_column(self):
        # Тест для случая с одной строкой и одним столбцом
        A = [[1, 2, 3]]
        B = [[4], [5], [6]]
        expected_result = [[32]]

        self.assertEqual(standard_multiply(A, B), expected_result)
        self.assertEqual(winograd_multiply(A, B), expected_result)
        self.assertEqual(optimized_winograd_multiply(A, B), expected_result)

    def test_large_matrices(self):
        # Тест для матриц 3x3
        A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        B = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        expected_result = [[30, 24, 18], [84, 69, 54], [138, 114, 90]]

        self.assertEqual(standard_multiply(A, B), expected_result)
        self.assertEqual(winograd_multiply(A, B), expected_result)
        self.assertEqual(optimized_winograd_multiply(A, B), expected_result)

    def test_identity_matrix(self):
        # Тест для случая с единичной матрицей
        A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        B = [[5, 6, 7], [8, 9, 10], [11, 12, 13]]
        expected_result = [[5, 6, 7], [8, 9, 10], [11, 12, 13]]

        self.assertEqual(standard_multiply(A, B), expected_result)
        self.assertEqual(winograd_multiply(A, B), expected_result)
        self.assertEqual(optimized_winograd_multiply(A, B), expected_result)

    def test_empty_matrices(self):
        # Тест для случая с пустыми матрицами
        A = []
        B = []
        expected_result = []

        self.assertIsNone(standard_multiply(A, B), expected_result)
        self.assertIsNone(winograd_multiply(A, B), expected_result)
        self.assertIsNone(optimized_winograd_multiply(A, B), expected_result)

    def test_incompatible_matrices(self):
        # Тест для случая с несовместимыми матрицами
        A = [[1, 2], [3, 4]]
        B = [[5, 6, 7]]

        self.assertIsNone(standard_multiply(A, B))
        self.assertIsNone(winograd_multiply(A, B))
        self.assertIsNone(optimized_winograd_multiply(A, B))


if __name__ == '__main__':
    unittest.main()