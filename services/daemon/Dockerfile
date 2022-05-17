FROM python:3.10
WORKDIR /usr/src/daemon
COPY . ./
RUN pip install -r requirements.txt
RUN pip install srblib--py3-none-any.whl
ENTRYPOINT ["python", "-m", "daemon"]