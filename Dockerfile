FROM python:3.13 AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update && apt-get install -y gettext
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

FROM builder AS final
RUN apt-get update && apt-get install -y gettext
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]