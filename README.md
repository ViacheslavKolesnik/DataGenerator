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

Create RabbitMQ exchange and queues.

Create MySQL database and table with following structure:

```
+-------------+---------------+------+-----+---------+----------------+
| Field       | Type          | Null | Key | Default | Extra          |
+-------------+---------------+------+-----+---------+----------------+
| id          | bigint(20)    | NO   | PRI | NULL    | auto_increment |
| order_id    | decimal(20,0) | NO   |     | NULL    |                |
| cur_pair    | varchar(12)   | NO   |     | NULL    |                |
| direction   | varchar(5)    | NO   |     | NULL    |                |
| status      | varchar(15)   | NO   |     | NULL    |                |
| datetime    | bigint(13)    | NO   |     | NULL    |                |
| init_px     | decimal(20,5) | NO   |     | NULL    |                |
| fill_px     | decimal(20,5) | NO   |     | NULL    |                |
| init_vol    | decimal(20,8) | NO   |     | NULL    |                |
| fill_vol    | decimal(20,8) | NO   |     | NULL    |                |
| description | varchar(45)   | NO   |     | NULL    |                |
| tag         | varchar(12)   | NO   |     | NULL    |                |
+-------------+---------------+------+-----+---------+----------------+
```

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
--Max: 21 ms
--Min: 13 ms
--Mean: 18 ms
--Total: 70 ms
-Red zone generation time:
--Max: 11 ms
--Min: 11 ms
--Mean: 11 ms
--Total: 11 ms
-Green zone generation time:
--Max: 18 ms
--Min: 9 ms
--Mean: 15 ms
--Total: 45 ms
-Blue zone generation time:
--Max: 13 ms
--Min: 13 ms
--Mean: 13 ms
--Total: 13 ms
-File insertion time:
--Max: 1947 ms
--Min: 1299 ms
--Mean: 1615 ms
--Total: 6460 ms
-Message publishing time:
--Max: 421 ms
--Min: 302 ms
--Mean: 356 ms
--Total: 1425 ms
-File reading and parsing time:
--Max: 18 ms
--Min: 10 ms
--Mean: 15 ms
--Total: 60 ms
-Database writing time:
--Max: 424 ms
--Min: 327 ms
--Mean: 390 ms
--Total: 1561 ms
```
Data output file:
```
16686152631967651139 | Buy | NZD/CAD | 0.8951 | 0.90933 | 94 | 90.4 | Iphone | I am gonna be rich. | To provider | 1550273357428
16686152631967651139 | Buy | NZD/CAD | 0.8951 | 0.90933 | 94 | 90.4 | Iphone | I am gonna be rich. | Partial filled | 1550450043920
33716462425260163410 | Sell | USD/SEK | 9.2742 | 0 | 1 | 0 | Birthday | Want this so much. | To provider | 1550450043920
33716462425260163410 | Sell | USD/SEK | 9.2742 | 0 | 1 | 0 | Birthday | Want this so much. | Rejected | 1550515558357
20905387061166284861 | Sell | USD/NOK | 8.6375 | 8.36812 | 16 | 16 | Birthday | Want this so much. | To provider | 1550454561137
20905387061166284861 | Sell | USD/NOK | 8.6375 | 8.36812 | 16 | 16 | Birthday | Want this so much. | Filled | 1550515558357
...
24349622160787433091 | Buy | USD/TRY | 5.2474 | 0.0 | 18 | 0.0 | Beauty | Give it to me. | New | 1550220919039
24349622160787433091 | Buy | USD/TRY | 5.2474 | 0.0 | 18 | 0.0 | Beauty | Give it to me. | To provider | 1550254607522
05586212103347769528 | Buy | USD/CNH | 6.7847 | 0.0 | 1 | 0.0 | Birthday | Want this so much. | New | 1550220919039
05586212103347769528 | Buy | USD/CNH | 6.7847 | 0.0 | 1 | 0.0 | Birthday | Want this so much. | To provider | 1550520356400
52184270405084643251 | Sell | USD/CHF | 1.0005 | 0.0 | 76 | 0.0 | Birthday | Want this so much. | New | 1550255521944
52184270405084643251 | Sell | USD/CHF | 1.0005 | 0.0 | 76 | 0.0 | Birthday | Want this so much. | To provider | 1550520356400
53938897245171046666 | Buy | USD/MXN | 19.077 | 0.0 | 31 | 0.0 | Birthday | Want this so much. | New | 1550212189502
53938897245171046666 | Buy | USD/MXN | 19.077 | 0.0 | 31 | 0.0 | Birthday | Want this so much. | To provider | 1550255521944

```
