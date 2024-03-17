
FROM python:3.10-alpine as web
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=0
COPY ./app .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run"]