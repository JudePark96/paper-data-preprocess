__author__ = 'Jude Park'
__email__ = 'judepark@kookmin.ac.kr'
__repository__ = ''

from sklearn.model_selection import train_test_split
from file_utils import write_txt_line_by_line
from tqdm import tqdm

corpus, keyphrases = [], []

with open('./rsc/processed_korean_paper_corpus.txt', 'r') as f:
    for line in tqdm(f):
        corpus.append(line.strip())
    f.close()

with open('./rsc/processed_korean_paper_keyphrases.txt', 'r') as f:
    for line in tqdm(f):
        keyphrases.append(line.strip())
    f.close()

assert len(corpus) == len(keyphrases)

train_ratio = 0.75
validation_ratio = 0.15
test_ratio = 0.10
seed = 3435

train_corpus, test_corpus, train_keyphrase, test_keyphrase = train_test_split(corpus, keyphrases,
                                                                              test_size=1 - train_ratio,
                                                                              random_state=seed)
valid_corpus, test_corpus, valid_keyphrase, test_keyphrase = train_test_split(test_corpus, test_keyphrase,
                                                                              test_size=test_ratio / (
                                                                                      test_ratio + validation_ratio),
                                                                              random_state=seed)

assert len(train_corpus) == len(train_keyphrase)
assert len(test_corpus) == len(test_keyphrase)
assert len(valid_corpus) == len(valid_keyphrase)

output_folder = './rsc/train_valid_test_set/'

write_txt_line_by_line(f'{output_folder}training.corpus', train_corpus)
write_txt_line_by_line(f'{output_folder}training.keyphrase', train_keyphrase)
write_txt_line_by_line(f'{output_folder}valid.corpus', valid_corpus)
write_txt_line_by_line(f'{output_folder}valid.keyphrase', valid_keyphrase)
write_txt_line_by_line(f'{output_folder}test.corpus', test_corpus)
write_txt_line_by_line(f'{output_folder}test.keyphrase', test_keyphrase)
