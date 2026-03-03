#!/usr/bin/env bash
./create_deck.py elements 3
./add_card.py elements '1' 'H' 'Водород'
./add_card.py elements '2' 'He' 'Гелий'
./add_card.py elements '3' 'Li' 'Литий'
./add_card.py elements '4' 'Be' 'Бериллий'
./add_card.py elements '5' 'B' 'Бор'
./add_card.py elements '6' 'C' 'Углерод'
./add_card.py elements '7' 'N' 'Азот'
./add_card.py elements '8' 'O' 'Кислород'
./add_card.py elements '9' 'F' 'Фтор'
./add_card.py elements '10' 'Ne' 'Неон'
./add_card.py elements '11' 'Na' 'Натрий'
./add_card.py elements '12' 'Mg' 'Магний'
./add_card.py elements '13' 'Al' 'Алюминий'
./add_card.py elements '14' 'Si' 'Кремний'
./add_card.py elements '15' 'P' 'Фосфор'
./add_card.py elements '16' 'S' 'Сера'
./add_card.py elements '17' 'Cl' 'Хлор'
./add_card.py elements '18' 'Ar' 'Аргон'
./add_card.py elements '19' 'K' 'Калий'
./add_card.py elements '20' 'Ca' 'Кальций'
./add_card.py elements '21' 'Sc' 'Скандий'
./add_card.py elements '22' 'Ti' 'Титан'
./add_card.py elements '23' 'V' 'Ванадий'
./add_card.py elements '24' 'Cr' 'Хром'
./add_card.py elements '25' 'Mn' 'Марганец'
./add_card.py elements '26' 'Fe' 'Железо'
./add_card.py elements '27' 'Co' 'Кобальт'
./add_card.py elements '28' 'Ni' 'Никель'
./add_card.py elements '29' 'Cu' 'Медь'
./add_card.py elements '30' 'Zn' 'Цинк'
./add_card.py elements '31' 'Ga' 'Галлий'
./add_card.py elements '32' 'Ge' 'Германий'
./add_card.py elements '33' 'As' 'Мышьяк'
./add_card.py elements '34' 'Se' 'Селен'
./add_card.py elements '35' 'Br' 'Бром'
./add_card.py elements '36' 'Kr' 'Криптон'
./create_mod.py elements 1 1 "Напиши номер элемента <{2}>: "
./create_mod.py elements 2 2 "Напиши обозначение элемента №{1}: "
./create_mod.py elements 3 3 "Напиши название элемента <{2}>: "

./create_deck.py capitals 2
./add_card.py capitals Россия Москва
./add_card.py capitals Украина Киев
./add_card.py capitals Чехия Прага
./add_card.py capitals Словакия Братислава
./add_card.py capitals Австрия Вена
./add_card.py capitals Венгрия Будапешт
./add_card.py capitals Великобритания Лондон
./add_card.py capitals Ирландия Дублин
./add_card.py capitals Бельгия Брюссель
./add_card.py capitals Германия Берлин
./add_card.py capitals Лихтенштейн Вадуц
./add_card.py capitals Люксембург Люксембург
./add_card.py capitals Монако Монако
./add_card.py capitals Нидерланды Амстердам
./add_card.py capitals Франция Париж
./add_card.py capitals Швейцария Берн
./add_card.py capitals Беларусь Минск
./add_card.py capitals Болгария София
./add_card.py capitals Молдова Кишинёв
./add_card.py capitals Румыния Бухарест
./add_card.py capitals Дания Копенгаген
./add_card.py capitals Исландия Рейкьявик
./add_card.py capitals Латвия Рига
./add_card.py capitals Литва Вильнюс
./add_card.py capitals Эстония Таллин
./add_card.py capitals Норвегия Осло
./add_card.py capitals Финляндия Хельсинки
./add_card.py capitals Швеция Стокгольм
./add_card.py capitals Албания Тирана
./add_card.py capitals Андора Андора-ла-Велья
./add_card.py capitals 'Босния и Герцеговина' Сараево
./add_card.py capitals Греция Афины
./add_card.py capitals Испания Мадрид
./add_card.py capitals Италия Рим
./add_card.py capitals 'Северная Македония' Скопье
./add_card.py capitals Мальта Валлетта
./add_card.py capitals Португалия Лиссабон
./add_card.py capitals Сан-Марино Сан-Марино
./add_card.py capitals Косово Приштина
./add_card.py capitals Сербия Белград
./add_card.py capitals Словения Любляна
./add_card.py capitals Хорватия Загреб

