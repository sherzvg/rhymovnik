import re
import json
import hashlib
from typing import List, Dict
from collections import defaultdict
import os

class RhymeEngine:
    def __init__(self):
        """Инициализация движка рифм"""
        self.vowels = 'аеёиоуыэюя'
        self.consonants = 'бвгджзйклмнпрстфхцчшщ'
        
        # Загружаем базу слов
        self.word_database = self._load_word_database()
        print(f"Загружено {len(self.word_database)} слов в базу")
        
    def _load_word_database(self) -> Dict:
        """Загрузка базы слов с метаданными"""
        
        # Абсолютные пути относительно папки этого файла
        base_dir = os.path.dirname(os.path.abspath(__file__))
        words_file = os.path.join(base_dir, 'data', 'russian_words.txt')
        metadata_file = os.path.join(base_dir, 'data', 'word_metadata.json')
        
        # Если есть сохранённые метаданные - загружаем их
        if os.path.exists(metadata_file):
            print("Загружаем метаданные из файла...")
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Иначе создаём базовую базу + загружаем слова из файла
        database = self._get_base_database()

        # Если есть файл со словами - загружаем дополнительные слова
        # Слова из базового словаря имеют приоритет над словами из файла
        if os.path.exists(words_file):
            print("Загружаем дополнительные слова...")
            file_words = self._load_words_from_file(words_file)
            for word, metadata in file_words.items():
                if word not in database:
                    database[word] = metadata
        
        # Сохраняем метаданные для быстрой загрузки в следующий раз (если возможно)
        try:
            os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, ensure_ascii=False, indent=2)
        except OSError:
            pass  # На read-only файловых системах просто пропускаем
        
        return database
    
    def _get_base_database(self) -> Dict:
        """Базовая база слов (ваш исходный словарь)"""
        return {
            'любовь': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'кровь': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'морковь': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'бровь': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'вновь': {'pos': 'наречие', 'freq': 'high', 'syllables': 1},
            'готовь': {'pos': 'глагол', 'freq': 'medium', 'syllables': 2},
            'обновь': {'pos': 'глагол', 'freq': 'low', 'syllables': 2},
            'изголовь': {'pos': 'существительное', 'freq': 'low', 'syllables': 3},
            
            'день': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'тень': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'лень': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'пень': {'pos': 'существительное', 'freq': 'medium', 'syllables': 1},
            'сирень': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'олень': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'ступень': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'плетень': {'pos': 'существительное', 'freq': 'low', 'syllables': 2},
            'мишень': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            
            'слово': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'снова': {'pos': 'наречие', 'freq': 'high', 'syllables': 2},
            'основа': {'pos': 'существительное', 'freq': 'high', 'syllables': 3},
            'готово': {'pos': 'прилагательное', 'freq': 'high', 'syllables': 3},
            'сурово': {'pos': 'наречие', 'freq': 'medium', 'syllables': 3},
            'здорово': {'pos': 'наречие', 'freq': 'high', 'syllables': 4},
            
            'мечта': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'высота': {'pos': 'существительное', 'freq': 'high', 'syllables': 3},
            'красота': {'pos': 'существительное', 'freq': 'high', 'syllables': 3},
            'пустота': {'pos': 'существительное', 'freq': 'high', 'syllables': 3},
            'темнота': {'pos': 'существительное', 'freq': 'high', 'syllables': 3},
            'чистота': {'pos': 'существительное', 'freq': 'medium', 'syllables': 3},
            
            'душа': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'хороша': {'pos': 'прилагательное', 'freq': 'high', 'syllables': 3},
            'малыша': {'pos': 'существительное', 'freq': 'medium', 'syllables': 3},
            'глуша': {'pos': 'существительное', 'freq': 'low', 'syllables': 2},
            'тиша': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            
            'свет': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'привет': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'ответ': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'рассвет': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'букет': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'кабинет': {'pos': 'существительное', 'freq': 'medium', 'syllables': 3},
            'портрет': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'нет': {'pos': 'частица', 'freq': 'high', 'syllables': 1},
            
            'весна': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'война': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'страна': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'она': {'pos': 'местоимение', 'freq': 'high', 'syllables': 2},
            'тишина': {'pos': 'существительное', 'freq': 'high', 'syllables': 3},
            'волна': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'сторона': {'pos': 'существительное', 'freq': 'high', 'syllables': 3},
            'цена': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            
            'ночь': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'дочь': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'мочь': {'pos': 'глагол', 'freq': 'high', 'syllables': 1},
            'прочь': {'pos': 'наречие', 'freq': 'medium', 'syllables': 1},
            
            'время': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'бремя': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'семя': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'племя': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'стремя': {'pos': 'существительное', 'freq': 'low', 'syllables': 2},
            
            'рука': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'река': {'pos': 'существительное', 'freq': 'high', 'syllables': 2},
            'мука': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            'тоска': {'pos': 'существительное', 'freq': 'medium', 'syllables': 2},
            
            'дом': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'сон': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'том': {'pos': 'существительное', 'freq': 'medium', 'syllables': 1},
            'ком': {'pos': 'существительное', 'freq': 'medium', 'syllables': 1},
            'гром': {'pos': 'существительное', 'freq': 'medium', 'syllables': 1},
            
            'путь': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'грудь': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'суть': {'pos': 'существительное', 'freq': 'high', 'syllables': 1},
            'ртуть': {'pos': 'существительное', 'freq': 'low', 'syllables': 1},
        }
    
    def _load_words_from_file(self, filepath: str) -> Dict:
        """
        Загрузка слов из текстового файла
        Формат: одно слово на строку
        """
        additional_words = {}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    
                    # Пропускаем пустые строки и уже существующие слова
                    if not word or word in additional_words:
                        continue
                    
                    # Автоматически определяем метаданные
                    metadata = self._auto_detect_metadata(word)
                    additional_words[word] = metadata
                    
            print(f"Загружено {len(additional_words)} новых слов из файла")
        except FileNotFoundError:
            print(f"Файл {filepath} не найден. Используем только базовую базу.")
        
        return additional_words
    
    def _auto_detect_metadata(self, word: str) -> Dict:
        """Автоматическое определение метаданных по окончанию слова"""
        syllables = self._count_syllables(word)
        pos = self._detect_pos(word)

        # Эвристика частоты: односложные слова обычно самые частые,
        # трёхсложные и длиннее — редкие
        if syllables == 1:
            freq = 'high'
        elif syllables == 2:
            freq = 'medium'
        else:
            freq = 'low'

        return {'pos': pos, 'freq': freq, 'syllables': syllables}

    def _detect_pos(self, word: str) -> str:
        """Определение части речи по окончанию"""

        # Местоимения — конкретный список
        pronouns = {
            'я', 'ты', 'он', 'она', 'оно', 'мы', 'вы', 'они',
            'меня', 'тебя', 'его', 'её', 'нас', 'вас', 'их',
            'мне', 'тебе', 'ему', 'ей', 'нам', 'вам', 'им',
            'мной', 'тобой', 'им', 'ней', 'нами', 'вами', 'ими',
            'себя', 'себе', 'собой', 'кто', 'что', 'кого', 'чего',
            'кому', 'чему', 'кем', 'чем', 'этот', 'эта', 'это',
            'эти', 'того', 'той', 'тот', 'те', 'тем', 'той',
            'свой', 'своя', 'своё', 'свои', 'своего', 'своей',
            'никто', 'ничто', 'некто', 'нечто', 'некого', 'нечего',
            'каждый', 'каждая', 'каждое', 'каждые',
        }
        if word in pronouns:
            return 'местоимение'

        # Глаголы — инфинитивы
        if word.endswith(('ться', 'тся')):
            return 'глагол'
        if word.endswith(('ывать', 'ивать', 'овать', 'евать')):
            return 'глагол'
        if word.endswith(('нуть', 'вать')):
            return 'глагол'
        if word.endswith(('ать', 'ять', 'ить', 'еть', 'оть', 'уть')):
            return 'глагол'
        if word.endswith(('сти', 'зти', 'чь', 'ти')) and len(word) > 3:
            return 'глагол'
        # Спрягаемые формы глаголов
        if word.endswith(('аешь', 'яешь', 'уешь', 'ёшь', 'ишь', 'ешь')):
            return 'глагол'
        if word.endswith(('ает', 'яет', 'ует', 'ёт', 'ит')) and len(word) > 3:
            return 'глагол'
        if word.endswith(('ают', 'яют', 'уют', 'ят', 'ут')) and len(word) > 3:
            return 'глагол'
        if word.endswith(('аем', 'яем', 'уем', 'им', 'ем')) and len(word) > 4:
            return 'глагол'
        if word.endswith(('айте', 'яйте', 'уйте', 'ите', 'ете')) and len(word) > 5:
            return 'глагол'
        if word.endswith(('ал', 'яла', 'ило', 'ила', 'али', 'яли', 'или', 'ели', 'ало', 'яло')):
            return 'глагол'

        # Прилагательные
        if word.endswith(('ый', 'ий', 'ой')):
            return 'прилагательное'
        if word.endswith(('ая', 'яя')):
            return 'прилагательное'
        if word.endswith(('ое', 'ее')):
            return 'прилагательное'
        if word.endswith(('ого', 'его', 'ому', 'ему')):
            return 'прилагательное'
        if word.endswith(('ым', 'им')) and len(word) > 4:
            return 'прилагательное'
        if word.endswith(('ых', 'их')) and len(word) > 4:
            return 'прилагательное'
        if word.endswith(('ыми', 'ими')) and len(word) > 5:
            return 'прилагательное'

        # Наречия
        if word.endswith(('ски', 'цки', 'чески', 'чно', 'жно', 'дно')) and len(word) > 4:
            return 'наречие'
        if word.endswith(('ально', 'ельно', 'льно')) and len(word) > 6:
            return 'наречие'
        # Наречия на -иво (красиво, игриво), -ро (быстро, остро, хитро)
        if word.endswith('иво') and len(word) > 5:
            return 'наречие'
        if re.search(r'[бвгджзклмнпрстфхцчшщ]ро$', word) and len(word) > 4:
            return 'наречие'

        return 'существительное'
    
    def _count_syllables(self, word: str) -> int:
        """Подсчёт количества слогов (по гласным буквам)"""
        count = 0
        for char in word.lower():
            if char in self.vowels:
                count += 1
        return max(count, 1)  # Минимум 1 слог
    
    def _get_phonetic_ending(self, word: str, length: int = 3) -> str:
        """Получить фонетическое окончание слова"""
        word = word.lower()
        ending = word[-length:] if len(word) >= length else word
        
        # Учитываем оглушение согласных в конце
        replacements = {
            'б': 'п', 'в': 'ф', 'г': 'к', 
            'д': 'т', 'ж': 'ш', 'з': 'с'
        }
        
        if ending and ending[-1] in replacements:
            ending = ending[:-1] + replacements[ending[-1]]
        
        return ending
    
    def _calculate_rhyme_score(self, word1: str, word2: str) -> int:
        """
        Вычислить качество рифмы (0-100)
        
        Принцип работы:
        1. Берём окончания обоих слов (4 последние буквы)
        2. Сравниваем их с конца посимвольно
        3. За каждую совпавшую букву даём +25 баллов
        4. Останавливаемся при первом несовпадении
        
        Пример:
        любовь → бовь
        кровь  → ровь
        
        Сравниваем с конца:
        ь = ь → +25 (итого 25)
        в = в → +25 (итого 50)
        о = о → +25 (итого 75)
        б ≠ р → СТОП
        
        Итого: 75 баллов
        """
        ending1 = self._get_phonetic_ending(word1, 4)
        ending2 = self._get_phonetic_ending(word2, 4)
        
        score = 0
        for i in range(min(len(ending1), len(ending2))):
            if ending1[-(i+1)] == ending2[-(i+1)]:
                score += 25
            else:
                break
        
        return min(score, 100)
    
    def _make_example(self, word: str, pos: str) -> str:
        """Генерация простого примера использования слова"""
        templates = {
            'существительное': [
                f'На горизонте — {word}.',
                f'В душе жила {word}.',
                f'Звучала тихо {word}.',
            ],
            'глагол': [
                f'Судьба велит: {word}.',
                f'Сердце просит: {word}.',
                f'Голос шепчет: {word}.',
            ],
            'прилагательное': [
                f'Всё казалось {word}.',
                f'Мир был {word}.',
                f'Небо стало {word}.',
            ],
            'наречие': [
                f'Время шло {word}.',
                f'Жизнь текла {word}.',
                f'Он ушёл {word}.',
            ],
            'местоимение': [
                f'Лишь {word} знает всё.',
                f'Думаю о {word}.',
                f'Без {word} — никуда.',
            ],
        }
        idx = int(hashlib.md5(word.encode()).hexdigest(), 16) % 3
        return templates.get(pos, templates['существительное'])[idx]

    def find_rhymes(self, word: str, filters: Dict) -> List[Dict]:
        """
        Найти рифмы для слова
        
        Алгоритм:
        1. Получаем окончание исходного слова (2 последние буквы)
        2. Ищем в базе все слова с похожим окончанием
        3. Для каждого кандидата вычисляем качество рифмы (score)
        4. Оставляем только рифмы с score >= 25
        5. Применяем фильтры пользователя
        6. Сортируем по качеству рифмы
        """
        word = word.lower().strip()
        rhymes = []
        
        # Получаем окончание для поиска
        ending = self._get_phonetic_ending(word, 2)
        
        # Поиск рифм в базе
        for candidate, metadata in self.word_database.items():
            # Пропускаем само слово
            if candidate == word:
                continue
            
            candidate_ending = self._get_phonetic_ending(candidate, 2)
            
            # Проверка на схожесть окончаний
            if ending in candidate_ending or candidate_ending in ending:
                score = self._calculate_rhyme_score(word, candidate)
                
                # Минимальный порог качества рифмы
                if score >= 25:
                    rhymes.append({
                        'word': candidate,
                        'score': score,
                        'pos': metadata['pos'],
                        'freq': metadata['freq'],
                        'syllables': metadata['syllables'],
                        'example': self._make_example(candidate, metadata['pos'])
                    })
        
        # Применение фильтров
        filtered_rhymes = self._apply_filters(rhymes, filters)
        
        # Сортировка по качеству рифмы (от лучшей к худшей)
        filtered_rhymes.sort(key=lambda x: x['score'], reverse=True)
        
        return filtered_rhymes
    
    def _apply_filters(self, rhymes: List[Dict], filters: Dict) -> List[Dict]:
        """
        Применить фильтры к результатам
        
        Фильтры:
        - part_of_speech: часть речи (существительное, глагол и т.д.)
        - frequency: частота использования (high, medium, low)
        - syllables: количество слогов (1, 2, 3, 4+)
        """
        filtered = rhymes
        
        # Фильтр по части речи
        if filters['part_of_speech'] != 'all':
            filtered = [r for r in filtered if r['pos'] == filters['part_of_speech']]
        
        # Фильтр по частоте
        if filters['frequency'] != 'all':
            filtered = [r for r in filtered if r['freq'] == filters['frequency']]
        
        # Фильтр по слогам
        if filters['syllables'] != 'all':
            syllables = int(filters['syllables'])
            if syllables >= 4:
                filtered = [r for r in filtered if r['syllables'] >= 4]
            else:
                filtered = [r for r in filtered if r['syllables'] == syllables]
        
        return filtered