__author__ = 'Jude Park'
__email__ = 'judepark@kookmin.ac.kr'
__repository__ = ''

import re
from typing import List
from tqdm import tqdm
from konlpy.tag import Okt


"""
All digits will be replaced by <digit>.
Example: 01234 -> <digit>
"""
digit = '<digit>'


def preprocess_corpus_by_regex_rule(corpus: List[str], lower: bool = True) -> List[str]:
    output = []
    language_regex = re.compile('[^a-zA-Z0-9 ㄱ-ㅣ가-힣<>()]+')

    def replace_digit(tokens: List[str]) -> List[str]:
        """Replace the digits to special token such as <digit>."""
        return [w if not re.match('^\d+$', w) else digit for w in tokens]

    for data in tqdm(corpus, desc='preprocess_corpus_by_regex_rule ...'):
        if lower:
            example = data.lower()

        example = language_regex.sub('', data)
        example = re.sub(r'[_<>,\(\)\.\'%]', ' \g<0> ', example)
        example_wo_digit = ' '.join(replace_digit(example.split(' ')))
        output.append(example_wo_digit)

    return output


def tokenize_corpus(tokenizer, corpus: List[str]) -> List[str]:
    output = [tokenizer.morphs(data) for data in tqdm(corpus, desc='tokenize_corpus')]
    return output


if __name__ == '__main__':
    from file_utils import load_json_data
    corpus = load_json_data('./rsc/combine_paper_data.json')
    corpus = [data[0] for data in tqdm(corpus)]
    output = preprocess_corpus_by_regex_rule(corpus)
    # print(output[:100])
    print(tokenize_corpus(Okt(), output)[:10])
