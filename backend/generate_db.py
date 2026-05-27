# -*- coding: utf-8 -*-
"""
Запусти этот скрипт один раз локально, чтобы сгенерировать
компактную базу слов для деплоя.

Результат: data/word_metadata.json (~10 МБ, ~150К слов)
Этот файл можно закоммитить в git.
"""
import json
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(BASE_DIR, 'data', 'russian_words.txt')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'word_metadata.json')

VOWELS = 'аеёиоуыэюя'
MAX_WORDS = 150_000


def count_syllables(word):
    return max(sum(1 for c in word if c in VOWELS), 1)


def detect_pos(word):
    pronouns = {
        'я','ты','он','она','оно','мы','вы','они','меня','тебя','его','её',
        'нас','вас','их','мне','тебе','ему','ей','нам','вам','им','мной',
        'тобой','ней','нами','вами','ими','себя','себе','собой','кто','что',
        'кого','чего','кому','чему','кем','чем','этот','эта','это','эти',
        'свой','своя','своё','свои','никто','ничто','некто','нечто',
    }
    if word in pronouns:
        return 'местоимение'
    if word.endswith(('ться', 'тся')):
        return 'глагол'
    if word.endswith(('ывать', 'ивать', 'овать', 'евать', 'нуть', 'вать')):
        return 'глагол'
    if word.endswith(('ать', 'ять', 'ить', 'еть', 'оть', 'уть')):
        return 'глагол'
    if word.endswith(('сти', 'зти', 'чь', 'ти')) and len(word) > 3:
        return 'глагол'
    if word.endswith(('аешь', 'яешь', 'уешь', 'ёшь', 'ишь', 'ешь')):
        return 'глагол'
    if word.endswith(('ает', 'яет', 'ует', 'ёт', 'ит')) and len(word) > 3:
        return 'глагол'
    if word.endswith(('ают', 'яют', 'уют', 'ят', 'ут')) and len(word) > 3:
        return 'глагол'
    if word.endswith(('ый', 'ий', 'ой')):
        return 'прилагательное'
    if word.endswith(('ая', 'яя', 'ое', 'ее')):
        return 'прилагательное'
    if word.endswith(('ого', 'его', 'ому', 'ему')):
        return 'прилагательное'
    if word.endswith(('ым', 'им', 'ых', 'их', 'ыми', 'ими')) and len(word) > 4:
        return 'прилагательное'
    if word.endswith(('ски', 'цки', 'чески', 'чно', 'жно', 'дно')) and len(word) > 4:
        return 'наречие'
    if word.endswith(('ально', 'ельно', 'льно')) and len(word) > 6:
        return 'наречие'
    if word.endswith('иво') and len(word) > 5:
        return 'наречие'
    if re.search(r'[бвгджзклмнпрстфхцчшщ]ро$', word) and len(word) > 4:
        return 'наречие'
    return 'существительное'


def detect_freq(syllables):
    if syllables == 1:
        return 'high'
    if syllables == 2:
        return 'medium'
    return 'low'


def is_valid(word):
    """Только чистые кириллические слова длиной 3–15 букв"""
    return bool(re.match(r'^[а-яё]{3,15}$', word))


