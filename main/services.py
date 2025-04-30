import math
import os
import re
from collections import Counter

from main.models import File, FileAnalysis
from project.settings import BASE_DIR

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
    if total_terms == 0:
        return {}
    return {word: count / total_terms for word, count in word_counts.items()}


def compute_idf(word: str, all_docs_word_counts: list[Counter]) -> float:
    num_docs = len(all_docs_word_counts)
    if num_docs == 0:
        return 0.0

    doc_freq = sum(1 for doc in all_docs_word_counts if word in doc)
    return math.log((num_docs + 1) / (doc_freq + 1)) + 1


def get_all_document_word_counts():
    all_docs_word_counts = []

    file_objects = File.objects.all()
    for file in file_objects:
        try:
            file_path = file.file.path
            text = get_file_content(file_path)
            words = filter_words(text)
            doc_word_counts = Counter(words)
            all_docs_word_counts.append(doc_word_counts)
        except (UnicodeDecodeError, FileNotFoundError, Exception) as e:
            print(f"Error processing file {file.file_name}: {str(e)}")
            continue

    return all_docs_word_counts


def compute_tf_idf(text: str) -> list[tuple[str, float, float, float]]:
    words = filter_words(text)
    word_counts = Counter(words)
    tf = compute_tf(word_counts)

    all_docs_word_counts = get_all_document_word_counts()

    current_doc_added = False
    for doc in all_docs_word_counts:
        if doc == word_counts:
            current_doc_added = True
            break

    if not current_doc_added:
        all_docs_word_counts.append(word_counts)

    idf_values = {}
    for word in word_counts:
        idf_values[word] = compute_idf(word, all_docs_word_counts)

    tfidf_list = []
    for word in word_counts:
        tf_score = tf[word]
        idf_score = idf_values[word]
        tfidf_score = tf_score * idf_score
        tfidf_list.append((word, round(tf_score, 6), round(idf_score, 6), round(tfidf_score, 6)))

    return sorted(tfidf_list, key=lambda x: x[2], reverse=True)[:50]


def handle_text_file(file_path) -> list[tuple[str, float, float, float]]:
    try:
        text = get_file_content(file_path)
        return compute_tf_idf(text)
    except UnicodeDecodeError:
        print(f"Error: Unable to decode file {file_path}. Make sure it's a valid text file with UTF-8 encoding.")
        return []
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return []


def compute_tfidf_for_file(file):
    analysis_result = handle_text_file(os.path.join(BASE_DIR, file.file.path))
    tfidf_data = [
        {"word": word, "tf": tf, "idf": idf, "tfidf": tfidf}
        for word, tf, idf, tfidf in analysis_result
    ]
    return tfidf_data


def update_all_file_analyses():
    files = File.objects.all()
    for file in files:
        try:
            tfidf_data = compute_tfidf_for_file(file)
            FileAnalysis.objects.update_or_create(
                file=file,
                defaults={"tfidf_data": tfidf_data}
            )
        except Exception as e:
            print(f"Error updating analysis for {file.file_name}: {str(e)}")