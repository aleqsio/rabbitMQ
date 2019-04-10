import rabbit
import json
import threading



def logLoop():
  channel = rabbit.setup()
  logQueue = channel.queue_declare(queue='', exclusive=True)
  channel.queue_bind(
              exchange='exchange', queue=logQueue.method.queue, routing_key="admin.log")
  def msgCallback(ch, method, properties, body):

    print("Received log item %r" % body, flush=True)

  channel.basic_consume(queue=logQueue.method.queue,
                      auto_ack=True,
                      on_message_callback=msgCallback)
  channel.start_consuming()



def mainLoop():
  channel = rabbit.setup()

  while(True):
    print("what is the message")
    msg = input()
    channel.basic_publish(exchange='exchange',
                          routing_key='admin.msg',
                          body=msg)
    rabbit.log("sending admin msg "+msg)


thread2 = threading.Thread(target=logLoop)
thread2.start()
thread3 = threading.Thread(target=mainLoop)
thread3.start()
thread2.join()
thread3.join()