def get_base_database():
    """Вручную составленные слова с гарантированно правильными метаданными"""
    return {
        'любовь':    {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'кровь':     {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'морковь':   {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
        'бровь':     {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'вновь':     {'pos': 'наречие',          'freq': 'high',   'syllables': 1},
        'готовь':    {'pos': 'глагол',           'freq': 'medium', 'syllables': 2},
        'обновь':    {'pos': 'глагол',           'freq': 'low',    'syllables': 2},
        'день':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'тень':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'лень':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'сирень':    {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
        'олень':     {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
        'осень':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'слово':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'снова':     {'pos': 'наречие',          'freq': 'high',   'syllables': 2},
        'основа':    {'pos': 'существительное', 'freq': 'high',   'syllables': 3},
        'мечта':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'красота':   {'pos': 'существительное', 'freq': 'high',   'syllables': 3},
        'пустота':   {'pos': 'существительное', 'freq': 'high',   'syllables': 3},
        'душа':      {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'хороша':    {'pos': 'прилагательное',  'freq': 'high',   'syllables': 3},
        'свет':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'ответ':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'рассвет':   {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'поэт':      {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'весна':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'война':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'страна':    {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'она':       {'pos': 'местоимение',      'freq': 'high',   'syllables': 2},
        'тишина':    {'pos': 'существительное', 'freq': 'high',   'syllables': 3},
        'волна':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'луна':      {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'ночь':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'дочь':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'мочь':      {'pos': 'глагол',           'freq': 'high',   'syllables': 1},
        'помочь':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'время':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'пламя':     {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
        'рука':      {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'река':      {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'тоска':     {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
        'судьба':    {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'дом':       {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'сон':       {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'гром':      {'pos': 'существительное', 'freq': 'medium', 'syllables': 1},
        'путь':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'грудь':     {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'суть':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'жить':      {'pos': 'глагол',           'freq': 'high',   'syllables': 1},
        'быть':      {'pos': 'глагол',           'freq': 'high',   'syllables': 1},
        'любить':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'забыть':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'открыть':   {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'знать':     {'pos': 'глагол',           'freq': 'high',   'syllables': 1},
        'ждать':     {'pos': 'глагол',           'freq': 'high',   'syllables': 1},
        'мечтать':   {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'молчать':   {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'летать':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'искать':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'стоять':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'бежать':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'петь':      {'pos': 'глагол',           'freq': 'high',   'syllables': 1},
        'гореть':    {'pos': 'глагол',           'freq': 'medium', 'syllables': 2},
        'смотреть':  {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'лететь':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'идти':      {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'уйти':      {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'найти':     {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'понять':    {'pos': 'глагол',           'freq': 'high',   'syllables': 2},
        'родной':    {'pos': 'прилагательное',  'freq': 'high',   'syllables': 2},
        'живой':     {'pos': 'прилагательное',  'freq': 'high',   'syllables': 2},
        'простой':   {'pos': 'прилагательное',  'freq': 'high',   'syllables': 2},
        'другой':    {'pos': 'прилагательное',  'freq': 'high',   'syllables': 2},
        'золотой':   {'pos': 'прилагательное',  'freq': 'high',   'syllables': 3},
        'молодой':   {'pos': 'прилагательное',  'freq': 'high',   'syllables': 3},
        'белый':     {'pos': 'прилагательное',  'freq': 'high',   'syllables': 2},
        'синий':     {'pos': 'прилагательное',  'freq': 'high',   'syllables': 2},
        'добрый':    {'pos': 'прилагательное',  'freq': 'high',   'syllables': 2},
        'вечный':    {'pos': 'прилагательное',  'freq': 'medium', 'syllables': 2},
        'жизнь':     {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'мир':       {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'боль':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'грусть':    {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'радость':   {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'печаль':    {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'надежда':   {'pos': 'существительное', 'freq': 'high',   'syllables': 3},
        'счастье':   {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'сердце':    {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'память':    {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'голос':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'слеза':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'мысль':     {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'звезда':    {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'земля':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'небо':      {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'море':      {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'лес':       {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'дождь':     {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'снег':      {'pos': 'существительное', 'freq': 'high',   'syllables': 1},
        'огонь':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'ветер':     {'pos': 'существительное', 'freq': 'high',   'syllables': 2},
        'всегда':    {'pos': 'наречие',          'freq': 'high',   'syllables': 2},
        'никогда':   {'pos': 'наречие',          'freq': 'high',   'syllables': 3},
        'давно':     {'pos': 'наречие',          'freq': 'high',   'syllables': 2},
        'тихо':      {'pos': 'наречие',          'freq': 'high',   'syllables': 2},
        'легко':     {'pos': 'наречие',          'freq': 'high',   'syllables': 2},
        'далеко':    {'pos': 'наречие',          'freq': 'high',   'syllables': 3},
    }


def main():
    if not os.path.exists(WORDS_FILE):
        print(f'Файл {WORDS_FILE} не найден.')
        print('Убедись, что russian_words.txt лежит в папке backend/data/')
        return

    print('Читаем russian_words.txt...')
    base = get_base_database()
    filtered = {}
    skipped = 0

    with open(WORDS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if len(filtered) >= MAX_WORDS:
                break
            word = line.strip().lower()
            if not is_valid(word) or word in base:
                skipped += 1
                continue
            s = count_syllables(word)
            filtered[word] = {
                'pos':       detect_pos(word),
                'freq':      detect_freq(s),
                'syllables': s,
            }

    # Base database имеет приоритет
    database = {**filtered, **base}

    print(f'Слов из файла: {len(filtered):,}')
    print(f'Пропущено: {skipped:,}')
    print(f'Итого в базе: {len(database):,}')

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False)  # без отступов = компактно

    size_mb = os.path.getsize(OUTPUT_FILE) / 1024 / 1024
    print(f'Файл сохранён: {OUTPUT_FILE}')
    print(f'Размер: {size_mb:.1f} МБ')
    print()
    print('Теперь выполни:')
    print('  git add backend/data/word_metadata.json')
    print('  git commit -m "add compact word database"')
    print('  git push')


if __name__ == '__main__':
    main()
