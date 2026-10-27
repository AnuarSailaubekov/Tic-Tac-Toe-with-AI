import g4f
import re  # Для поиска числа в тексте

def get_ai_move(board):
    prompt = f"""Вот текущее состояние поля (нумерация 0-8):
{board}
Ты играешь за 'O'. Напиши ТОЛЬКО номер клетки, в которую ты поставишь 'O' (без пояснений, текста и лишних слов)."""

    response = g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "Ты играешь в крестики-нолики. Отвечай только одним числом от 0 до 8."},
                  {"role": "user", "content": prompt}]
    )

    print("Ответ от g4f:", response)  # Отладка

    # Используем регулярку, чтобы извлечь только число
    match = re.search(r'\b[0-8]\b', response)  # Ищем число от 0 до 8
    if match:
        return int(match.group(0))
    else:
        print("Ошибка: ИИ дал неверный ответ:", response)
        return -1  # Если ответ странный, просто пропускаем ход



