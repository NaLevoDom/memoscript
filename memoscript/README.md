# memoscript

CLI-приложение для повторения карточек (spaced repetition) на SQLite.

## Что изменилось в формате колод

Теперь колода хранит поля карточек в JSON, а имена полей задаются при создании колоды.

- `deck`: `card_id`, `fields_json`
- `deck_fields`: `field_position`, `field_name`
- `templates`: `template_id`, `auto_grade`, `answer_field`, `question_form`
- `daily_stats`: статистика за день
- `schedule`: расписание повторений

Индексная логика (`answer_index`, `{1}`, `{2}`) больше не используется.

## Быстрый старт

### 1) Создать колоду

```bash
./create_deck.py months number name days
```

Где:
- `months` — имя колоды
- `number name days` — имена полей карточки

### 2) Добавить карточки

```bash
./add_card.py months 1 Январь 31
./add_card.py months 2 Февраль 28
```

Количество значений должно совпадать с количеством `field_names`.

### 3) Создать template

```bash
./create_template.py months 1 number "Напиши порядковый номер месяца <{name}>: "
```

Аргументы:
- `months` — колода
- `1` — `template_id`
- `number` — `answer_field` (должен существовать в `deck_fields`)
- строка — `question_form` с именованными плейсхолдерами

Пример плейсхолдеров:
- `{card_id}`
- `{number}`
- `{name}`
- `{days}`

### 4) Запуск повторения

```bash
./memo.py months 1
```

Ad-hoc режим:

```bash
./memo.py months 1 -a
./memo.py months 1 -a -i 1-5 8 10
./memo.py months 1 -a -l 3
```

## Обновление

### Обновить карточку

```bash
./update_card.py months -f 12 Декабрь 31
```

Первое значение после `-f` — `card_id`, дальше поля в том же порядке, что в `create_deck.py`.

### Обновить template

```bash
./update_template.py months 1 number "Напиши номер месяца <{name}>: "
```

## Диагностика

```bash
./show_deck.py months
```

Показывает:
- `field_names` (порядок полей колоды)
- карточки колоды
- templates
- schedule по каждому template

## Частые ошибки

- `Expected N fields, got M`
  - в `add_card.py`/`update_card.py` передано не то количество полей;
  - проверь, какие `field_names` были указаны в `create_deck.py`.

- `Unknown field name: ...`
  - в `create_template.py`/`update_template.py` указан `answer_field`, которого нет в колоде;
  - используй имя поля из `field_names` этой колоды.

- `KeyError` в `question_form.format(...)`
  - в шаблоне вопроса используется плейсхолдер, которого нет среди полей;
  - проверь имена в `{...}` и названия `field_names`.

- Падает на старой базе после обновления структуры
  - новый формат использует JSON (`fields_json`) и `deck_fields`;
  - для старых баз без миграции проще пересоздать колоду.

