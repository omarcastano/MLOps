### test stage ##
FROM python:3.9.0-slim AS test_app

# move to working directory
WORKDIR /app

COPY . ./

# install dependences
RUN pip install --upgrade pip && pip install poetry
RUN poetry install
RUN poetry run pytest

### run stage ##
FROM python:3.9.0-slim AS runner

WORKDIR /app

COPY --from=test_app /app/poetry.lock ./
COPY . ./

RUN pip install --upgrade pip && pip install poetry
RUN poetry install --only main

ENV MODEL="cardiffnlp/twitter-roberta-base-sentiment-latest"
EXPOSE 8000

# Run commands on the shell
#CMD ["poetry", "run", "python", "app.py", "--model", "${MODEL}"]
CMD poetry run python src/app.py --model=${MODEL}