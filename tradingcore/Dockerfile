FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD python manage.py migrate && python manage.py createsuperuser ==noinput || true && daphne -b 0.0.0.0 -p 8000 tradingcore.asgi:application