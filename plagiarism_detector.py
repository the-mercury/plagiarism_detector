import math
import string
import sys


class Utilities:
    COMMON = [
        'a', 'an',
        'i', 'you', 'he', 'she', 'they', 'we',
        'am', 'is', 'are', 'be',
        'my', 'his', 'her', 'their', 'ours',
        'the', 'this', 'that', 'these', 'those', 'it',
        'at', 'on', 'in', 'from', 'to',
        'of', 'if', 'for',
        'too', 'but', 'not',
        'or', 'and',
        'all', 'so'
    ]

    @staticmethod
    def read_file(path: str) -> str:
        with open(path) as f:
            return f.read()

    @staticmethod
    def text_preprocess(text: str) -> [str]:
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        return text.lower().translate(str.maketrans('', '', string.punctuation)).split()

    @staticmethod
    def vector_magnitude(vector: list) -> float:
        mag = 0
        for ele in vector:
            mag += ele * ele
        return math.sqrt(mag)

    @staticmethod
    def normalize_vector(vector: list) -> list:
        vector_magnitude = Utilities.vector_magnitude(vector)
        return [vector[i]/vector_magnitude for i in range(len(vector))]

    @staticmethod
    def vector_similarity(vector_1: list, vector_2: list, threshold: float = 0.5) -> bool:
        dif = Utilities.vector_magnitude([(vector_2[i] - vector_1[i]) for i in range(len(vector_1))])
        plus = Utilities.vector_magnitude([(vector_2[i] + vector_1[i]) for i in range(len(vector_1))])
        return dif / plus < threshold

    @staticmethod
    def word_dict(set_union: set, word_list: list) -> dict:
        word_dict = {word: 0 for word in set_union}
        for word in word_list:
            if word in Utilities.COMMON:
                word_dict[word] += 0.1
            else:
                word_dict[word] += 1
        return word_dict


def detect_plagiarism() -> bool:
    path_1 = sys.argv[1]
    path_2 = sys.argv[2]
    file_1 = Utilities.read_file(path_1)
    list_1 = Utilities.text_preprocess(file_1)
    file_2 = Utilities.read_file(path_2)
    list_2 = Utilities.text_preprocess(file_2)
    set_union_keys = set(list_1).union(set(list_2))
    word_dict_1 = Utilities.word_dict(set_union_keys, list_1)
    word_dict_2 = Utilities.word_dict(set_union_keys, list_2)
    vector_1 = Utilities.normalize_vector(list(word_dict_1.values()))
    vector_2 = Utilities.normalize_vector(list(word_dict_2.values()))
    similarity = Utilities.vector_similarity(vector_1, vector_2)
    return similarity


if __name__ == '__main__':
    try:
        print(1) if detect_plagiarism() else print(0)
    except Exception:
        print(-1)
