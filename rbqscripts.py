#scripts for rabbitmq

import pika
import uuid
import subprocess
from subprocess import Popen,PIPE
import re

#class for client works like shit
class TesterStbt(object):

	g_data='a' #make class to put data of test you want to do !!!
	g_host='localhost'
	g_routing_key='task_stbt'

	def __init__(self):
		self.g_data='a' #make class to put data of test you want to do !!!
		g_host='localhost'
		self.g_routing_key='task_stbt'

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host = str(g_host)))
		self.channel = self.connection.channel()

		result = self.channel.queue_declare(queue='', exclusive=True)
		self.callback_queue = result.method.queue

		self.channel.basic_consume(
			queue=self.callback_queue,
			on_message_callback=self.on_response,
			auto_ack=True)

	def on_response(self,ch,method,props,body):
		if self.corr_id==props.correlation_id:
			self.response = body

	def call(self):
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(
			exchange='',
			routing_key=self.g_routing_key,
			properties=pika.BasicProperties(reply_to=self.callback_queue,correlation_id=self.corr_id,),
			body=str(self.g_data))
		while self.response is None:
			self.connection.process_data_events()
		return str(self.response)

#class for server/stbterster maker 

class StbtTestMaker(object):

	g_host='localhost'
	g_queue='task_stbt'

	def __init__(self):

		self.g_host='localhost'
		g_queue='task_stbt'
		#g_specify=list()
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.g_host))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=g_queue) #durable=True
		self.channel.basic_qos(prefetch_count=1)


	def receive(self):
		#self.channel.basic_qos(prefetch_count=1)
		self.channel.basic_consume(queue=self.g_queue,on_message_callback=self.on_request)
		self.channel.start_consuming()

	def on_request(self, ch, method, props, body):
		print(" [X] Received %r" % body)
		self.doTask(self.setSpecify(body))
		print(" [Y] Done ")
		us = UniwersalSend()
		us.send('Start Test')

	def doTask(self, l_specify):
		print(l_specify)
		subtask="sudo stbt run /stbt/Stb-tester-test-pack-anovo-master-clone/tests/test_anv.py::test_wygrzewanieWstepneDsiW74"
		Popen([subtask],stdout=PIPE,shell=True)

	def setSpecify(self, data):

		l_list=re.sub("[^\w]", " ",  str(data)).split()
		return l_list


class UniwersalSend(object):

	g_host='localhost'
	g_queue='task_stbt'
	g_routing_key='task_stbt'

	def __init__(self):
		g_host='localhost'
		g_queue='task_stbt'
		g_routing_key='task_stbt'

		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.g_host))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=self.g_queue, durable=True)


	def send(self,data):

		self.channel.basic_publish(
    			exchange='',
    			routing_key=self.g_routing_key,
    			body=data,
    			properties=pika.BasicProperties(
        			delivery_mode=2,  # make message persistent
    			))

		self.connection.close()


class Uniwersalreceiver(object):


	g_host='localhost'
	g_queue='task_stbt'
	g_routing_key='task_stbt'
	g_return=False

	def __init__(self):

		g_host='localhost'
		g_queue='task_stbt'
		g_routing_key='task_stbt'
		g_return=False

		self.connection = pika.BlockingConnection(
			pika.ConnectionParameters(host=g_host))
		self.channel = self.connection.channel()

		self.channel.queue_declare(queue=g_queue, durable=True)

	def receive(self):
		self.channel.basic_qos(prefetch_count=1)
		self.channel.basic_consume(queue=self.g_queue, on_message_callback=self.callback)
		self.channel.start_consuming()

	def callback(self, ch, method, properties, body):
		print(str(body))
		self.g_return=True
		ch.basic_ack(delivery_tag=method.delivery_tag)


