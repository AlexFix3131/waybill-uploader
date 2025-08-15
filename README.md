
# Waybill PDF → Excel (GitHub/Vercel вариант)

Два простых пути:

## Вариант A — GitHub Actions (без собственного сервера)
1. Создайте приватный репозиторий и включите **Actions** и **Pages**.
2. Загружайте PDF (или CSV из PDF) в папку `/uploads` через интерфейс GitHub.
3. Workflow обработает файл и положит Excel в `/output`. Страницу скачивания можно раздавать через Pages.

## Вариант B — Небольшой сайт на Vercel (кнопка Upload)
1. Импортируйте этот репозиторий в Vercel (Free).
2. В `api/upload` добавьте обработчик (Node + formidable) для приёма PDF.
3. Вызовите `process_invoice.py` (см. `requirements.txt`) и верните ссылку на скачивание.

### Правила извлечения
- Колонки: `MPN | Replacem | Quantity | Totalsprice | Order reference`.
- `Replacem` всегда пустой.
- Ничего не пересчитывать: `Totalsprice` брать из **Summa**, `Cena` игнорировать.
- `Order reference` — построчно: если есть отдельная колонка — берём её; иначе копируем номер из маркера `#123456` на каждую строку блока.
