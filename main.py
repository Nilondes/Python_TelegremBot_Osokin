from colorama import Fore, Style


def draw_board(board):
    try:
        # функция, определяющая цвет символа
        colorize = lambda x: Fore.RED + x + Style.RESET_ALL if x == 'X' else Fore.GREEN + x + Style.RESET_ALL if x == 'O' else x
        # запустить цикл, который проходит по всем 3 строкам доски
        for i in range(3):
            # поставить разделители значений в строке
            print(colorize(board[i][0]) + " | " + colorize(board[i][1]) + " | " + colorize(board[i][2]))
            # поставить разделители строк
            if i < 2:
                print("---------")
    except:
        print('An error occurred')


def ask_and_make_move(player, board):
    try:
        while True:
            coordinates = ask_move(player, board)
            if coordinates:
                break
        board = make_move(player, board, coordinates[0], coordinates[1])
        return board
    except:
        print('An error occurred')


def ask_move(player, board):
    try:
        player_x, player_y = input(f'Игрок {player}, Введите координаты x y: ').strip().split(' ')
        player_x, player_y = int(player_x), int(player_y)
        if player_x not in (0, 1, 2) or player_y not in (0, 1, 2):
            print('Значение координаты должно быть в диапазоне от 0 до 2')
            return False
        if board[player_y][player_x] != ' ':
            print('Ячейка занята, пожалуйста выберите другие координаты')
            return False
        return player_x, player_y
    except:
        print('An error occurred')


def make_move(player, board, x, y):
    try:
        board[y][x] = player
        return board
    except:
        print('An error occurred')


def check_win(player, board):
    """Check win conditions"""
    try:
        for row in board:
            if row == [player, player, player]:  # Ищем совпадение по строкам
                return True
        for j in range(3):
            if [board[0][j], board[1][j], board[2][j]] == [player, player, player]:  # Ищем совпадение по столбцам
                return True
        if [board[0][0], board[1][1], board[2][2]] == [player, player, player]:  # Ищем совпадение по главной диагонали
            return True
        if [board[0][2], board[1][1], board[2][0]] == [player, player, player]:  # Ищем совпадение по побочной диагонали
            return True
        return False
    except:
        print('An error occurred')


def check_draw(board):
    """Checks whether there is at least one empty spot"""
    try:
        for row in board:
            for cell in row:
                if cell == ' ':
                    return False
        return True
    except:
        print('An error occurred')


def tic_tac_toe():
    try:
        the_board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        draw_board(the_board)
        current_player = {1: 'X',
                          -1: 'O',
                          }
        player_key = -1
        while not check_win(current_player[player_key], the_board):
            player_key *= -1  # Switch player
            the_board = ask_and_make_move(current_player[player_key], the_board)
            draw_board(the_board)
            if check_draw(the_board):
                print('Ничья!')
                return None
        print(f'Игрок {current_player[player_key]} победил!')
    except:
        print('An error occurred')


while True:
    tic_tac_toe()
    answer = input('Чтобы сыграть ещё, напишите "Да"')
    if not answer.lower() == 'да':
        print('Good bye!')
        break
