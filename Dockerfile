FROM python:3.11.4-slim-buster

WORKDIR /app

COPY . .

RUN apt-get update \
  && apt-get install -y \
    --no-install-recommends \
    --no-install-suggests \
    curl gcc g++ gnupg unixodbc-dev \
    unixodbc-dev \
    libgssapi-krb5-2 && \
    apt-get autoclean && \
    apt-get autoremove && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip install --no-cache-dir --force -r requirements.txt

CMD [ "python", "-Bu", "main.py" ]