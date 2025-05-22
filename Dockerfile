FROM python:    

WORKDIR /app

COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . . 

RUN mkdir -p static
RUN python manage.py collecstatic --noinput || echo 'collectstatic skipped'

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]