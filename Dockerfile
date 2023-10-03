FROM python:3.11.5-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install postgres dependecy
RUN apt update && apt install libpq-dev gcc -y

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

EXPOSE 80

CMD [ "python3", "main.py" ]