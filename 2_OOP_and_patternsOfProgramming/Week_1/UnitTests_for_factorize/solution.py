"""
A function is given:
def factorize(x):
    Factorize positive integer and return its factors.
    :type x: int,>=0
    :rtype: tuple[N],N>0
    pass

Write following unittests for it:

1) test_wrong_types_raise_exception - tests that float and string as input does
invoke TypeError. Test data:  'string',  1.5
2) test_negative - tests that negative values as input causes ValueError.
Test data: -1,  -10,  -100
3) test_zero_and_one_cases - tests that if 0 and 1 is given as input, tuples
(0, ) and (1, ) will be returned
4) test_simple_numbers - tests that for simple numbers tuples with the same
number returned
Test data: 3 → (3, ),  13 → (13, ),   29 → (29, )
test_two_simple_multipliers — проверяет случаи, когда передаются числа для которых функция factorize возвращает кортеж с числом элементов равным 2.
Набор тестовых данных: 6 → (2, 3),   26 → (2, 13),   121 --> (11, 11)
test_many_multipliers - проверяет случаи, когда передаются числа для которых функция factorize возвращает кортеж с числом элементов больше 2.
Hабор тестовых данных: 1001 → (7, 11, 13)
9699690 → (2, 3, 5, 7, 11, 13, 17, 19)

"""


class TestFactorize(unittest.TestCase):
    def test_wrong_types_raise_exception(self):
        cases = ('string', 1.5)
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(TypeError, factorize, x)

    def test_negative(self):
        cases = (-1, -10, -100)
        for x in cases:
            with self.subTest(case=x):
                self.assertRaises(ValueError, factorize, x)

    def test_zero_and_one_cases(self):
        cases = (0, 1)
        for x in cases:
            with self.subTest(case=x):
                fact_of_case = factorize(x)
                self.assertEqual(type(fact_of_case), type((x,)))
                self.assertEqual(len(fact_of_case), len((x,)))
                self.assertCountEqual(fact_of_case, (x,))

    def test_simple_numbers(self):
        cases = (3, 13, 29)
        for x in cases:
            with self.subTest(case=x):
                fact_of_case = factorize(x)
                self.assertEqual(type(fact_of_case), type((x,)))
                self.assertEqual(len(fact_of_case), len((x,)))
                self.assertCountEqual(fact_of_case, (x,))

    def test_two_simple_multipliers(self):
        test_map = {
            '6 → (2, 3)': [6, (2, 3)],
            '26 → (2, 13)': [26, (2, 13)],
            '121 → (11, 11)': [121, (11, 11)],
        }
        for name, (x, result) in test_map.items():
            with self.subTest(name=name):
                self.assertEqual(factorize(x), result)

    def test_many_multipliers(self):
        test_map = {
            '1001 → (7, 11, 13)': [1001, (7, 11, 13)],
            '9699690 → (2, 3, 5, 7, 11, 13, 17, 19)': [9699690, (2, 3, 5, 7, 11, 13, 17, 19)],
        }
        for name, (x, result) in test_map.items():
            with self.subTest(name=name):
                self.assertEqual(factorize(x), result)