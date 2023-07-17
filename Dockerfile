FROM python:3.10.4-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Create and switch to a new user

RUN useradd --create-home etl
USER etl
WORKDIR /home/etl

FROM base AS python-deps

# Install pipenv and compilation dependencies
USER root
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev vim
RUN pip3 install pipenv==v2022.4.20

# Install python dependencies in /home/etl/.venv
COPY Pipfile .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps --chown=etl:etl /home/etl/.venv /.venv
ENV PATH="/.venv/bin:$PATH"
