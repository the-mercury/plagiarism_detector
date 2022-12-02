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
        return text.lower().translate(str.maketrans('', '', string.punctuation)).split(sep=' ')

    @staticmethod
    def frequency_map(word_list: list) -> dict:
        frequency = {}
        for new_word in word_list:
            if new_word not in Utilities.COMMON:
                if new_word in frequency:
                    frequency[new_word] = frequency[new_word] + 1
                else:
                    frequency[new_word] = 1
        return frequency

    @staticmethod
    def dot_product(vector_1: dict, vector_2: dict) -> float:
        product_value = 0.0
        for key in vector_1:
            if key in vector_2:
                product_value += (vector_1[key] * vector_2[key]) * len(key)
        return product_value

    @staticmethod
    def vector_magnitude(vector):
        mag = 0
        for ele in vector:
            mag += ele * ele
        return math.sqrt(mag)

    @staticmethod
    def vector_cos(freq_map_1: dict, freq_map_2: dict) -> float:
        numerator = Utilities.dot_product(freq_map_1, freq_map_2)
        denominator = math.sqrt(Utilities.dot_product(freq_map_1, freq_map_1) * Utilities.dot_product(freq_map_2, freq_map_2))
        return numerator / denominator

    @staticmethod
    def vector_similarity(freq_map_1: dict, freq_map_2: dict, threshold: float = 0.5) -> bool:
        # print(1 - Utilities.vector_cos(freq_map_1, freq_map_2))
        return Utilities.vector_cos(freq_map_1, freq_map_2) > threshold

    @staticmethod
    def vector_similarity_2(freq_map_1: dict, freq_map_2: dict, threshold: float = 0.5) -> bool:
        vector_1 = list(freq_map_1.values())
        vector_2 = list(freq_map_2.values())
        dif = Utilities.vector_magnitude([(vector_2[i] - vector_1[i]) for i in range(len(vector_1))])
        plus = Utilities.vector_magnitude([(vector_2[i] + vector_1[i]) for i in range(len(vector_1))])
        # print(dif/plus)
        return dif / plus < threshold

    @staticmethod
    def sort_dict_by_value(dictionary: dict, reverse: bool = True) -> dict:
        return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse))


def detect_plagiarism() -> bool:
    path_1 = sys.argv[1]
    path_2 = sys.argv[2]
    file_1 = Utilities.read_file(path_1)
    list_1 = Utilities.text_preprocess(file_1)
    freq_map_1 = Utilities.frequency_map(list_1)
    freq_map_1 = Utilities.sort_dict_by_value(freq_map_1)
    file_2 = Utilities.read_file(path_2)
    list_2 = Utilities.text_preprocess(file_2)
    freq_map_2 = Utilities.frequency_map(list_2)
    freq_map_2 = Utilities.sort_dict_by_value(freq_map_2)
    similar = Utilities.vector_similarity(freq_map_1, freq_map_2)
    return similar


def detect_plagiarism_2() -> bool:
    path_1 = sys.argv[1]
    path_2 = sys.argv[2]
    # path_1 = '../data/okay01/1.txt'
    # path_2 = '../data/okay01/2.txt'
    file_1 = Utilities.read_file(path_1)
    list_1 = Utilities.text_preprocess(file_1)
    freq_map_1 = Utilities.frequency_map(list_1)
    freq_map_1 = Utilities.sort_dict_by_value(freq_map_1)
    file_2 = Utilities.read_file(path_2)
    list_2 = Utilities.text_preprocess(file_2)
    freq_map_2 = Utilities.frequency_map(list_2)
    freq_map_2 = Utilities.sort_dict_by_value(freq_map_2)
    set_union = set(freq_map_1.keys()).union(set(freq_map_2.keys()))
    word_dict_1 = {word: 0 for word in set_union}
    word_dict_2 = {word: 0 for word in set_union}
    for key in word_dict_1:
        if key in freq_map_1.keys():
            word_dict_1[key] = freq_map_1[key]
        else:
            word_dict_1[key] = 0
    for key in word_dict_2:
        if key in freq_map_2.keys():
            word_dict_2[key] = freq_map_2[key]
        else:
            word_dict_2[key] = 0
    similarity = Utilities.vector_similarity_2(word_dict_1, word_dict_2)
    return similarity


if __name__ == '__main__':
    try:
        print(1) if detect_plagiarism_2() else print(0)
        # print(1) if detect_plagiarism() else print(0)
    except:
        print(-1)
