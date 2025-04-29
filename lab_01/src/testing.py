from alg import *

test_cases_lev = [
    # 1. Пустые строки
    ("", "", 0),
    ("abc", "", 3),
    ("", "abc", 3),

    # 2. Одинаковые строки
    ("abc", "abc", 0),  # Совпадающие строки

    # 3. Полностью разные строки
    ("abc", "xyz", 3),

    # 4. Одна строка — подстрока другой
    ("abc", "abcd", 1),
    ("abcd", "abc", 1),

    # 5. Строки с небольшими изменениями
    ("kitten", "sitting", 3),
    ("reka", "muka", 2),
    ("apple", "appel", 2)
]

test_cases_dam_lev = [
    # 1. Пустые строки
    ("", "", 0),
    ("abc", "", 3),
    ("", "abc", 3),

    # 2. Одинаковые строки
    ("abc", "abc", 0),  # Совпадающие строки

    # 3. Полностью разные строки
    ("abc", "xyz", 3),

    # 4. Одна строка — подстрока другой
    ("abc", "abcd", 1),
    ("abcd", "abc", 1),

    # 5. Строки с небольшими изменениями
    ("kitten", "sitting", 3),
    ("reka", "muka", 2),

    #6. Строки с перестановкой
    ("apple", "appel", 1)
]

lev_funcs = [levenshtein_recursive, levenshtein_recursive_memo, levenshtein]
dam_lev_funcs = [damerau_levenshtein]


def testing():
    for func in lev_funcs:
        print(f"Тестирование {func.__name__}")
        count_mist = 0

        for str1, str2, expected in test_cases_lev:
            result = func(str1, str2)
            if result != expected:
                print(f"Ошибка на тесте {str1} vs {str2}. Ожидалось: {expected}, получено: {result}")
                count_mist += 1

        if count_mist == 0:
            print("Все тесты пройдены успешно.")

        print()

    for func in dam_lev_funcs:
        print(f"Тестирование {func.__name__}")
        count_mist = 0

        for str1, str2, expected in test_cases_dam_lev:
            result = func(str1, str2)
            if result != expected:
                print(f"Ошибка на тесте {str1} vs {str2}. Ожидалось: {expected}, получено: {result}")
                count_mist += 1

        if count_mist == 0:
            print("Все тесты пройдены успешно.")

        print()

if __name__ == "__main__":
    testing()
