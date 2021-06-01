FROM python:3.9.5-slim

RUN pip install pipenv

WORKDIR /app

ENV FLASK_APP app
ENV FLASK_ENV development

ENV MYSQL_HOST db_dev
ENV MYSQL_USER=root
ENV MYSQL_DB=bookmark
ENV MYSQL_PORT=3307 

COPY Pipfile* .

RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt

ADD . .

RUN pip install .

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]