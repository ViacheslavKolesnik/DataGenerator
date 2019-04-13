from pika.exceptions import *
from threading import Thread

from config.constant.exit_code import EXIT_CODE_CONSUMING_ERROR
from service.message_broker.consumer.consumer import Consumer


class RabbitMQConsumer(Consumer, Thread):
	def __init__(self, logger, storage, message_broker, queue):
		Thread.__init__(self)
		super(RabbitMQConsumer, self).__init__(logger)
		self.__storage = storage
		self.message_broker = message_broker
		self.__queue = queue
		self.__is_interrupted = False

	def start(self):
		Thread.start(self)

	def run(self):
		self.message_broker.open_connection()
		channel = self.message_broker._get_channel()

		self._consume(channel)

		self.message_broker._close_channel(channel)
		self.message_broker.close_connection()

	def stop(self):
		self.__is_interrupted = True

	def _consume(self, channel):
		try:
			for message in channel.consume(queue=self.__queue, auto_ack=True, inactivity_timeout=1):
				if self.__is_interrupted:
					break
				if not message:
					continue
				method, properties, body = message
				if not body:
					continue
				self._on_consume(body)
		except Exception as ex:
			self.logger.fatal("Error occured while consuming from queue {0}".format(self.__queue))
			self.logger.fatal(ex)
			exit(EXIT_CODE_CONSUMING_ERROR)

	def _on_consume(self, message):
		self.__storage.put(message)
