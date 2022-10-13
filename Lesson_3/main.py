# Реализация решения через цикл For


def sort_grades(data, estimates):
    data_sorted = []
    estimates.sort(reverse=True)
    data.sort(reverse=True)


    for estimate in estimates:

        for value in data:
            if value.upper() == estimate.upper():
                data_sorted = data_sorted + list(value.upper())

    return data_sorted

# grades = []
# grades_sorted = []

if __name__ == '__main__':
    estimates = ['A', 'B', 'C', 'D', 'F']

    grades = ['A', 'B', 'C', 'C', 'F', 'A']
    print(sort_grades(grades, estimates))  # -> ['F', 'C', 'C', 'B', 'A' , 'A']
    grades = ['b', 'c', 'C', 'f', 'A']
    print(sort_grades(grades, estimates))  # -> ['F', 'C', 'C', 'B', 'A']
    grades = []
    print(sort_grades(grades, estimates))  # -> []

    print('''выше показано рещение на исходных данных в задаче.
    Ниже вы можете ввести систему оценок и результаты для обработки
    ''')
    in_estimates = input('Введите систему ойенок: ')
    estimates = list(in_estimates)
    in_grades = input('Введите  беспорядочные данные: ')
    grades = list(in_grades)
    print(sort_grades(grades, estimates))  # -> []
