#!/usr/bin/env bash
rm -rf decks
./memo.py create deck elements number symbol name
./memo.py create template elements 1 number "Напиши номер элемента <{name}>: "
./memo.py create template elements 2 symbol "Напиши обозначение элемента №{number}: "
./memo.py create template elements 3 name "Напиши название элемента <{symbol}>: "
./memo.py create card elements 1 H Водород
./memo.py create card elements 2 He Гелий
./memo.py create card elements 3 Li Литий
./memo.py create card elements 4 Be Бериллий
./memo.py create card elements 5 B Бор
./memo.py create card elements 6 C Углерод
./memo.py create card elements 7 N Азот
./memo.py create card elements 8 O Кислород
./memo.py create card elements 9 F Фтор
./memo.py create card elements 10 Ne Неон
./memo.py create card elements 11 Na Натрий
./memo.py create card elements 12 Mg Магний
./memo.py create card elements 13 Al Алюминий
./memo.py create card elements 14 Si Кремний
./memo.py create card elements 15 P Фосфор
./memo.py create card elements 16 S Сера
./memo.py create card elements 17 Cl Хлор
./memo.py create card elements 18 Ar Аргон
./memo.py create card elements 19 K Калий
./memo.py create card elements 20 Ca Кальций
./memo.py create card elements 21 Sc Скандий
./memo.py create card elements 22 Ti Титан
./memo.py create card elements 23 V Ванадий
./memo.py create card elements 24 Cr Хром
./memo.py create card elements 25 Mn Марганец
./memo.py create card elements 26 Fe Железо
./memo.py create card elements 27 Co Кобальт
./memo.py create card elements 28 Ni Никель
./memo.py create card elements 29 Cu Медь
./memo.py create card elements 30 Zn Цинк
./memo.py create card elements 31 Ga Галлий
./memo.py create card elements 32 Ge Германий
./memo.py create card elements 33 As Мышьяк
./memo.py create card elements 34 Se Селен
./memo.py create card elements 35 Br Бром
./memo.py create card elements 36 Kr Криптон
./memo.py create card elements 37 Rb Рубидий
./memo.py create card elements 38 Sr Стронций
./memo.py create card elements 39 Y Иттрий
./memo.py create card elements 40 Zr Цирконий
./memo.py create card elements 41 Nb Ниобий
./memo.py create card elements 42 Mo Молибден
./memo.py create card elements 43 Tc Технеций
./memo.py create card elements 44 Ru Рутений
./memo.py create card elements 45 Rh Родий
./memo.py create card elements 46 Pd Палладий
./memo.py create card elements 47 Ag Серебро
./memo.py create card elements 48 Cd Кадмий
./memo.py create card elements 49 In Индий
./memo.py create card elements 50 Sn Олово
./memo.py create card elements 51 Sb Сурьма
./memo.py create card elements 52 Te Теллур
./memo.py create card elements 53 I Иод
./memo.py create card elements 54 Xe Ксенон
./memo.py create card elements 55 Cs Цезий
./memo.py create card elements 56 Ba Барий
./memo.py create card elements 57 La Лантан
./memo.py create card elements 58 Ce Церий
./memo.py create card elements 59 Pr Празеодим
./memo.py create card elements 60 Nd Неодим
./memo.py create card elements 61 Pm Прометий
./memo.py create card elements 62 Sm Самарий
./memo.py create card elements 63 Eu Европий
./memo.py create card elements 64 Gd Гадолиний
./memo.py create card elements 65 Tb Тербий
./memo.py create card elements 66 Dy Диспрозий

