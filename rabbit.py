import pika
import random
import string

def setup():
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()

  channel.exchange_declare(exchange='exchange', exchange_type='topic')
  channel.queue_declare(queue='kneeOperations')
  channel.queue_declare(queue='elbowOperations')
  channel.queue_declare(queue='hipOperations')
  for joint in ["knee", "elbow", "hip"]:
    channel.queue_bind(
            exchange='exchange', queue=joint+'Operations', routing_key="technician.exam."+joint)
  
  return channel


def adminMsgLoop():
  def msgCallback(ch, method, properties, body):
      print("Received admin message %r" % body)

  channel = setup()

  msgQueue = channel.queue_declare(queue="", exclusive=True)

  channel.queue_bind(
        exchange='exchange', queue=msgQueue.method.queue, routing_key="admin.msg")

  channel.basic_consume(queue=msgQueue.method.queue,
                      auto_ack=True,
                      on_message_callback=msgCallback)

  channel.start_consuming()


def log(msg):
  channel = setup()

  channel.basic_publish(exchange='exchange',
                      routing_key='admin.log',
                      body=msg)

def randId():
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
