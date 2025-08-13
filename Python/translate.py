# pip install googletrans==4.0.0rc1
# pip install googletrans==3.1.0a0

import sqlite3
import googletrans
from googletrans import Translator

language_list = [value for value in (googletrans.LANGUAGES.values())]
language_list.remove('hebrew')
language_list.remove('frisian')
language_list.remove('uyghur')
language_list.remove('xhosa')
language_list.remove('yoruba')
language_list.remove('russian')

translator = Translator()
# for i in range(69):
#     language_list.pop(0)


def create():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        for NAME in language_list:
            NAME = f"'{NAME}'"
            query = f""" ALTER TABLE language ADD COLUMN {NAME} TEXT"""
            cursor.execute(query)


def translate(name, language):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        translation = cursor.execute(f""" SELECT "{language}" FROM language WHERE name == '{name}' """).fetchone()[0]
        return translation


def main_list():
    main_list = list()
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        translation = cursor.execute(f""" SELECT Main FROM language""").fetchall()
        main_tuple = list(translation)
        for name in main_tuple:
            name = str(name)[2:-3]
            main_list.append(name)
        return main_list


cur_list = main_list()
# print(language_list)
print(cur_list)
# for i in cur_list:
#     if i == '':
#         cur_list.remove(i)
# print(cur_list)

# create()

# for lang in language_list:
#     for name in cur_list:
#         print(lang)
#         with sqlite3.connect('database.db') as db:
#             cursor = db.cursor()
#             query = f""" UPDATE language SET "{lang}" = "{translator.translate(name, dest=lang).text}" WHERE Main = "{name}" """
#             cursor.execute(query)


for lang in language_list:
    print(lang)
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = f""" UPDATE language SET "{lang}" = "{translator.translate('Personalisation', dest=lang).text}" WHERE name = "Label_mode" """
        cursor.execute(query)


# with sqlite3.connect('database.db') as db:
#     cursor = db.cursor()
#     query = f""" UPDATE language SET "afrikaans" = "afrikaans" WHERE name = "language" """
#     cursor.execute(query)

# with sqlite3.connect('database.db') as db:
#     cursor = db.cursor()
#     query = f""" UPDATE language SET chinese (simplified) = "{translator.translate(name, dest=lang).text}" WHERE Main = "{name}" """
#     cursor.execute(query)


# print(googletrans.LANGUAGES)
# print(translator.translate(text1, dest='afrikaans').text)
# print(translator.translate('chinese (simplified)', dest='chinese (simplified)').text)

# with sqlite3.connect('database.db') as db:
#     cursor = db.cursor()
#     translation = cursor.execute(f""" SELECT chinese(simplified) FROM language WHERE name == 'alpha' """).fetchone()[0]
#     print(translation)
