import re, json, glob, argparse
from gensim.corpora import WikiCorpus, Dictionary
from gensim.utils import to_unicode
import pandas as pd
from tqdm import tqdm

"""
mkdir -p data/sentence-embeddings/pretrain-data
python preprocess/dump.py \
  --input_path ./sample_bert.xlsx \
  --output_path data/processed/pretrain.txt
split -l 300000 data/processed/pretrain.txt data/sentence-embeddings/pretrain-data/data_
"""

def process_xlsx(xlsx_fname, output_fname):
  df = pd.read_excel(xlsx_fname)
  contents = df['본문']
  with open(output_fname, 'w', encoding='utf-8') as f2:
    for line in tqdm(contents):
      sentences = re.split("(?<=[.!?])\s+", line.strip())
      for sentence in sentences:
          sentence = sentence.replace('.', '')
          sentence = sentence.replace('\n', '')
          f2.writelines(sentence + "\n")
      f2.writelines("\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('--preprocess_mode', type=str, help='preprocess mode')
    parser.add_argument('--input_path', type=str, help='Location of input files')
    parser.add_argument('--output_path', type=str, help='Location of output files')
    parser.add_argument('--with_label', help='with label', type=str, default="False")
    args = parser.parse_args()

    process_xlsx(args.input_path, args.output_path)