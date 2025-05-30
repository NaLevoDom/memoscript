#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlite3 import connect

dbpath = "asd3.db"
# dbpath = "khjgng.db"

def create_taskperday_db(): # it is done to both of dbs
    with connect(dbpath) as c:
        q = """CREATE TABLE taskperday(
        id TEXT PRIMARY KEY,
        day INT,
        new INT,
        total INT);
        """
        c.execute(q)

def add_record(identif, sym):
    with connect(dbpath) as c:
        db_form = [identif, sym]
        q = f"INSERT INTO deck VALUES(?, ?)"
        c.execute(q, db_form)

def add_record2():
    with connect("asd.db") as c:
        q = f"INSERT INTO taskperday VALUES(1, 739400, 0, 0)"
        c.execute(q)
        q = f"INSERT INTO taskperday VALUES(2, 739400, 0, 0)"
        c.execute(q)
    with connect("khjgng.db") as c:
        q = f"INSERT INTO taskperday VALUES(1, 739400, 0, 0)"
        c.execute(q)

def add_record3():
    with connect("khjgng.db") as c:
        q = f"INSERT INTO taskperday VALUES(2, 739400, 0, 0)"
        c.execute(q)

def create_db(): # / сделано
    with connect(dbpath) as c:
        q = """CREATE TABLE deck(
        id TEXT PRIMARY KEY,
        sym TEXT);
        """
        # column_0, column_1???
        
        c.execute(q)

def drop_qa(): # Элемент в номер / сделано
    with connect("asd.db") as c:
        q = "DROP TABLE qa"
        c.execute(q)
    with connect("khjgng.db") as c:
        q = "DROP TABLE qa"
        c.execute(q)

def create_qa_table(): # done
    with connect("asd.db") as c:
        q = """CREATE TABLE qa(
        mod_id TEXT PRIMARY KEY,
        answer_index INT,
        question TEXT);
        """
        c.execute(q)
    with connect("khjgng.db") as c:
        q = """CREATE TABLE qa(
        mod_id TEXT PRIMARY KEY,
        answer_index INT,
        question TEXT);
        """
        c.execute(q)


def add_qa_records(): # done
    with connect("asd.db") as c:
        q = "INSERT INTO qa VALUES('1', 0, 'Напиши порядковый номер элемента <{1}>: ')"
        c.execute(q)
        q = "INSERT INTO qa VALUES(2, 1, 'Напиши обозначение элемента №{0}: ')"
        c.execute(q)
    with connect("khjgng.db") as c:
        q = "INSERT INTO qa VALUES(1, 0, 'Напиши порядковый номер месяца <{1}>: ')"
        c.execute(q)


def add_qa_records2(): # done
    with connect("khjgng.db") as c:
        q = "INSERT INTO qa VALUES(2, 1, 'Напиши месяц №{0}: ')"
        c.execute(q)






def drop_elements(): # Элемент в номер / сделано
    with connect(dbpath) as c:
        q = "DROP TABLE deck"
        c.execute(q)

def ad_hoc_add(): # / сделано
    elements = [['1', 'H'], ['2', 'He'], ['3', 'Li'], ['4', 'Be'], ['5', 'B'], ['6', 'C'], ['7', 'N'], ['8', 'O'], ['9', 'F'], ['10', 'Ne'], ['11', 'Na'], ['12', 'Mg'], ['13', 'Al'], ['14', 'Si'], ['15', 'P'], ['16', 'S'], ['17', 'Cl'], ['18', 'Ar'], ['19', 'K'], ['20', 'Ca'], ['21', 'Sc'], ['22', 'Ti'], ['23', 'V'], ['24', 'Cr'], ['25', 'Mn'], ['26', 'Fe'], ['27', 'Co'], ['28', 'Ni'], ['29', 'Cu'], ['30', 'Zn'], ['31', 'Ga'], ['32', 'Ge'], ['33', 'As'], ['34', 'Se'], ['35', 'Br'], ['36', 'Kr']]
    for identif, sym in elements:
        add_record(identif, sym)

