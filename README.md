# Data generator
## Description
Generates data.

Writes data to file.

Publishes serialized data to message broker.

Read data from file.

Writes data to database.
## Requirements
- python 3.7:
  - pymysql 0.9.3
  - pika 0.13.0
  - protobuf 3.7.1
- mysql server 8.0.15
- rabbitmq 3.7.12:
  - requires Erlang/OTP >=20.3
## Run steps
Install python.

Install additional modules:
`python -m pip install -r ./requirements.txt`

Install MySQL server:
  - linux:
    `https://dev.mysql.com/downloads/file/?id=482330`
  - windows:
    `https://dev.mysql.com/downloads/file/?id=484900`

Install RabbitMQ:
  - linux:
    `https://packagecloud.io/rabbitmq/rabbitmq-server/install#bash-deb`
  - windows:
    `https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.7.12/rabbitmq-server-3.7.12.exe`
  - requires Erlang/OTP >=20.3:
    `https://www.erlang.org/downloads/20.3`

Create RabbitMQ exchange, queues, bindings.

Create MySQL database and table with script:
`table_creation_script.sql`

Edit configs(DataGenerator/config_files/) according to your database/RabbitMQ and other configurations.

Browse to root project directory and run following in command line: `python launcher.py`.
## Run example
Report:
```
Startup configurations:
-Red zone orders: 300.
-Green zone orders: 1200.
-Blue zone orders: 500.
-Total orders: 2000.
-Chunk size: 500.
----------------------------------
Results:
-Generation time:
--Max: 24 ms
--Min: 12 ms
--Mean: 17 ms
--Total: 69 ms
-Red zone generation time:
--Max: 9 ms
--Min: 9 ms
--Mean: 9 ms
--Total: 9 ms
-Green zone generation time:
--Max: 17 ms
--Min: 14 ms
--Mean: 16 ms
--Total: 47 ms
-Blue zone generation time:
--Max: 12 ms
--Min: 12 ms
--Mean: 12 ms
--Total: 12 ms
-Message publishing time:
--Max: 644 ms
--Min: 449 ms
--Mean: 556 ms
--Total: 2225 ms
-Database writing time:
--Max: 280 ms
--Min: 194 ms
--Mean: 231 ms
--Total: 923 ms
-Received from message broker: 5200
-Written to db:
--Order records: 5200
--Orders: 2000
--Red zone orders: 300
--Green zone orders: 1200
--Blue zone orders: 500
```