./memo.py create deck countries country capital status
./memo.py create template countries 1 country 'В какой стране столица {capital}? ({status}): ' 'В какой стране столица {capital}?: '
./memo.py create template countries 2 capital 'Какая столица в стране {country}? ({status}): ' 'Какая столица в стране {country}?: '
./memo.py create card countries Австрия Вена
./memo.py create card countries Албания Тирана
./memo.py create card countries Андорра Андорра-ла-Велья
./memo.py create card countries "Беларусь|Белоруссия" Минск
./memo.py create card countries Бельгия Брюссель
./memo.py create card countries Болгария София
./memo.py create card countries "Босния и Герцеговина" Сараево
./memo.py create card countries Ватикан Ватикан
./memo.py create card countries Великобритания Лондон
./memo.py create card countries Венгрия Будапешт
./memo.py create card countries Германия Берлин
./memo.py create card countries Греция Афины
./memo.py create card countries Дания Копенгаген
./memo.py create card countries Ирландия Дублин
./memo.py create card countries Исландия Рейкьявик
./memo.py create card countries Испания Мадрид
./memo.py create card countries Италия Рим
./memo.py create card countries Латвия Рига
./memo.py create card countries Литва Вильнюс
./memo.py create card countries Лихтенштейн Вадуц
./memo.py create card countries Люксембург Люксембург
./memo.py create card countries Мальта Валетта
./memo.py create card countries "Молдова|Молдавия" Кишинёв
./memo.py create card countries Монако Монако
./memo.py create card countries "Нидерланды|Голландия" Амстердам де-юре
./memo.py create card countries "Нидерланды|Голландия" Гаага де-факто
./memo.py create card countries Норвегия Осло
./memo.py create card countries Польша Варшава
./memo.py create card countries Португалия Лиссабон
./memo.py create card countries "Россия|РФ" Москва
./memo.py create card countries Румыния Бухарест
./memo.py create card countries Сан-Марино Сан-Марино
./memo.py create card countries Северная Македония Скопье
./memo.py create card countries Сербия Белград
./memo.py create card countries Словакия Братислава
./memo.py create card countries Словения Любляна
./memo.py create card countries Украина Киев
./memo.py create card countries Финляндия Хельсинки
./memo.py create card countries Франция Париж
./memo.py create card countries Хорватия Загреб
./memo.py create card countries Черногория Подгорица главная
./memo.py create card countries Черногория Цетине историческая
./memo.py create card countries Чехия Прага
./memo.py create card countries Швейцария Берн де-факто
./memo.py create card countries Швеция Стокгольм
./memo.py create card countries Эстония Таллин
./memo.py create card countries Азербайджан Баку
./memo.py create card countries Армения Ереван
./memo.py create card countries Афганистан Кабул
./memo.py create card countries Бангладеш Дакка
./memo.py create card countries Бахрейн Манама
./memo.py create card countries Бруней Бандар-Сери-Бегаван
./memo.py create card countries Бутан Тхимпху
./memo.py create card countries "Восточный Тимор" Дили
./memo.py create card countries Вьетнам Ханой
./memo.py create card countries Грузия Тбилиси
./memo.py create card countries Израиль Иерусалим непризнанная
./memo.py create card countries Израиль Тель-Авив признанная
./memo.py create card countries Индия Нью-Дели
./memo.py create card countries Индонезия Нусантара новая
./memo.py create card countries Индонезия Джакарта старая
./memo.py create card countries Иордания Амман
./memo.py create card countries Ирак Багдад
./memo.py create card countries Иран Тегеран
./memo.py create card countries Йемен Сана
./memo.py create card countries Казахстан Астана
./memo.py create card countries Камбоджа Пномпень
./memo.py create card countries Катар Доха
./memo.py create card countries Кипр Никосия
./memo.py create card countries "Киргизия|Кыргызстан" Бишкек
./memo.py create card countries Китай Пекин
./memo.py create card countries КНДР Пхеньян
./memo.py create card countries Кувейт Эль-Кувейт
./memo.py create card countries Лаос Вьентьян
./memo.py create card countries Ливан Бейрут
./memo.py create card countries Малайзия Куала-Лумпур де-юре
./memo.py create card countries Малайзия Путраджая де-факто
./memo.py create card countries Мальдивы Мале
./memo.py create card countries Монголия Улан-Батор
./memo.py create card countries Мьянма Нейпьидо
./memo.py create card countries Непал Катманду
./memo.py create card countries ОАЭ Абу-Даби
./memo.py create card countries Оман Маскат
./memo.py create card countries Пакистан Исламабад
./memo.py create card countries "Саудовская Аравия" Эр-Рияд
./memo.py create card countries Сингапур Сингапур
./memo.py create card countries Сирия Дамаск
./memo.py create card countries Таджикистан Душанбе
./memo.py create card countries Таиланд Бангкок
./memo.py create card countries "Туркменистан|Туркмения" Ашхабад
./memo.py create card countries Турция Анкара
./memo.py create card countries Узбекистан Ташкент
./memo.py create card countries Филиппины Манила
./memo.py create card countries Шри-Ланка Шри-Джаяварденепура-Котте де-юре
./memo.py create card countries Шри-Ланка Коломбо де-факто
./memo.py create card countries "Южная Корея" Сеул
./memo.py create card countries Япония Токио
./memo.py create card countries "Антигуа и Барбуда" Сент-Джонс
./memo.py create card countries Аргентина Буэнос-Айрес
./memo.py create card countries "Багамские Острова" Нассау
./memo.py create card countries Барбадос Бриджтаун
./memo.py create card countries Белиз Бельмопан
./memo.py create card countries Боливия Сукре де-юре
./memo.py create card countries Боливия Ла-Пас де-факто
./memo.py create card countries Бразилия Бразилиа
./memo.py create card countries Венесуэла Каракас
./memo.py create card countries Гаити Порт-о-Пренс
./memo.py create card countries Гайана Джорджтаун
./memo.py create card countries Гватемала Гватемала
./memo.py create card countries Гондурас Тегусигальпа
./memo.py create card countries Гренада Сент-Джорджес
./memo.py create card countries Доминика Розо
./memo.py create card countries "Доминиканская Республика" Санто-Доминго
./memo.py create card countries Канада Оттава
./memo.py create card countries Колумбия Богота
./memo.py create card countries Коста-Рика Сан-Хосе
./memo.py create card countries Куба Гавана
./memo.py create card countries Мексика Мехико
./memo.py create card countries Никарагуа Манагуа
./memo.py create card countries Панама Панама
./memo.py create card countries Парагвай Асунсьон
./memo.py create card countries Перу Лима
./memo.py create card countries Сальвадор Сан-Сальвадор
./memo.py create card countries "Сент-Винсент и Гренадины" Кингстаун
./memo.py create card countries "Сент-Китс и Невис" Бастер
./memo.py create card countries Сент-Люсия Кастри
./memo.py create card countries Суринам Парамарибо
./memo.py create card countries США Вашингтон
./memo.py create card countries "Тринидад и Тобаго" Порт-оф-Спейн
./memo.py create card countries Уругвай Монтевидео
./memo.py create card countries Чили Сантьяго
./memo.py create card countries Эквадор Кито
./memo.py create card countries Ямайка Кингстон
./memo.py create card countries Алжир Алжир
./memo.py create card countries Ангола Луанда
./memo.py create card countries Бенин Порто-Ново де-юре
./memo.py create card countries Бенин Котону де-факто
./memo.py create card countries Ботсвана Габороне
./memo.py create card countries Буркина-Фасо Уагадугу
./memo.py create card countries Бурунди Гитега
./memo.py create card countries Габон Либревиль
./memo.py create card countries Гамбия Банжул
./memo.py create card countries Гана Аккра
./memo.py create card countries Гвинея Конакри
./memo.py create card countries Гвинея-Бисау Бисау
./memo.py create card countries Джибути Джибути
./memo.py create card countries Египет Каир
./memo.py create card countries Замбия Лусака
./memo.py create card countries Зимбабве Хараре
./memo.py create card countries Кабо-Верде Прая
./memo.py create card countries Камерун Яунде
./memo.py create card countries Кения Найроби
./memo.py create card countries Коморы Морони
./memo.py create card countries Конго Браззавиль
./memo.py create card countries "Демократическая Республика Конго" Киншаса
./memo.py create card countries Кот-д-Ивуар Ямусукро де-юре
./memo.py create card countries Кот-д-Ивуар Абиджан де-факто
./memo.py create card countries Лесото Масеру
./memo.py create card countries Либерия Монровия
./memo.py create card countries Ливия Триполи
./memo.py create card countries Маврикий Порт-Луи
./memo.py create card countries Маврикания Нуакшот
./memo.py create card countries Мадагаскар Антананариву
./memo.py create card countries Малави Лилонгве
./memo.py create card countries Мали Бамако
./memo.py create card countries Марокко Рабат
./memo.py create card countries Мозамбик Мапуту
./memo.py create card countries Намибия Виндхук
./memo.py create card countries Нигер Ниамей
./memo.py create card countries Нигерия Абуджа
./memo.py create card countries Руанда Кигали
./memo.py create card countries "Сан-Томе и Принсипи" Сан-Томе
./memo.py create card countries "Сейшельские Острова" Виктория
./memo.py create card countries Сенегал Дакар
./memo.py create card countries Сомали Могадишо
./memo.py create card countries Судан Хартум
./memo.py create card countries Сьерра-Леоне Фритаун
./memo.py create card countries Танзания Додома де-юре
./memo.py create card countries Танзания Дар-эс-Салам де-факто
./memo.py create card countries Того Ломе
./memo.py create card countries Тунис Тунис
./memo.py create card countries Уганда Кампала
./memo.py create card countries ЦАР Банги
./memo.py create card countries Чад Нджамена
./memo.py create card countries Экваториальная Гвинея Малабо
./memo.py create card countries Эритрея Асмэра
./memo.py create card countries Эсватини Мбабане административная
./memo.py create card countries Эсватини Лобамба королевская
./memo.py create card countries Эфиопия Аддис-Абеба
./memo.py create card countries ЮАР Претория административная
./memo.py create card countries ЮАР Кейптаун законодательная
./memo.py create card countries ЮАР Блумфонтейн судебная
./memo.py create card countries "Южный Судан" Джуба
./memo.py create card countries Австралия Канберра
./memo.py create card countries Вануату Порт-Вила
./memo.py create card countries Кирибати "Южная Тарава"
./memo.py create card countries "Маршалловы Острова" Маджуро
./memo.py create card countries Микронезия Паликир
./memo.py create card countries Науру Ярен де-факто
./memo.py create card countries Новая Зеландия Веллингтон
./memo.py create card countries Палау Нгерулмуд
./memo.py create card countries "Папуа-Новая Гвинея" Порт-Морсби
./memo.py create card countries Самоа Апиа
./memo.py create card countries "Соломоновы Острова" Хониара
./memo.py create card countries Тонга Нукуалофа
./memo.py create card countries Тувалу Фунафути
./memo.py create card countries Фиджи Сува

