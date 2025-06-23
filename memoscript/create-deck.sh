#!/usr/bin/env bash
./create-deck.py elements 3
./add-card.py elements '1' 'H' 'Водород'
./add-card.py elements '2' 'He' 'Гелий'
./add-card.py elements '3' 'Li' 'Литий'
./add-card.py elements '4' 'Be' 'Бериллий'
./add-card.py elements '5' 'B' 'Бор'
./add-card.py elements '6' 'C' 'Углерод'
./add-card.py elements '7' 'N' 'Азот'
./add-card.py elements '8' 'O' 'Кислород'
./add-card.py elements '9' 'F' 'Фтор'
./add-card.py elements '10' 'Ne' 'Неон'
./add-card.py elements '11' 'Na' 'Натрий'
./add-card.py elements '12' 'Mg' 'Магний'
./add-card.py elements '13' 'Al' 'Алюминий'
./add-card.py elements '14' 'Si' 'Кремний'
./add-card.py elements '15' 'P' 'Фосфор'
./add-card.py elements '16' 'S' 'Сера'
./add-card.py elements '17' 'Cl' 'Хлор'
./add-card.py elements '18' 'Ar' 'Аргон'
./add-card.py elements '19' 'K' 'Калий'
./add-card.py elements '20' 'Ca' 'Кальций'
./add-card.py elements '21' 'Sc' 'Скандий'
./add-card.py elements '22' 'Ti' 'Титан'
./add-card.py elements '23' 'V' 'Ванадий'
./add-card.py elements '24' 'Cr' 'Хром'
./add-card.py elements '25' 'Mn' 'Марганец'
./add-card.py elements '26' 'Fe' 'Железо'
./add-card.py elements '27' 'Co' 'Кобальт'
./add-card.py elements '28' 'Ni' 'Никель'
./add-card.py elements '29' 'Cu' 'Медь'
./add-card.py elements '30' 'Zn' 'Цинк'
./add-card.py elements '31' 'Ga' 'Галлий'
./add-card.py elements '32' 'Ge' 'Германий'
./add-card.py elements '33' 'As' 'Мышьяк'
./add-card.py elements '34' 'Se' 'Селен'
./add-card.py elements '35' 'Br' 'Бром'
./add-card.py elements '36' 'Kr' 'Криптон'
./create-mod.py elements 1 1 "Напиши номер элемента <{2}>: "
./create-mod.py elements 2 2 "Напиши обозначение элемента №{1}: "
./create-mod.py elements 3 3 "Напиши название элемента <{2}>: "

./create-deck.py capitals 2
./add-card.py capitals Россия Москва
./add-card.py capitals Украина Киев
./add-card.py capitals Чехия Прага
./add-card.py capitals Словакия Братислава
./add-card.py capitals Австрия Вена
./add-card.py capitals Венгрия Будапешт
./add-card.py capitals Англия Лондон
./add-card.py capitals Уэльс Кардифф
./add-card.py capitals Шотландия Эдинбург
./add-card.py capitals 'Северная Ирландия' Белфаст
./add-card.py capitals 'Республика Ирландия' Дублин
./add-card.py capitals Бельгия Брюссель
./add-card.py capitals Германия Берлин
./add-card.py capitals Лихтенштейн Вадуц
./add-card.py capitals Люксембург Люксембург
./add-card.py capitals Монако Монако
./add-card.py capitals Нидерланды Амстердам
./add-card.py capitals Франция Париж
./add-card.py capitals Швейцария Берн
./add-card.py capitals Беларусь Минск
./add-card.py capitals Болгария София
./add-card.py capitals Молдова Кишинёв
./add-card.py capitals Румыния Бухарест
./add-card.py capitals Дания Копенгаген
./add-card.py capitals Исландия Рейкьявик
./add-card.py capitals Латвия Рига
./add-card.py capitals Литва Вильнюс
./add-card.py capitals Эстония Таллин
./add-card.py capitals Норвегия Осло
./add-card.py capitals Финляндия Хельсинки
./add-card.py capitals Швеция Стокгольм
./add-card.py capitals Албания Тирана
./add-card.py capitals Андора Андора-ла-Велья
./add-card.py capitals 'Босния и Герцеговина' Сараево
./add-card.py capitals Греция Афины
./add-card.py capitals Испания Мадрид
./add-card.py capitals Италия Рим
./add-card.py capitals 'Северная Македония' Скопье
./add-card.py capitals Мальта Валлетта
./add-card.py capitals Португалия Лиссабон
./add-card.py capitals Сан-Марино Сан-Марино
./add-card.py capitals Косово Приштина
./add-card.py capitals Сербия Белград
./add-card.py capitals Словения Любляна
./add-card.py capitals Хорватия Загреб

./add-card.py capitals Канада Оттава
./add-card.py capitals Австралия Камберра

./add-card.py capitals Азербайджан Баку
./add-card.py capitals Армения Ереван
./add-card.py capitals Грузия Тбилиси
./add-card.py capitals Казахстан Астана
./add-card.py capitals Кыргызстан Бишкек
./add-card.py capitals Таджикистан Душанбе
./add-card.py capitals Туркменистан Ашхабад
./add-card.py capitals Узбекистан Ташкент

./add-card.py capitals Иран Тегеран
./add-card.py capitals 'Саудовская Аравия' Эр-Рияд
./add-card.py capitals Афганистан Кабул
./add-card.py capitals Израиль Иерусалим
./add-card.py capitals Сирия Дамаск
./add-card.py capitals Ирак Багдад

./create-mod.py capitals 1 1 'Какой страны столица {2}?: '
./create-mod.py capitals 2 2 'Какой страны столица {1}?: '

./create-deck.py months 3
./add-card.py months 1 Январь 31
./add-card.py months 2 Февраль 28
./add-card.py months 3 Март 31
./add-card.py months 4 Апрель 30
./add-card.py months 5 Май 31
./add-card.py months 6 Июнь 30
./add-card.py months 7 Июль 31
./add-card.py months 8 Август 31
./add-card.py months 9 Сентябрь 30
./add-card.py months 10 Октябрь 31
./add-card.py months 11 Ноябрь 30
./add-card.py months 12 Декабрь 31

./create-mod.py months 1 1 'Напиши порядковый номер месяца <{2}>: '
./create-mod.py months 2 2 'Напиши месяц №{1}: '
./create-mod.py months 3 3 'Сколько дней в {2}: '


