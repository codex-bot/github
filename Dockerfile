FROM python:3.9-slim-buster


WORKDIR /home/github

RUN pip install --upgrade pip
COPY ./requirements.txt /home/github/requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]