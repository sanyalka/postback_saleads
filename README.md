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

- создание и редактирование кампаний в кастомной панели;
- генерация четырех ссылок для кампании без URL-кодирования токенов `{clickId}`, `{conversionId}`, `{offerId}`, `{goalId}`, `{profit}`, `{sum}`, `{custom}`;
- прием параметров `clickId`, `conversionId`, `offerId`, `goalId`, `profit`, `sum`, `custom`;
- просмотр общей статистики, списка кампаний, журнала событий и статистики по одной кампании в едином кастомном дизайне с графиками;
- экспорт конверсий кампании в JSON и CSV.
