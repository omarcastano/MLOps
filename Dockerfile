### run stage ##
FROM python:3.9.0-slim AS runner

WORKDIR /python_app

COPY . ./

RUN pip install --upgrade pip && pip install poetry
RUN poetry install

ENV DATASET="titanic"
ENV NUM_INPUT_FEATURES="age"
ENV CAT_INPUT_FEATURES="class"
ENV TARGET_VAR="survived"
EXPOSE 8000

# Run commands on the shell
#CMD ["poetry", "run", "python", "app.py", "--model", "${MODEL}"]
CMD poetry run pytest && \
    poetry run python src/app/app.py --dataset=${DATASET} --num_input_features=${NUM_INPUT_FEATURES} \
    --cat_input_features=${CAT_INPUT_FEATURES} --target_var=${TARGET_VAR}