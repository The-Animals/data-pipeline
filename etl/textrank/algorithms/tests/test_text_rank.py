from pkgutil import get_data
from subprocess import run, PIPE
from pathlib import Path
from nltk import sent_tokenize
from os.path import dirname
from os import remove

import textrank.algorithms.text_rank as tr
from textrank.storage.sentence import Sentence

F_SCORE_MIN = 0.8
OUTPUT_FILE = 'output'

def get_test_data(f):
    input_text = str(get_data('textrank', str(Path('algorithms/tests/inputs', f))).decode('utf-8'))
    return input_text

def run_summarizer(input_text):
    sentences = [Sentence(s) for s in sent_tokenize(input_text)]
    summarizer = tr.Summarizer(sentences)
    sentences.sort(key=lambda s: s.rank)
    with open(OUTPUT_FILE, 'w') as f: 
        for s in sentences[:10]: 
            f.write(s.text + '\n')

def evaluate_summarizer(f): 
    path = Path(dirname(tr.__file__), f'tests/inputs/{f}')
    process = run(['sumy_eval', 'text-rank', 'output', f'--file={path}', '--length=10', '--format=plaintext'], stdout=PIPE)
    f_score = float(str(process.stdout.decode('utf-8')).split('\n')[2].split(':')[1])
    return f_score

def test_npl_summarizer_wiki():
    file_name = 'nlp_wiki'
    input_text = get_test_data(file_name)
    run_summarizer(input_text)
    f_score = evaluate_summarizer(file_name)
    assert f_score > F_SCORE_MIN
    remove(OUTPUT_FILE)

def test_automatic_summarization_wiki():
    file_name = 'automatic_summarization_wiki'
    input_text = get_test_data(file_name)
    run_summarizer(input_text)
    f_score = evaluate_summarizer(file_name)
    assert f_score > F_SCORE_MIN
    remove(OUTPUT_FILE)

def test_duties_of_american_citizens():
    file_name = 'duties_of_american_citizens'
    input_text = get_test_data(file_name)
    run_summarizer(input_text)
    f_score = evaluate_summarizer(file_name)
    assert f_score > F_SCORE_MIN
    remove(OUTPUT_FILE)

def test_we_shall_fight_on_the_beaches():
    file_name = 'duties_of_american_citizens'
    input_text = get_test_data(file_name)
    run_summarizer(input_text)
    f_score = evaluate_summarizer(file_name)
    assert f_score > F_SCORE_MIN
    remove(OUTPUT_FILE)

# Should be significantly different because we use an appended set of stop words
def test_speech_from_the_throne():
    file_name = 'speech_from_the_throne_2020'
    input_text = get_test_data(file_name)
    run_summarizer(input_text)
    f_score = evaluate_summarizer(file_name)
    assert f_score < 0.5
    remove(OUTPUT_FILE)