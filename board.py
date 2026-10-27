def check_winner(board):
    # Шаблоны победных комбинаций
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Горизонтали
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Вертикали
        [0, 4, 8], [2, 4, 6]  # Диагонали
    ]
    
    # Проверка победных комбинаций
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] and board[pattern[0]] != " ":
            return board[pattern[0]]
    
    # Если победителя нет
    return None

def get_available_moves(board):
    # Возвращаем список всех доступных клеток
    return [i for i, cell in enumerate(board) if cell == " "]



