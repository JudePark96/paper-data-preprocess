__author__ = 'Jude Park'
__email__ = 'judepark@kookmin.ac.kr'
__repository__ = ''

import re
from typing import Tuple, List
from konlpy.tag import Okt
from tqdm import tqdm

import pickle
import json

# end of title
eot_token = '<eot>'

digit = '<digit>'

p_start = '<p_start>'
a_start = '<a_start>'
delimiter = ';'


def load_json_data(src_path: str, is_eot_token: bool = False):
    abstract, word = [], []
    language_regex = re.compile('[^a-zA-Z0-9 ㄱ-ㅣ가-힣()]+')
    tokenizer = Okt()

    def replace_digit(tokens: List[str]) -> List[str]:
        """Replace the digits to special token such as <digit>."""
        return [w if not re.match('^\d+$', w) else digit for w in tokens]

    p = 0
    a = 0

    with open(src_path, 'r', encoding='utf-8') as f:
        for line in tqdm(f):
            data = json.loads(line)
            if is_eot_token:
                content = data['title'] + ' ' + eot_token + ' ' + data['abstract']
            else:
                content = data['abstract']

            content = content.lower()
            content = language_regex.sub('', content)
            content = re.sub(r'[_<>,\(\)\.\'%]', ' \g<0> ', content)
            content = ' '.join(replace_digit(content.split(' ')))
            content = ' '.join(tokenizer.morphs(content))

            keywords = data['keyword']
            keywords = [language_regex.sub('', keyword) for keyword in keywords.split(';')]

            present_keywords = []
            absent_keywords = []

            if '' not in keywords:
                for keyword in keywords:
                    if keyword not in content:
                        a += 1
                        absent_keywords.append(f'{a_start} {" ".join(tokenizer.morphs(keyword, stem=True))}')
                    else:
                        p += 1
                        present_keywords.append(f'{p_start} {" ".join(tokenizer.morphs(keyword, stem=True))}')

                all_keywords = present_keywords + absent_keywords
                all_keywords = f' {delimiter} '.join(all_keywords)
                abstract.append(content.strip())
                word.append(all_keywords.strip())
        f.close()

    print(f'total data number => {len(abstract)}')
    print(f'total present keywords => {p}')
    print(f'total absent keywords => {a}')

    with open('./rsc/processed_korean_paper_corpus.txt', 'w', encoding='utf-8') as f:
        for line in tqdm(abstract):
            f.write(line + '\n')
        f.close()

    with open('./rsc/processed_korean_paper_keyphrases.txt', 'w', encoding='utf-8') as f:
        for line in tqdm(word):
            f.write(line + '\n')
        f.close()


if __name__ == '__main__':
    load_json_data('./rsc/combine_paper_data.json')
