FROM python:3.10
WORKDIR /usr/src/srblib
COPY . ./
RUN pip install poetry==1.1.13
RUN poetry build --format wheel