import tkinter as tk
from tkinter import messagebox
from board import check_winner
from ai import get_ai_move

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.geometry("400x500")
        self.root.configure(bg="#2e3b4e")
        
        self.board = [" " for _ in range(9)]  # 3x3 поле
        self.player = None  # Игрок еще не выбрал символ
        self.current_player = None  # Текущий игрок, которого нужно отобразить на экране

        self.buttons = []
        self.create_widgets()

        # Инициализация переменных для анимации точек
        self.ai_dots = 0
        self.ai_animating = False

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Крестики-нолики", font=("Arial", 24, "bold"), bg="#2e3b4e", fg="#ffffff")
        title_label.pack(pady=20)

        # Создаем кнопку для выбора крестика или нолика
        choose_label = tk.Label(self.root, text="Выберите, кем будете играть:", font=("Arial", 14), bg="#2e3b4e", fg="#ffffff")
        choose_label.pack(pady=10)

        # Кнопки для выбора X или O
        choose_x_button = tk.Button(self.root, text="Крестик (X)", width=20, height=2, font=("Arial", 14), 
                                    bg="#ff6347", fg="#ffffff", relief="raised", command=lambda: self.set_player("X"))
        choose_o_button = tk.Button(self.root, text="Нолик (O)", width=20, height=2, font=("Arial", 14), 
                                    bg="#4682b4", fg="#ffffff", relief="raised", command=lambda: self.set_player("O"))
        choose_x_button.pack(pady=10)
        choose_o_button.pack(pady=10)

    def set_player(self, symbol):
        """Устанавливаем символ игрока и начинаем игру."""
        self.player = symbol
        # Если игрок выбрал "O", то ИИ начинает первым
        self.current_player = "O" if self.player == "O" else "X"
        self.create_game_screen()

    def create_game_screen(self):
        """Создаем экран игры после выбора символа."""
        # Удаляем кнопки выбора X и O
        for widget in self.root.winfo_children():
            widget.destroy()

        # Заголовок
        title_label = tk.Label(self.root, text="Крестики-нолики", font=("Arial", 24, "bold"), bg="#2e3b4e", fg="#ffffff")
        title_label.pack(pady=20)

        # Создаем 9 кнопок для игрового поля
        self.board_frame = tk.Frame(self.root, bg="#2e3b4e")
        self.board_frame.pack()

        for i in range(9):
            button = tk.Button(self.board_frame, text=" ", width=10, height=3, font=("Arial", 24), 
                               bg="#f0f0f0", fg="#333333", relief="raised", command=lambda i=i: self.make_move(i))
            button.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(button)

        # Кнопка "Начать заново"
        restart_button = tk.Button(self.root, text="Начать заново", width=20, height=2, font=("Arial", 14), 
                                   bg="#ff6347", fg="#ffffff", relief="raised", command=self.reset_game)
        restart_button.pack(pady=20)

        # Статус
        self.status_label = tk.Label(self.root, text=f"Ход игрока: {self.current_player}", font=("Arial", 14), bg="#2e3b4e", fg="#ffffff")
        self.status_label.pack(pady=10)

        # Метка для ИИ
        self.ai_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#2e3b4e", fg="#ffffff")
        self.ai_label.pack(pady=10)

        # Если игрок выбрал "O", ИИ должен начать первым
        if self.player == "O":
            self.ai_move()  # ИИ начинает, если игрок выбрал O

    def make_move(self, index):
        if self.board[index] == " " and self.current_player == "X":  # Игрок X делает ход только если клетка пуста
            self.board[index] = "X"
            self.buttons[index].config(text="X", state="disabled", fg="#ff6347")  # Обновляем кнопку
            self.check_winner_and_switch_player()

    def ai_move(self):
        # Начинаем анимацию точек
        self.ai_dots = 0
        self.update_ai_animation()

        # Информируем пользователя, что ИИ думает
        self.ai_label.config(text="ИИ думает.")
        self.root.update()  # Обновляем интерфейс

        # ИИ делает ход
        move = get_ai_move(self.board)
        if move != -1 and self.board[move] == " ":  # Проверяем, что клетка пуста
            self.board[move] = "O"
            self.buttons[move].config(text="O", state="disabled", fg="#4682b4")  # Обновляем кнопку ИИ
            self.check_winner_and_switch_player()

        # После хода ИИ убираем текст "ИИ думает..."
        self.ai_label.config(text="")

    def update_ai_animation(self):
        if self.ai_dots < 3:
            self.ai_dots += 1
        else:
            self.ai_dots = 1  # Сбросить до одной точки

        # Обновляем текст метки
        self.ai_label.config(text=f"ИИ думает{'.' * self.ai_dots}")
        if self.ai_dots < 3:  # Обновляем только если нужно продолжать анимацию
            self.root.after(500, self.update_ai_animation)  # Обновляем каждую 500 миллисекунд

    def check_winner_and_switch_player(self):
        winner = check_winner(self.board)  # Проверяем победителя
        if winner:
            self.display_winner(winner)  # Если есть победитель, показываем результат
        elif " " not in self.board:  # Если нет пустых клеток, значит ничья
            self.display_draw()
        else:
            # Меняем игрока
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text=f"Ход игрока: {self.current_player}")
            if self.current_player == "O":
                self.ai_move()  # Ход ИИ

    def display_winner(self, winner):
        messagebox.showinfo("Конец игры", f"Победитель: {winner}", icon="info")
        self.reset_game()

    def display_draw(self):
        messagebox.showinfo("Конец игры", "Ничья!", icon="info")
        self.reset_game()

    def reset_game(self):
        # Сбрасываем поле
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", state="normal", fg="#333333")  # Сбрасываем текст на кнопках
        # Устанавливаем игрока X первым
        self.current_player = "X"
        self.status_label.config(text=f"Ход игрока: {self.current_player}")
        self.ai_label.config(text="")  # Сбросим текст "ИИ думает..." при сбросе игры

def main():
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