./memo.py create deck months number name days
./memo.py create template months 1 number 'Напиши порядковый номер месяца <{name}>: '
./memo.py create template months 2 name 'Напиши месяц №{number}: '
./memo.py create template months 3 days 'Сколько дней в {name}: '
./memo.py create card months 1 Январь 31
./memo.py create card months 2 Февраль 28
./memo.py create card months 3 Март 31
./memo.py create card months 4 Апрель 30
./memo.py create card months 5 Май 31
./memo.py create card months 6 Июнь 30
./memo.py create card months 7 Июль 31
./memo.py create card months 8 Август 31
./memo.py create card months 9 Сентябрь 30
./memo.py create card months 10 Октябрь 31
./memo.py create card months 11 Ноябрь 30
./memo.py create card months 12 Декабрь 31
# ### февраль, по хорошему, тоже нужно обрабатывать как особый случай

./memo.py create deck math/quaternions expression value
./memo.py create template math/quaternions 1 value '{expression} = '
./memo.py create card math/quaternions -- i^2 -1
./memo.py create card math/quaternions -- ij k
./memo.py create card math/quaternions -- ik -j
./memo.py create card math/quaternions -- ji -k
./memo.py create card math/quaternions -- j^2 -1
./memo.py create card math/quaternions -- jk i
./memo.py create card math/quaternions -- ki j
./memo.py create card math/quaternions -- kj -i
./memo.py create card math/quaternions -- k^2 -1

