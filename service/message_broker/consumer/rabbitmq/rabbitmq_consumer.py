from pika.exceptions import *
from threading import Thread

from service.message_broker.consumer.consumer import Consumer


class RabbitMQConsumer(Consumer):
	def __init__(self, logger, storage, message_broker_connection_manager, queue):
		super(RabbitMQConsumer, self).__init__(logger)
		self.__storage = storage
		self.connection_manager = message_broker_connection_manager
		self.__connection = None
		self.__channel = None
		self.__queue = queue
		self.__thread = None

	def start(self):
		self.__thread = Thread(target=self._consume)
		self.__thread.start()

	def _consume(self):
		self.__connection = self.connection_manager.open_connection()
		self.__channel = self.__connection.channel()
		try:
			self.__channel.basic_consume(queue=self.__queue,
										 on_message_callback=self._on_consume,
										 auto_ack=True,)
			self.__channel.start_consuming()
		except ChannelError as ex:
			self.logger.error("ChanelError occured while consuming from queue {0}".format(self.__queue))
			self.logger.error(ex)
		except AMQPError as ex:
			self.logger.error("AMQPError occured while consuming from queue {0}".format(self.__queue))
			self.logger.error(ex)
		except Exception as ex:
			self.logger.error("Error occured while consuming from queue {0}".format(self.__queue))
			self.logger.error(ex)

	def _on_consume(self, ch, method, properties, message):
		self.__storage.put(message)
