"""
Скрипт для загрузки большого словаря русских слов

Использование:
    python download_dictionary.py

Скрипт:
1. Скачивает словарь с GitHub (danakt/russian-words)
2. Очищает от дубликатов
3. Сохраняет в data/russian_words.txt
"""

import requests
import os
from typing import Set

def download_russian_words():
    """Скачать словарь русских слов с GitHub"""
    
    print("Загружаем словарь русских слов...")
    
    # URL словаря (примерно 2.5 млн слов)
    url = "https://raw.githubusercontent.com/danakt/russian-words/master/russian.txt"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Декодируем содержимое
        content = response.content.decode('windows-1251')
        
        # Разбиваем на слова
        words = content.strip().split('\n')
        
        print(f"Скачано {len(words)} слов")
        
        return words
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке: {e}")
        return []

def clean_words(words: list) -> Set[str]:
    """Очистить список слов от дубликатов и невалидных значений"""
    
    print("Очищаем словарь...")
    
    cleaned = set()
    
    for word in words:
        word = word.strip().lower()
        
        # Пропускаем пустые строки
        if not word:
            continue
        
        # Пропускаем слова с цифрами или латиницей
        if any(char.isdigit() or char.isascii() and char.isalpha() for char in word):
            continue
        
        # Пропускаем слишком короткие или длинные слова
        if len(word) < 2 or len(word) > 30:
            continue
        
        cleaned.add(word)
    
    print(f"После очистки осталось {len(cleaned)} уникальных слов")
    
    return cleaned

def save_words(words: Set[str], filepath: str = 'data/russian_words.txt'):
    """Сохранить слова в файл"""
    
    print(f"Сохраняем в {filepath}...")
    
    # Создаём папку data если её нет
    os.makedirs('data', exist_ok=True)
    
    # Сортируем для удобства
    sorted_words = sorted(words)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(word + '\n')
    
    print(f"Успешно сохранено {len(sorted_words)} слов!")

def download_alternative_dictionary():
    """
    Альтернативный метод: скачать меньший, но качественный словарь
    Используется если основной недоступен
    """
    
    print("Используем альтернативный источник...")
    
    # Частотный словарь (топ-10000 самых используемых слов)
    url = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/ru/ru_50k.txt"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        words = []
        for line in response.text.strip().split('\n'):
            # Формат: "слово частота"
            parts = line.split()
            if parts:
                words.append(parts[0])
        
        print(f"Скачано {len(words)} частотных слов")
        return words
        
    except Exception as e:
        print(f"Ошибка: {e}")
        return []

def main():
    """Основная функция"""
    
    print("=" * 50)
    print("Загрузка словаря русских слов")
    print("=" * 50)
    print()
    
    # Пробуем основной источник
    words = download_russian_words()
    
    # Если не получилось - пробуем альтернативный
    if not words:
        print("\nПробуем альтернативный источник...")
        words = download_alternative_dictionary()
    
    if not words:
        print("\n❌ Не удалось загрузить словарь.")
        print("Попробуйте:")
        print("1. Проверить интернет-соединение")
        print("2. Скачать вручную с https://github.com/danakt/russian-words")
        print("3. Поместить файл в папку data/russian_words.txt")
        return
    
    # Очищаем
    cleaned_words = clean_words(words)
    
    # Сохраняем
    save_words(cleaned_words)
    
    print("\n" + "=" * 50)
    print("✅ Готово! Словарь загружен и готов к использованию")
    print("=" * 50)
    print(f"\nТеперь запустите backend:")
    print("  cd backend")
    print("  python app.py")

if __name__ == "__main__":
    main()