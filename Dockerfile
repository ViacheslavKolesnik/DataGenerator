FROM python:3.7.3-alpine3.9

WORKDIR /app
COPY . /app
RUN python -m pip install -r requirements.txt

CMD ["python", "launcher.py"]
