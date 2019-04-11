from pika.exceptions import *
from threading import Thread

from service.message_broker.consumer.consumer import Consumer


class RabbitMQConsumer(Consumer, Thread):
	def __init__(self, logger, storage, message_broker_connection_manager, queue):
		Thread.__init__(self)
		super(RabbitMQConsumer, self).__init__(logger)
		self.__storage = storage
		self.connection_manager = message_broker_connection_manager
		self.__queue = queue
		self.__is_interrupted = False

	def start(self):
		Thread.start(self)

	def run(self):
		self._consume()

	def stop(self):
		self.__is_interrupted = True

	def _consume(self):
		connection = self.connection_manager.open_connection()
		channel = connection.channel()
		try:
			# self.__channel.basic_consume(queue=self.__queue,
			# 							 on_message_callback=self._on_consume,
			# 							 auto_ack=True,)
			# self.__channel.start_consuming()
			for message in channel.consume(queue=self.__queue, auto_ack=True, inactivity_timeout=1):
				if self.__is_interrupted:
					break
				if not message:
					continue
				method, properties, body = message
				if not body:
					continue
				self._on_consume(body)
			self.connection_manager.close_channel(channel)
			self.connection_manager.close_connection(connection)
		except ChannelError as ex:
			self.logger.error("ChanelError occured while consuming from queue {0}".format(self.__queue))
			self.logger.error(ex)
		except AMQPError as ex:
			self.logger.error("AMQPError occured while consuming from queue {0}".format(self.__queue))
			self.logger.error(ex)
		except Exception as ex:
			self.logger.error("Error occured while consuming from queue {0}".format(self.__queue))
			self.logger.error(ex)

	# def _on_consume(self, ch, method, properties, message):
	# 	self.__storage.put(message)

	def _on_consume(self, message):
		self.__storage.put(message)
