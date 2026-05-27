from flask import Flask, request, jsonify
from flask_cors import CORS
from rhyme_engine import RhymeEngine
import logging

app = Flask(__name__)
CORS(app)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация движка рифм
rhyme_engine = RhymeEngine()

@app.route('/api/rhymes', methods=['POST'])
def get_rhymes():
    """Получить рифмы для слова"""
    try:
        data = request.get_json()
        word = data.get('word', '').strip().lower()
        
        if not word:
            return jsonify({'error': 'Слово не указано'}), 400
        
        # Получение фильтров
        filters = {
            'part_of_speech': data.get('partOfSpeech', 'all'),
            'frequency': data.get('frequency', 'all'),
            'syllables': data.get('syllables', 'all')
        }
        
        logger.info(f"Поиск рифм для слова: {word}")
        rhymes = rhyme_engine.find_rhymes(word, filters)
        
        return jsonify({
            'word': word,
            'rhymes': rhymes,
            'count': len(rhymes)
        })
        
    except Exception as e:
        logger.error(f"Ошибка при поиске рифм: {str(e)}")
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return jsonify({'status': 'ok', 'message': 'Сервер работает'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)