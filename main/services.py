import math
import re
from collections import Counter

stop_words_ru = {
    "и", "в", "во", "не", "что", "он", "на", "я", "с", "со", "как", "а", "то", "все", "она", "так",
    "его", "но", "да", "ты", "к", "у", "же", "вы", "за", "бы", "по", "только", "ее", "мне", "было",
    "вот", "от", "меня", "еще", "нет", "о", "из", "ему", "теперь", "когда", "даже", "ну", "вдруг",
    "ли", "если", "уже", "или", "ни", "быть", "был", "него", "до", "вас", "нибудь", "опять", "уж",
    "вам", "ведь", "там", "потом", "себя", "ничего", "ей", "может", "они", "тут", "где", "есть",
    "надо", "ней", "для", "мы", "тебя", "их", "чем", "была", "сам", "чтоб", "без", "будто", "чего",
    "раз", "тоже", "себе", "под", "будет", "ж", "тогда", "кто", "этот", "того", "потому", "этого",
    "какой", "совсем", "ним", "здесь", "этом", "один", "почти", "мой", "тем", "чтобы", "нее",
    "сейчас", "были", "куда", "зачем", "всех", "никогда", "можно", "при", "наконец", "два",
    "об", "другой", "хоть", "после", "над", "больше", "тот", "через", "эти", "нас", "про", "всего",
    "них", "какая", "много", "разве", "три", "эту", "моя", "впрочем", "хорошо", "свою", "этой",
    "перед", "иногда", "лучше", "чуть", "том", "нельзя", "такой", "им", "более", "всегда", "конечно",
    "всю", "между"
}


def get_file_content(file_path: str) -> str:
    with open(file_path, 'r', encoding="utf-8") as file:
        return file.read()


def filter_words(text: str) -> list[str]:
    words = re.findall(r'\b\w+\b', text.lower())
    return [word for word in words if word not in stop_words_ru]


def compute_tf(word_counts: Counter) -> dict:
    total_terms = sum(word_counts.values())
    return {word: count / total_terms for word, count in word_counts.items()}


def compute_idf(word_counts: Counter, all_docs: list[Counter]) -> dict:
    num_docs = len(all_docs)
    idf_values = {}
    for word in word_counts:
        doc_freq = sum(1 for doc in all_docs if word in doc)
        idf_values[word] = math.log((num_docs + 1) / (doc_freq + 1)) + 1  # Smoothed IDF
    return idf_values


def compute_tf_idf(text: str) -> list[tuple[str, float, float]]:
    words = filter_words(text)
    word_counts = Counter(words)
    tf = compute_tf(word_counts)
    idf = compute_idf(word_counts, [word_counts])

    tfidf_list = [(word, round(tf[word], 6), round(idf[word], 6)) for word in word_counts]
    return sorted(tfidf_list, key=lambda x: x[2], reverse=True)[:50]


def handle_text_file(file_path: str) -> list[tuple[str, float, float]]:
    text = get_file_content(file_path)
    return compute_tf_idf(text)