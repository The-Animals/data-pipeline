from pathlib import Path
import json
from pkgutil import get_data
import pytest

from preprocess.speech_parser import SpeechParser

input_data_folder = 'parse_speeches_test_data/input/'
output_data_folder = 'parse_speeches_test_data/output/'

def get_test_data(f):
    input_text = str(get_data('preprocess', str(Path('speech_parser/tests/inputs', f))).decode('utf-8'))
    output_text = str(get_data('preprocess', str(Path('speech_parser/tests/outputs', f))).decode('utf-8'))
    return input_text, output_text


def test_extract_speech_with_title_and_page_break():
    mlas = {'Member Loyola'}
    input_text, output = get_test_data('title_and_page_break')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)

    for v in speeches.values(): 
        for s in v:
            assert s in output

def test_extract_speech_with_time_and_page_break():
    mlas = {'Ms Ganley'}
    input_text, output = get_test_data('time_and_page_break')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values(): 
        for s in v:
            assert s in output

def test_extract_speech_with_multiple_mlas():
    mlas = {'Ms Glasgo', 'Mr.Panda'}
    input_text, output = get_test_data('multiple_mlas')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)

    for v in speeches.values(): 
        for s in v:
            assert s in output

def test_extract_speech_with_speaker_after_mla():
    mlas = {'Ms Sigurdson'}
    input_text, output = get_test_data('speaker_after_mla')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values(): 
        for s in v:
            assert s in output

def test_extract_with_weird_line_break():
    mlas = {'Ms Sweet'}
    input_text, output = get_test_data('weird_line_break')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values():
        for s in v:
            assert s in output

def test_extract_member_ceci():
    mlas = {'Member Ceci'}
    input_text, output = get_test_data('member_ceci')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values():
        for s in v:
            assert s in output

def test_first_speech():
    mlas = {'Mr. Luan'}
    input_text, output = get_test_data('first_speech')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values():
        for s in v:
            assert s in output

def test_last_speech():
    mlas = {'Ms Ganley'}
    input_text, output = get_test_data('last_speech')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values():
        for s in v:
            assert s in output

def test_contains_semi_colon(): 
    mlas = {'Ms Sweet'}
    input_text, output = get_test_data('contains_semi_colon')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values():
        for s in v:
            assert s in output

def test_contains_name_of_other_mla(): 
    mlas = {'Mr. Bilous', 'Ms Notley'}
    input_text, output = get_test_data('contains_name_of_other_mla')
    sp = SpeechParser(mlas)
    speeches = sp.parse_speeches(input_text)
    
    for v in speeches.values():
        for s in v:
            assert s in output
