
def find_color_chess_cage(line_vertical, line_horizontal):
    color_cage = ('wight', 'black')
    if ord(line_vertical[-1]) % 2 == 0:
        if int(line_horizontal) % 2 == 0:
            return color_cage[0]
        return color_cage[1]
    else:
        if int(line_horizontal) % 2 == 0:
            return color_cage[1]
        return color_cage[0]




print('''
Привет, Друзья!
Данная задача возвращает вам цвет клетки на шахматной доске по выбранными Вами координатам.
Линии по горизонтале  - a, b, c, d ...
Линии по вертикали - 1, 2, 3, 4 ...
Клетка с координатами а1 имеет цвет- white
''')
line_vertical = input('введите буквенное значение линии по горизонтале:')
line_horizontal = input('введите цифровое значение линии по вертикале:')

print(f'Ваша клетка на шахматной доске имеет цвет - {find_color_chess_cage(line_vertical, line_horizontal)}')