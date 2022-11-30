import math
import string
import sys


class Utilities:
    COMMON = [
        'i', 'you', 'he', 'she', 'they', 'we',
        'am', 'is', 'are',
        'my', 'his', 'her', 'their', 'ours',
        'the', 'this', 'that', 'these', 'those', 'it',
        'at', 'on', 'in', 'from', 'to',
        'of', 'if', 'for'
    ]

    @staticmethod
    def read_file(path: str) -> str:
        try:
            with open(path) as f:
                return f.read()
        except Exception as e:
            print(f'>>> Something went wrong reading the file -> {e.__class__, e.__str__()}')
            sys.exit()

    @staticmethod
    def text_preprocess(text: str) -> [str]:
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        return text.lower().translate(str.maketrans('', '', string.punctuation)).split(sep=' ')

    @staticmethod
    def frequency_map(word_list):
        frequency = {}
        for new_word in word_list:
            if new_word not in Utilities.COMMON:
                if new_word in frequency:
                    frequency[new_word] = frequency[new_word] + 1
                else:
                    frequency[new_word] = 1
        return frequency

    @staticmethod
    def dot_product(vector_1, vector_2):
        product_value = 0.0
        for key in vector_1:
            if key in vector_2:
                product_value += (vector_1[key] * vector_2[key]) * len(key)
        return product_value

    @staticmethod
    def vector_cos(freq_map_1, freq_map_2):
        numerator = Utilities.dot_product(freq_map_1, freq_map_2)
        denominator = math.sqrt(Utilities.dot_product(freq_map_1, freq_map_1) * Utilities.dot_product(freq_map_2, freq_map_2))
        return numerator / denominator

    @staticmethod
    def vector_similarity(freq_map_1, freq_map_2, threshold=0.5):
        return Utilities.vector_cos(freq_map_1, freq_map_2) > threshold

    @staticmethod
    def sort_dict_by_value(dictionary, reverse=False):
        return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=reverse))


def detect_plagiarism() -> bool:
    if len(sys.argv) == 1:
        print('\n>>> NO file path passed as an argument!')
        path_1 = input('Please provide path to the first file:\n')
        path_2 = input('Please provide path to the second file:\n')
    else:
        try:
            path_1 = sys.argv[1]
            path_2 = sys.argv[2]
        except Exception as e:
            print(f'Not enough arguments passed!', {e.__class__, e.__str__()})
            sys.exit()
    file_1 = Utilities.read_file(path_1)
    list_1 = Utilities.text_preprocess(file_1)
    freq_map_1 = Utilities.frequency_map(list_1)
    freq_map_1 = Utilities.sort_dict_by_value(freq_map_1, True)
    file_2 = Utilities.read_file(path_2)
    list_2 = Utilities.text_preprocess(file_2)
    freq_map_2 = Utilities.frequency_map(list_2)
    freq_map_2 = Utilities.sort_dict_by_value(freq_map_2, True)
    similar = Utilities.vector_similarity(freq_map_1, freq_map_2)
    return similar


if __name__ == '__main__':
    print(1) if detect_plagiarism() else print(0)
