import re
import csv
from collections import Counter
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_epub(file_path):
    # Otwórz plik epub
    book = epub.read_epub(file_path)
    text_content = []

    # Przejdź przez wszystkie elementy w książce
    for item in book.get_items():
        # Sprawdź, czy element jest dokumentem tekstowym
        if item.media_type == 'application/xhtml+xml':
            # Wyciągnij tekst z HTML-a za pomocą BeautifulSoup
            soup = BeautifulSoup(item.get_body_content(), 'html.parser')
            text_content.append(soup.get_text())

    # Połącz całość tekstu w jeden łańcuch
    return ' '.join(text_content)

def get_word_frequencies(text):
    # Znajdź wszystkie słowa, ignorując wielkość liter
    words = re.findall(r'\b\w+\b', text.lower())
    # Zlicz wystąpienia każdego słowa
    return Counter(words)

def save_word_frequencies_to_csv(word_counts, file_name='word_frequencies.csv'):
    # Zapisz wyniki do pliku CSV
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Zapisz nagłówki
        writer.writerow(['Word', 'Frequency'])
        # Zapisz każde słowo i jego liczbę wystąpień
        for word, count in word_counts.items():
            writer.writerow([word, count])

# Główna część skryptu
file_path = 'pg11.epub'  # Zmień na ścieżkę do swojego pliku epub
text = extract_text_from_epub(file_path)
word_counts = get_word_frequencies(text)

# Zapisz wyniki do pliku CSV
save_word_frequencies_to_csv(word_counts)
