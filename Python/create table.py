import sqlite3

ru_html = \
    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"> \
    <html><body style="font-size:13pt; font-weight:400; font-style:normal;"> \
    <p align="center"style="margin-top:0px;margin-bottom:0px;margin-left:0px;margin-right:0px;-qt-block-indent:0;text-indent:0px;"><span style="font-size:12pt;">Как пользоваться программой:</span></p> \
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt;">[в процессе...]</span></p></body></html>'

en_html = \
    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"> \
    <html><body style="font-size:13pt; font-weight:400; font-style:normal;"> \
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt;">How to use this program:</span></p> \
    <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt;">[in procces...]</span></p></body></html>'

ru_error = 'неправильные числа'
en_error = 'incorrect input numbers'
ru_error_parallel = '(лучи параллельны)'
en_error_parallel = '(the beams are parallel)'
ru_error_intersection = '(лучи не пересекаются)'
en_error_intersection = '(the beams don\'t intersect)'

with sqlite3.connect('database.db') as db:
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS language (name TEXT, Русский TEXT, English TEXT)''')
    query = """ INSERT INTO language (name, Русский, English) VALUES ('label_auto_mode', 'Авто мод', 'Auto mode') """
    query2 = """ INSERT INTO language (name, Русский, English) VALUES ('hotkey1', 'Горячая клавиша 1-ого броска', 'Hotkey for first trow') """
    query3 = """ INSERT INTO language (name, Русский, English) VALUES ('hotkey2', 'Горячая клавиша 2-ого броска', 'Hotkey for second trow') """
    query4 = """ INSERT INTO language (name, Русский, English) VALUES ('label_language', 'Язык', 'Language') """
    query5 = """ INSERT INTO language (name, Русский, English) VALUES ('first_eye', '1-ый глаз эндера', '1-st eye of ender') """
    query6 = """ INSERT INTO language (name, Русский, English) VALUES ('second_eye', '2-ой глаз эндера', '2-nd eye of ender') """
    query7 = """ INSERT INTO language (name, Русский, English) VALUES ('label_coordinates', 'Координаты портала', 'Portal coordinates') """
    query8 = """ INSERT INTO language (name, Русский, English) VALUES ('btn_command', 'Скопировать команду с координатами', 'Copy command with coordinates') """
    query9 = """ INSERT INTO language (name, Русский, English) VALUES ('checkBox', 'Авто мод', 'Auto mode') """
    query10 = """ INSERT INTO language (name, Русский, English) VALUES ('tabWidget', 'Поиск', 'Finder') """
    query11 = """ INSERT INTO language (name, Русский, English) VALUES ('tabWidget2', 'Настройки', 'Settings') """
    query12 = """ INSERT INTO language (name, Русский, English) VALUES ('alpha', 'угол:', 'angle:') """
    query13 = """ INSERT INTO language (name, Русский, English) VALUES ('beta', 'угол:', 'angle:') """
    query14 = f""" INSERT INTO language (name, Русский, English) VALUES ('textBrowser', '{ru_html}', '{en_html}') """
    query15 = f""" INSERT INTO language (name, Русский, English) VALUES ('error', '{ru_error}', '{en_error}') """
    query16 = f""" INSERT INTO language (name, Русский, English) VALUES ('error_parallel', '{ru_error_parallel}', '{en_error_parallel}') """
    query17 = f""" INSERT INTO language (name, Русский, English) VALUES ('error_intersection', '{ru_error_intersection}', '{en_error_intersection}') """

    cursor.execute(query)
    cursor.execute(query2)
    cursor.execute(query3)
    cursor.execute(query4)
    cursor.execute(query5)
    cursor.execute(query6)
    cursor.execute(query7)
    cursor.execute(query8)
    cursor.execute(query9)
    cursor.execute(query10)
    cursor.execute(query11)
    cursor.execute(query12)
    cursor.execute(query13)
    cursor.execute(query14)
    cursor.execute(query15)
    cursor.execute(query16)
    cursor.execute(query17)
    db.commit()
