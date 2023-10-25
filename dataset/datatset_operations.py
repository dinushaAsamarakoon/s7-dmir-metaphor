from sinling import SinhalaStemmer
from dataset.elasticsearch_client import bulk_insert_documents, create_metaphor_index
import csv


def read_dataset(file_path):
    with open(file_path, mode='r', encoding='utf_8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header

        metaphors = [row for row in reader if row[5] == 'ඔව්']

    return metaphors


def stem_sinhala_text(text_line: str):
    stemmer = SinhalaStemmer()
    text_line = text_line.lstrip().rstrip()
    words = text_line.split()
    stemmed_words = [stemmer.stem(i)[0] for i in words]
    return ' '.join(stemmed_words)


def convert_metaphor_to_elasticsearch_document(m):
    document = {
        'poem_name': m[0],
        'type': m[1],
        'author': m[2] if m[2] != "" else "කතෘ",
        'year': m[3] if m[3] != "" else "1900",
        'lime': m[4],
        'stemmed_lime': stem_sinhala_text(m[4]),
        'metaphor_available': m[5],
        'count': m[6],
        'source': m[7],
        'target': m[8],
        'meaning': m[9],
    }
    return document


def main():
    metaphors = read_dataset('dataset/190544E_corpus.csv')
    metaphor_documents = [convert_metaphor_to_elasticsearch_document(i) for i in metaphors]
    print(len(metaphor_documents), 'metaphor documents found.')

    create_metaphor_index()
    print(bulk_insert_documents(metaphor_documents))
