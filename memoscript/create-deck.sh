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


./add-card.py elements 37 Rb Рубидий
./add-card.py elements 38 Sr Стронций
./add-card.py elements 39 Y Иттрий
./add-card.py elements 40 Zr Цирконий
./add-card.py elements 41 Nb Ниобий
./add-card.py elements 42 Mo Молибден
./add-card.py elements 43 Tc Технеций
./add-card.py elements 44 Ru Рутений
./add-card.py elements 45 Rh Родий
./add-card.py elements 46 Pd Палладий
./add-card.py elements 47 Ag Серебро
./add-card.py elements 48 Cd Кадмий
./add-card.py elements 49 In Индий
./add-card.py elements 50 Sn Олово
./add-card.py elements 51 Sb Сурьма
./add-card.py elements 52 Te Теллур
./add-card.py elements 53 I Иод
./add-card.py elements 54 Xe Ксенон

./add-card.py capitals Турция Анкара
./add-card.py capitals Кипр Никосия
./add-card.py capitals Йемен Сана
./add-card.py capitals Оман Маскат
./add-card.py capitals Ливан Бейрут
./add-card.py capitals Иордания Амман
./add-card.py capitals Кувейт Эль-Кувейт
./add-card.py capitals Бахрейн Манама
./add-card.py capitals Катар Доха
./add-card.py capitals ОАЭ Абу-Даби
./add-card.py capitals Пакистан Исламабад
./add-card.py capitals Индия Нью-Дели
./add-card.py capitals Непал Катманду
./add-card.py capitals Китай Пекин
./add-card.py capitals Монголия Улан-Батор
./add-card.py capitals Бутан Тхимпху
./add-card.py capitals Бангладеш Дакка
./add-card.py capitals Мьянма Нейпьидо
./add-card.py capitals Таиланд Бангкок
./add-card.py capitals Камбоджа "Пном Пен"
./add-card.py capitals Лаос Вьентьян
./add-card.py capitals Вьетнам Ханой
./add-card.py capitals "Южная Корея" Сеул 
./add-card.py capitals "Северная Корея" Пхеньян
./add-card.py capitals Япония Токио
./add-card.py capitals Тайвань Тайбэй
./add-card.py capitals Филиппины Манила
./add-card.py capitals Малайзия Куала-Лумпур
./add-card.py capitals Индонезия Джакарта
./add-card.py capitals Сингапур Сингапур
./add-card.py capitals "Папуа-Новая Гвинея" Порт-Морсби
./add-card.py capitals "Соломоновы острова" Хониара
./add-card.py capitals "Новая Зеландия" Веллингтон

./add-card.py capitals США Вашингтон
./add-card.py capitals Мексика Мехико
./add-card.py capitals Гватемала Гватемала
./add-card.py capitals Белиз Бельмопан
./add-card.py capitals Сальвадор Сан-Сальвадор
./add-card.py capitals Гондурас Тегусигальпа
./add-card.py capitals Никарагуа Манагуа
./add-card.py capitals Коста-Рика Сан-Хосе
./add-card.py capitals Панама Панама
./add-card.py capitals Куба Гавана
./add-card.py capitals "Доминиканская Республика" Санто-Доминго
./add-card.py capitals Багамы Нассау
./add-card.py capitals "Острова Теркс и Кайкос" Коберн-Таун
./add-card.py capitals Пуэрто-Рико Сан-Хуан
./add-card.py capitals "Британские Виргинские Острова" Род-Таун
./add-card.py capitals "Американские Виргинские Острова" Шарлотта-Амалия
./add-card.py capitals Ангилья Валли
./add-card.py capitals "Антигуа и Барбуда" Сент-Джонс
./add-card.py capitals Гваделупа Бас-Тер
./add-card.py capitals Доминика Розо
./add-card.py capitals Мартиника Фор-де-Франс
./add-card.py capitals Сент-Люсия Кастри
./add-card.py capitals "Сент-Винсент и Гренадины" Кингстаун
./add-card.py capitals Барбадос Бриджтаун
./add-card.py capitals Гренада Сент-Джорджес
./add-card.py capitals "Тринидад и Тобаго" Порт-оф-Спейн
./add-card.py capitals Аруба Ораньестад
./add-card.py capitals Кюрасао Виллемстад

./add-card.py elements 55 Cs Цезий
./add-card.py elements 56 Ba Барий
./add-card.py elements 57 La Лантан
./add-card.py elements 58 Ce Церий
./add-card.py elements 59 Pr Празеодим
./add-card.py elements 60 Nd Неодим

./add-card.py elements 61 Pm Прометий
./add-card.py elements 62 Sm Самарий
./add-card.py elements 63 Eu Европий
./add-card.py elements 64 Gd Гадолиний
./add-card.py elements 65 Tb Тербий
./add-card.py elements 66 Dy Диспрозий

./add-card.py capitals Венесуэла Каракас
./add-card.py capitals Колумбия Богота
./add-card.py capitals Эквадор Кито
./add-card.py capitals Перу Лима
./add-card.py capitals Бразилия Бразилиа
./add-card.py capitals Гайана Джорджтаун
./add-card.py capitals Суринам Парамарибо
./add-card.py capitals Боливия Сукре
./add-card.py capitals Парагвай Асунсьон
./add-card.py capitals Чили Сантьяго
./add-card.py capitals Уругвай Монтевидео
./add-card.py capitals Аргентина Буэнос‑Айрес
