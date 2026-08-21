# Saleads Postback Admin

Django-проект для приема и просмотра постбеков Saleads.

## Быстрый старт

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_admin --username admin --password admin
python manage.py runserver
```

Админка Django: `/admin/`, общая статистика: `/`.

## Возможности

- создание отдельной кампании в админке;
- генерация четырех ссылок для кампании: клик, конверсия в обработке, подтвержденная конверсия, отклоненная конверсия;
- прием параметров `clickId`, `conversionId`, `offerId`, `goalId`, `profit`, `sum`, `custom`;
- просмотр общей статистики и статистики по одной кампании;
- экспорт конверсий кампании в JSON и CSV.
