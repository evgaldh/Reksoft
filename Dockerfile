FROM python:slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:slim

EXPOSE 8000

WORKDIR /app/

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./migrations /app/migrations

COPY ./resourceapp /app/resourceapp

CMD ["waitress-serve", "--port=8000", "--host=0.0.0.0", "resourceapp.app:application"]