# ------------------------------------------------


def create_db111():
    with connect("asd3.db") as c:
        q = """CREATE TABLE deck(
        id TEXT PRIMARY KEY,
        sym TEXT);
        """
        # 0страна 1столица
        
        c.execute(q)

def ad_hoc_add111(): # / сделано
    elements = [['Россия', 'Москва'], ['Украина', 'Киев']]
    for identif, sym in elements:
        add_record(identif, sym)


def create_qa_table111(): # done
    with connect("asd3.db") as c:
        q = """CREATE TABLE qa(
        mod_id TEXT PRIMARY KEY,
        answer_index INT,
        question TEXT);
        """
        c.execute(q)

def add_qa_records(): # done
    with connect("asd3.db") as c:
        q = "INSERT INTO qa VALUES('1', 0, 'Какой страны столица {1}? ')"
        c.execute(q)
        q = "INSERT INTO qa VALUES(2, 1, 'Какая столица страны {0}? ')"
        c.execute(q)

def create_taskperday_db111():
    with connect("asd3.db") as c:
        q = """CREATE TABLE taskperday(
        id TEXT PRIMARY KEY,
        day INT,
        new INT,
        total INT);
        """
        c.execute(q)


def add_recordasdasdasdgfddfgdf():
    with connect("asd3.db") as c:
        q = f"INSERT INTO taskperday VALUES(1, 739400, 0, 0)"
        c.execute(q)
        q = f"INSERT INTO taskperday VALUES(2, 739400, 0, 0)"
        c.execute(q)


def ad_hoc_add1112(): # / сделано
    elements = [['Чехия', 'Прага'], ['Словакия', 'Братислава'], ['Австрия', 'Вена'], ['Венгрия', 'Будапешт'], ['Англия', 'Лондон'], ['Уэльс', 'Кардифф'], ['Шотландия', 'Эдинбург'], ['Северная Ирландия', 'Белфаст'], ['Республика Ирландия', 'Дублин'], ['Бельгия', 'Брюссель'], ['Германия', 'Берлин'], ['Лихтенштейн', 'Вадуц'], ['Люксембург', 'Люксембург'], ['Монако', 'Монако'], ['Нидерланды', 'Амстердам'], ['Франция', 'Париж'], ['Швейцария', 'Берн'], ['Беларусь', 'Минск'], ['Болгария', 'София'], ['Молдова', 'Кишинёв'], ['Польша', 'Варшава'], ['Румыния', 'Бухарест'], ['Дания', 'Копенгаген'], ['Исландия', 'Рейкьявик'], ['Латвия', 'Рига'], ['Литва', 'Вильнюс'], ['Эстония', 'Таллин'], ['Норвегия', 'Осло'], ['Финляндия', 'Хельсинки'], ['Швеция', 'Стокгольм'], ['Албания', 'Тирана'], ['Андора', 'Андора-ла-Велья'], ['Босния и Герцеговина', 'Сараево'], ['Ватикан', 'Ватикан'], ['Греция', 'Афины'], ['Испания', 'Мадрид'], ['Италия', 'Рим'], ['Северная Македония', 'Скопье'], ['Мальта', 'Валлетта'], ['Португалия', 'Лиссабон'], ['Сан-Марино', 'Сан-Марино'], ['Косово', 'Приштина'], ['Сербия', 'Белград'], ['Словения', 'Любляна'], ['Хорватия', 'Загреб'], ['Азербайджан', 'Баку'], ['Армения', 'Ереван'], ['Грузия', 'Тбилиси'], ['Казахстан', 'Астана'], ['Кыргызстан', 'Бишкек'], ['Таджикистан', 'Душанбе'], ['Туркменистан', 'Ашхабад'], ['Узбекистан', 'Ташкент'], ['Австралия', 'Камберра'], ['Канада', 'Оттава']]
    for identif, sym in elements:
        add_record(identif, sym)







