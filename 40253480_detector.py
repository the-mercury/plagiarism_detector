import math
import string


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
        except:
            raise Exception('Something went wrong reading the file at: {path}')

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


def detect_plagiarism(path_1: str = '', path_2: str = '') -> bool:
    path_1 = r'/Users/mercury/Documents/Documents - Mehrdad’s MacBook Pro/CS_Concordia/S1/Algorithm Design Techniques/project/sample_data_and_submission/data/okay02/1.txt'
    path_2 = r'/Users/mercury/Documents/Documents - Mehrdad’s MacBook Pro/CS_Concordia/S1/Algorithm Design Techniques/project/sample_data_and_submission/data/okay02/2.txt'
    # path_1 = r'/Users/mercury/Documents/Documents - Mehrdad’s MacBook Pro/CS_Concordia/S1/Algorithm Design Techniques/project/sample_data_and_submission/data/plagiarism08/1.txt'
    # path_2 = r'/Users/mercury/Documents/Documents - Mehrdad’s MacBook Pro/CS_Concordia/S1/Algorithm Design Techniques/project/sample_data_and_submission/data/plagiarism08/2.txt'

    file_1 = Utilities.read_file(path_1)
    list_1 = Utilities.text_preprocess(file_1)
    freq_map_1 = Utilities.frequency_map(list_1)
    freq_map_1 = Utilities.sort_dict_by_value(freq_map_1, True)
    file_2 = Utilities.read_file(path_2)
    list_2 = Utilities.text_preprocess(file_2)
    freq_map_2 = Utilities.frequency_map(list_2)
    freq_map_2 = Utilities.sort_dict_by_value(freq_map_2, True)
    similar = Utilities.vector_similarity(freq_map_1, freq_map_2)
    print(similar)
    return similar


if __name__ == '__main__':
    # if detect_plagiarism(input('provide path to the first file:\n'),
    #                      input('provide path to the second file:\n')):
    #     print(0)
    # else:
    #     print(1)
    detect_plagiarism()
