import requests
import glob
import os

def detect_lang(text):
    api_key = 'trnsl.1.1.20170202T191956Z.8cacb24d8fd29d5f.606419810f6562e33d7dee93e3d054ea8bc1efe0'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    specs = dict(key=api_key,text=text)
    response = requests.get(url, specs).json()
    return(response['lang'])

def translate(text, target_lang = 'ru'):
    api_key = 'trnsl.1.1.20170202T191956Z.8cacb24d8fd29d5f.606419810f6562e33d7dee93e3d054ea8bc1efe0'
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    lang = '-'.join([str(detect_lang(text)), target_lang])
    specs = dict(key=api_key, text=text, lang=lang)
    response = requests.get(url, specs).json()
    return (response['text'])

def find_files():
    files = glob.glob('*.txt')
    return (files)

def create_result_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def write_results(file_name):
    with open(file_name, 'r') as initial_file:
        translated = '\n'.join(translate(initial_file.read()))

    target_folder = 'results'
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    target_file = os.path.join(target_folder, file_name)

    with open(target_file, 'w', encoding='UTF-8') as result_file:
        result_file.write(translated)

files = find_files()
for each in files:
    write_results(each)


