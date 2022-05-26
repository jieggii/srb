FROM python:3.10
WORKDIR /usr/src/daemon
COPY . ./
RUN pip install -r requirements.txt
RUN pip install *.whl
ENTRYPOINT ["python", "-m", "daemon"]