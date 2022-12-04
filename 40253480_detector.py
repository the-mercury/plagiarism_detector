import math
import string
import sys


class Utilities:
    COMMON = [
        'a', 'an', '',
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
        return text.lower().translate(str.maketrans('', '', string.punctuation)).split(sep=' ')

    @staticmethod
    def frequency_mapping(word_list: list) -> dict:
        frequency_dict = {}
        for new_word in word_list:
            if new_word not in Utilities.COMMON:
                if new_word in frequency_dict:
                    frequency_dict[new_word] = frequency_dict[new_word] + 1
                else:
                    frequency_dict[new_word] = 1
        return frequency_dict

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
    def vector_similarity(freq_dict_1: dict, freq_dict_2: dict, threshold: float = 0.5) -> bool:
        vector_1 = Utilities.normalize_vector(list(freq_dict_1.values()))
        vector_2 = Utilities.normalize_vector(list(freq_dict_2.values()))
        dif = Utilities.vector_magnitude([(vector_2[i] - vector_1[i]) for i in range(len(vector_1))])
        plus = Utilities.vector_magnitude([(vector_2[i] + vector_1[i]) for i in range(len(vector_1))])
        # print(dif / plus)
        return dif / plus < threshold

    @staticmethod
    def sort_dict_by_value(dictionary: dict, reverse: bool = True) -> dict:
        return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse))

    @staticmethod
    def word_dict(set_union: set, freq_dict: dict) -> dict:
        word_dict = {word: 0 for word in set_union}
        for key in word_dict:
            if key in freq_dict.keys():
                word_dict[key] = freq_dict[key]
        return word_dict


def detect_plagiarism() -> bool:
    path_1 = sys.argv[1]
    path_2 = sys.argv[2]
    # path_1 = '../data/plagiarism09/1.txt'
    # path_2 = '../data/plagiarism09/2.txt'
    # path_1 = '../data/okay05/1.txt'
    # path_2 = '../data/okay05/2.txt'
    file_1 = Utilities.read_file(path_1)
    list_1 = Utilities.text_preprocess(file_1)
    freq_dict_1 = Utilities.frequency_mapping(list_1)
    file_2 = Utilities.read_file(path_2)
    list_2 = Utilities.text_preprocess(file_2)
    freq_dict_2 = Utilities.frequency_mapping(list_2)
    set_union_keys = set(freq_dict_1.keys()).union(set(freq_dict_2.keys()))
    word_dict_1 = Utilities.word_dict(set_union_keys, freq_dict_1)
    word_dict_2 = Utilities.word_dict(set_union_keys, freq_dict_2)
    similarity = Utilities.vector_similarity(word_dict_1, word_dict_2)
    return similarity


if __name__ == '__main__':
    try:
        print(1) if detect_plagiarism() else print(0)
    except:
        print(-1)