./add_card.py capitals Канада Оттава
./add_card.py capitals Австралия Камберра

./add_card.py capitals Азербайджан Баку
./add_card.py capitals Армения Ереван
./add_card.py capitals Грузия Тбилиси
./add_card.py capitals Казахстан Астана
./add_card.py capitals Кыргызстан Бишкек
./add_card.py capitals Таджикистан Душанбе
./add_card.py capitals Туркменистан Ашхабад
./add_card.py capitals Узбекистан Ташкент

./add_card.py capitals Иран Тегеран
./add_card.py capitals 'Саудовская Аравия' Эр-Рияд
./add_card.py capitals Афганистан Кабул
./add_card.py capitals Израиль Иерусалим
./add_card.py capitals Сирия Дамаск
./add_card.py capitals Ирак Багдад

./create_mod.py capitals 1 1 'Какой страны столица {2}?: '
./create_mod.py capitals 2 2 'Какой страны столица {1}?: '

./create_deck.py months 3
./add_card.py months 1 Январь 31
./add_card.py months 2 Февраль 28
./add_card.py months 3 Март 31
./add_card.py months 4 Апрель 30
./add_card.py months 5 Май 31
./add_card.py months 6 Июнь 30
./add_card.py months 7 Июль 31
./add_card.py months 8 Август 31
./add_card.py months 9 Сентябрь 30
./add_card.py months 10 Октябрь 31
./add_card.py months 11 Ноябрь 30
./add_card.py months 12 Декабрь 31

./create_mod.py months 1 1 'Напиши порядковый номер месяца <{2}>: '
./create_mod.py months 2 2 'Напиши месяц №{1}: '
./create_mod.py months 3 3 'Сколько дней в {2}: '


./add_card.py elements 37 Rb Рубидий
./add_card.py elements 38 Sr Стронций
./add_card.py elements 39 Y Иттрий
./add_card.py elements 40 Zr Цирконий
./add_card.py elements 41 Nb Ниобий
./add_card.py elements 42 Mo Молибден
./add_card.py elements 43 Tc Технеций
./add_card.py elements 44 Ru Рутений
./add_card.py elements 45 Rh Родий
./add_card.py elements 46 Pd Палладий
./add_card.py elements 47 Ag Серебро
./add_card.py elements 48 Cd Кадмий
./add_card.py elements 49 In Индий
./add_card.py elements 50 Sn Олово
./add_card.py elements 51 Sb Сурьма
./add_card.py elements 52 Te Теллур
./add_card.py elements 53 I Иод
./add_card.py elements 54 Xe Ксенон

