import sys, math, argparse, re
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
from soynlp.normalizer import *
from soyspacing.countbase import CountSpace
from soynlp.hangle import decompose, character_is_korean

import sentencepiece as spm
sys.path.append('models')
from bert.tokenization import FullTokenizer, convert_to_unicode

"""
mkdir -p data/sentence-embeddings/bert/pretrain-ckpt
python preprocess/unsupervised_nlputils.py --preprocess_mode make_bert_vocab \
  --input_path data/processed/pretrain.txt \
  --vocab_path data/sentence-embeddings/bert/pretrain-ckpt/vocab.txt
"""

def make_bert_vocab(input_fname, output_fname):
    train = '--input=' + input_fname + ' --model_prefix=sentpiece --vocab_size=32000 --model_type=bpe --character_coverage=0.9995'
    spm.SentencePieceTrainer.Train(train)
    with open('sentpiece.vocab', 'r', encoding='utf-8') as f1, \
            open(output_fname, 'w', encoding='utf-8') as f2:
        f2.writelines("[PAD]\n[UNK]\n[CLS]\n[SEP]\n[MASK]\n")
        for line in f1:
            word = line.replace('\n', '').split('\t')[0].replace('▁', '##')
            if not word or word in ["##", "<unk>", "<s>", "</s>"]: continue
            f2.writelines(word + "\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preprocess_mode', type=str, help='preprocess mode')
    parser.add_argument('--input_path', type=str, help='Location of input files')
    parser.add_argument('--output_path', type=str, help='Location of output files')
    parser.add_argument('--model_path', type=str, help='Location of model files')
    parser.add_argument('--vocab_path', type=str, help='Location of vocab files')
    parser.add_argument('--with_label', help='with label', type=str, default="False")
    args = parser.parse_args()

    make_bert_vocab(args.input_path, args.vocab_path)

    # if args.preprocess_mode == "train_space":
    #     train_space_model(args.input_path, args.model_path)
    # elif args.preprocess_mode == "apply_space_correct":
    #     apply_space_correct(args.input_path, args.model_path, args.output_path, args.with_label.lower() == "true")
    # elif args.preprocess_mode == "compute_soy_word_score":
    #     compute_soy_word_score(args.input_path, args.model_path)
    # elif args.preprocess_mode == "soy_tokenize":
    #     soy_tokenize(args.input_path, args.model_path, args.output_path)
    # elif args.preprocess_mode == "make_bert_vocab":
    #     make_bert_vocab(args.input_path, args.vocab_path)
    # elif args.preprocess_mode == "bert_tokenize":
    #     bert_tokenize(args.vocab_path, args.input_path, args.output_path)
    # elif args.preprocess_mode == "make_xlnet_vocab":
    #     make_xlnet_vocab(args.input_path, args.vocab_path)
    # elif args.preprocess_mode == "jamo":
    #     process_jamo(args.input_path, args.output_path)