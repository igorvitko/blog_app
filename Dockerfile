FROM python:3.8

WORKDIR /blog.app

COPY . .

EXPOSE 5000

ENV FLASK_APP=app_blog.py

RUN pip install -r requirements.txt

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "80"]