./add_card.py capitals Турция Анкара
./add_card.py capitals Кипр Никосия
./add_card.py capitals Йемен Сана
./add_card.py capitals Оман Маскат
./add_card.py capitals Ливан Бейрут
./add_card.py capitals Иордания Амман
./add_card.py capitals Кувейт Эль-Кувейт
./add_card.py capitals Бахрейн Манама
./add_card.py capitals Катар Доха
./add_card.py capitals ОАЭ Абу-Даби
./add_card.py capitals Пакистан Исламабад
./add_card.py capitals Индия Нью-Дели
./add_card.py capitals Непал Катманду
./add_card.py capitals Китай Пекин
./add_card.py capitals Монголия Улан-Батор
./add_card.py capitals Бутан Тхимпху
./add_card.py capitals Бангладеш Дакка
./add_card.py capitals Мьянма Нейпьидо
./add_card.py capitals Таиланд Бангкок
./add_card.py capitals Камбоджа "Пном Пен"
./add_card.py capitals Лаос Вьентьян
./add_card.py capitals Вьетнам Ханой
./add_card.py capitals "Южная Корея" Сеул 
./add_card.py capitals "Северная Корея" Пхеньян
./add_card.py capitals Япония Токио
./add_card.py capitals Тайвань Тайбэй
./add_card.py capitals Филиппины Манила
./add_card.py capitals Малайзия Куала-Лумпур
./add_card.py capitals Индонезия Джакарта
./add_card.py capitals Сингапур Сингапур
./add_card.py capitals "Папуа-Новая Гвинея" Порт-Морсби
./add_card.py capitals "Соломоновы острова" Хониара
./add_card.py capitals "Новая Зеландия" Веллингтон

./add_card.py capitals США Вашингтон
./add_card.py capitals Мексика Мехико
./add_card.py capitals Гватемала Гватемала
./add_card.py capitals Белиз Бельмопан
./add_card.py capitals Сальвадор Сан-Сальвадор
./add_card.py capitals Гондурас Тегусигальпа
./add_card.py capitals Никарагуа Манагуа
./add_card.py capitals Коста-Рика Сан-Хосе
./add_card.py capitals Панама Панама
./add_card.py capitals Куба Гавана
./add_card.py capitals "Доминиканская Республика" Санто-Доминго
./add_card.py capitals Багамы Нассау
./add_card.py capitals "Острова Теркс и Кайкос" Коберн-Таун
./add_card.py capitals Пуэрто-Рико Сан-Хуан
./add_card.py capitals "Британские Виргинские Острова" Род-Таун
./add_card.py capitals "Американские Виргинские Острова" Шарлотта-Амалия
./add_card.py capitals Ангилья Валли
./add_card.py capitals "Антигуа и Барбуда" Сент-Джонс
./add_card.py capitals Гваделупа Бас-Тер
./add_card.py capitals Доминика Розо
./add_card.py capitals Мартиника Фор-де-Франс
./add_card.py capitals Сент-Люсия Кастри
./add_card.py capitals "Сент-Винсент и Гренадины" Кингстаун
./add_card.py capitals Барбадос Бриджтаун
./add_card.py capitals Гренада Сент-Джорджес
./add_card.py capitals "Тринидад и Тобаго" Порт-оф-Спейн
./add_card.py capitals Аруба Ораньестад
./add_card.py capitals Кюрасао Виллемстад

./add_card.py elements 55 Cs Цезий
./add_card.py elements 56 Ba Барий
./add_card.py elements 57 La Лантан
./add_card.py elements 58 Ce Церий
./add_card.py elements 59 Pr Празеодим
./add_card.py elements 60 Nd Неодим

./add_card.py elements 61 Pm Прометий
./add_card.py elements 62 Sm Самарий
./add_card.py elements 63 Eu Европий
./add_card.py elements 64 Gd Гадолиний
./add_card.py elements 65 Tb Тербий
./add_card.py elements 66 Dy Диспрозий

./add_card.py capitals Венесуэла Каракас
./add_card.py capitals Колумбия Богота
./add_card.py capitals Эквадор Кито
./add_card.py capitals Перу Лима
./add_card.py capitals Бразилия Бразилиа
./add_card.py capitals Гайана Джорджтаун
./add_card.py capitals Суринам Парамарибо
./add_card.py capitals Боливия Сукре
./add_card.py capitals Парагвай Асунсьон
./add_card.py capitals Чили Сантьяго
./add_card.py capitals Уругвай Монтевидео
./add_card.py capitals Аргентина Буэнос‑Айрес
