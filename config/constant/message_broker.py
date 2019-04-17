RABBITMQ_EXCHANGE = "orders_by_statuses"
RABBITMQ_EXCHANGE_TYPE = 'direct'
RABBITMQ_EXCHANGE_DECLARE_PASSIVE = False
RABBITMQ_EXCHANGE_DURABLE = True
RABBITMQ_QUEUE_NEW = 'status_new'
RABBITMQ_QUEUE_TO_PROVIDER = 'status_to_provider'
RABBITMQ_QUEUE_FINAL = 'status_final'
RABBITMQ_QUEUE_DECLARE_PASSIVE = False
RABBITMQ_QUEUE_DURABLE = True
RABBITMQ_QUEUE_BIND_ROUTING_KEY_NEW = 'new'
RABBITMQ_QUEUE_BIND_ROUTING_KEY_TO_PROVIDER = 'to_provider'
RABBITMQ_QUEUE_BIND_ROUTING_KEY_FILLED = 'filled'
RABBITMQ_QUEUE_BIND_ROUTING_KEY_PARTIAL_FILLED = 'partial_filled'
RABBITMQ_QUEUE_BIND_ROUTING_KEY_REJECTED = 'rejected'
RABBITMQ_MESSAGE_DELIVERY_MODE = 2
RABBITMQ_CONSUMER_INACTIVITY_TIMEOUT = 10
