const API_URL = 'https://rhymovnik-api.onrender.com';

// Примеры слов
const exampleWords = [
    'любовь', 'день', 'слово', 'мечта', 'душа', 
    'свет', 'весна', 'ночь', 'время', 'рука'
];

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    initializeExamples();
    setupEventListeners();
});

function initializeExamples() {
    const grid = document.getElementById('examplesGrid');
    exampleWords.forEach(word => {
        const btn = document.createElement('button');
        btn.className = 'example-word';
        btn.textContent = word;
        btn.onclick = () => searchWord(word);
        grid.appendChild(btn);
    });
}

function setupEventListeners() {
    document.getElementById('searchBtn').addEventListener('click', handleSearch);
    document.getElementById('searchInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
    
    document.getElementById('toggleFilters').addEventListener('click', toggleFilters);
    
    // Обработчики фильтров
    ['posFilter', 'freqFilter', 'syllablesFilter'].forEach(id => {
        document.getElementById(id).addEventListener('change', handleSearch);
    });
}

function toggleFilters() {
    const panel = document.getElementById('filtersPanel');
    const text = document.getElementById('filterToggleText');
    
    panel.classList.toggle('hidden');
    text.textContent = panel.classList.contains('hidden') 
        ? 'Показать фильтры' 
        : 'Скрыть фильтры';
}

function handleSearch() {
    const word = document.getElementById('searchInput').value.trim();
    if (word) {
        searchWord(word);
    }
}

async function searchWord(word) {
    // Обновляем поле ввода
    document.getElementById('searchInput').value = word;
    
    // Показываем загрузку
    showLoading();
    hideElements(['examplesSection', 'resultsSection', 'noResults']);
    
    // Получаем фильтры
    const filters = {
        partOfSpeech: document.getElementById('posFilter').value,
        frequency: document.getElementById('freqFilter').value,
        syllables: document.getElementById('syllablesFilter').value
    };
    
    try {
        const response = await fetch(`${API_URL}/rhymes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ word, ...filters })
        });
        
        if (!response.ok) {
            throw new Error('Ошибка при получении рифм');
        }
        
        const data = await response.json();
        hideLoading();
        
        if (data.rhymes && data.rhymes.length > 0) {
            displayResults(data.rhymes);
        } else {
            showNoResults();
        }
        
    } catch (error) {
        console.error('Ошибка:', error);
        hideLoading();
        alert('Ошибка при подключении к серверу. Убедитесь, что backend запущен.');
    }
}

function displayResults(rhymes) {
    const resultsSection = document.getElementById('resultsSection');
    const rhymesList = document.getElementById('rhymesList');
    const rhymeCount = document.getElementById('rhymeCount');
    
    rhymeCount.textContent = rhymes.length;
    rhymesList.innerHTML = '';
    
    rhymes.forEach(rhyme => {
        const card = createRhymeCard(rhyme);
        rhymesList.appendChild(card);
    });
    
    resultsSection.classList.remove('hidden');
}

function createRhymeCard(rhyme) {
    const card = document.createElement('div');
    card.className = 'rhyme-card';
    
    const freqClass = `badge-freq-${rhyme.freq}`;
    const freqLabel = {
        high: 'Частое',
        medium: 'Среднее',
        low: 'Редкое'
    }[rhyme.freq];
    
    const syllablesText = rhyme.syllables === 1 ? 'слог' : 
                         rhyme.syllables < 5 ? 'слога' : 'слогов';
    
    card.innerHTML = `
        <div class="rhyme-header">
            <div class="rhyme-word-group">
                <div class="rhyme-word">${rhyme.word}</div>
                <div class="rhyme-pos">${rhyme.pos}</div>
            </div>
            <div class="rhyme-badges">
                <span class="badge ${freqClass}">${freqLabel}</span>
                <span class="badge badge-syllables">${rhyme.syllables} ${syllablesText}</span>
            </div>
        </div>
        <div class="rhyme-example">
            <strong>Пример:</strong> ${rhyme.example}
        </div>
    `;
    
    return card;
}

function showLoading() {
    document.getElementById('loadingSpinner').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingSpinner').classList.add('hidden');
}

function showNoResults() {
    document.getElementById('noResults').classList.remove('hidden');
}

function hideElements(ids) {
    ids.forEach(id => {
        document.getElementById(id).classList.add('hidden');
    });
}