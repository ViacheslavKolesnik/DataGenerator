FROM python:3.7.3-alpine3.9

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN python -m pip install -r requirements.txt

EXPOSE 9090
CMD ["python", "launcher.py"]
