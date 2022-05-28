FROM python:3.10
WORKDIR /usr/src/daemon
ENV SRBLIB_WHEEL=srblib-0.1.0-py3-none-any.whl

COPY daemon ./daemon/
COPY pyproject.toml ./

COPY --from=srb-srblib /usr/src/srblib/dist/$SRBLIB_WHEEL ./

RUN sed -i '/srblib/d' pyproject.toml

RUN pip install poetry==1.1.13
RUN poetry config virtualenvs.create false

RUN poetry add ./$SRBLIB_WHEEL
RUN poetry install

ENTRYPOINT ["python", "-m", "daemon"]