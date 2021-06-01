FROM python:3.9.5-alpine

RUN pip install pipenv

WORKDIR /app

ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV MYSQL_USER root
ENV MYSQL_HOST db

COPY Pipfile* .

RUN pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r requirements.txt

# RUN pip install pipenv && \
#     pipenv install --dev --system --deploy --ignore-pipfile

ADD . .

RUN pip install .

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]