# кватернионы могут быть отдельной ТРЕНИРОВКОЙ в рамках октанионов?
# видимо пора вводить новую сущность тренировка, это как заранее заданный адхок?
./memo.py create deck math/octonions expression value
./memo.py create template math/octonions 1 value '{expression} = '
./memo.py create card math/octonions -- i^2 -1
./memo.py create card math/octonions -- j^2 -1
./memo.py create card math/octonions -- k^2 -1
./memo.py create card math/octonions -- l^2 -1
./memo.py create card math/octonions -- m^2 -1
./memo.py create card math/octonions -- n^2 -1
./memo.py create card math/octonions -- o^2 -1
./memo.py create card math/octonions -- ij k
./memo.py create card math/octonions -- jk i
./memo.py create card math/octonions -- ki j
./memo.py create card math/octonions -- ji -k
./memo.py create card math/octonions -- kj -i
./memo.py create card math/octonions -- ik -j
./memo.py create card math/octonions -- il m
./memo.py create card math/octonions -- lm i
./memo.py create card math/octonions -- mi l
./memo.py create card math/octonions -- li -m
./memo.py create card math/octonions -- ml -i
./memo.py create card math/octonions -- im -l
./memo.py create card math/octonions -- jl n
./memo.py create card math/octonions -- ln j
./memo.py create card math/octonions -- nj l
./memo.py create card math/octonions -- lj -n
./memo.py create card math/octonions -- nl -j
./memo.py create card math/octonions -- jn -l
./memo.py create card math/octonions -- kl o
./memo.py create card math/octonions -- lo k
./memo.py create card math/octonions -- ok l
./memo.py create card math/octonions -- lk -o
./memo.py create card math/octonions -- ol -k
./memo.py create card math/octonions -- ko -l
./memo.py create card math/octonions -- io n
./memo.py create card math/octonions -- on i
./memo.py create card math/octonions -- ni o
./memo.py create card math/octonions -- oi -n
./memo.py create card math/octonions -- no -i
./memo.py create card math/octonions -- in -o
./memo.py create card math/octonions -- jo m
./memo.py create card math/octonions -- om j
./memo.py create card math/octonions -- mj o
./memo.py create card math/octonions -- oj -m
./memo.py create card math/octonions -- mo -j
./memo.py create card math/octonions -- jm -o
./memo.py create card math/octonions -- kn m
./memo.py create card math/octonions -- nm k
./memo.py create card math/octonions -- mk n
./memo.py create card math/octonions -- nk -m
./memo.py create card math/octonions -- mn -k
./memo.py create card math/octonions -- km -n

./memo.py create deck orthography word pronunciation
./memo.py create template orthography 1 word '[{pronunciation}]: '
./memo.py create card orthography аппроксимация "(а/о)п?р(а/о)кс(и/е)м?ация"
./memo.py create card orthography координаты "к(а/о)?рд(и/е)наты"
./memo.py create card orthography дифференцировать "д(и/е)ф?(и/е)р?(и/е)нцировать"
./memo.py create card orthography абонемент "(а/о)б?н(и/е)мент"
./memo.py create card orthography ажиотаж "(а/о)ж(и/е)(а/о)таж"
./memo.py create card orthography акклиматизация "(а/о)к?л(и/е)м(а/о)т(и/е)зация"
./memo.py create card orthography аккомпанемент "(а/о)к?(а/о)мп(а/о)н(и/е)мент"
./memo.py create card orthography аккорд "(а/о)к?орд"
./memo.py create card orthography аккордеон  "(а/о)к?(а/о)рд(и/е)он"
./memo.py create card orthography аккуратность "(а/о)к?уратность"
./memo.py create card orthography акробатика "(а/о)к?р(а/о)батика"
./memo.py create card orthography аксессуар "(а/о)к?с(и/е)с?уар"
./memo.py create card orthography аллегория "(а/о)л?(и/е)гория"
./memo.py create card orthography единица "ед(и/е)ница"
./memo.py create card orthography трансцендентный "трансце?дентный"
./memo.py create card orthography инцидент "инц(и/е)дент"
./memo.py create card orthography прецедент "пр(и/е)ц(и/е)дент"
./memo.py create card orthography президент "пр(и/е)з(и/е)дент"
