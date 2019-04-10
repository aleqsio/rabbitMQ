import rabbit
import json
import threading

id = rabbit.randId()

def resultLoop():
  channel = rabbit.setup()
  result = channel.queue_declare(queue='', exclusive=True)

  def msgCallback(ch, method, properties, body):
      print("Received exam results %r" % body, flush=True)
      rabbit.log("received results "+str(body))
  channel.queue_bind(
          exchange='exchange', queue=result.method.queue, routing_key="doctor.examResult."+id)

  channel.basic_consume(queue=result.method.queue,
                      auto_ack=True,
                      on_message_callback=msgCallback)
  channel.start_consuming()


def mainLoop():
  channel = rabbit.setup()

  while(True):
    print("opType [K_nee, H_ip, E_lbow])")
    opType = {"k":"knee", "h": "hip", "e": "elbow", "knee":"knee", "hip":"hip","elbow":"elbow"}[input()]
    print("name")
    name = input()
    channel.basic_publish(exchange='exchange',
                          routing_key='technician.exam.'+opType,
                          body=json.dumps({"name": name, "opType": opType, "docId": id}))
    rabbit.log("sending exam order for "+json.dumps({"name": name, "opType": opType, "docId": id}))


thread1 = threading.Thread(target=mainLoop)
thread1.start()
thread2 = threading.Thread(target=resultLoop)
thread2.start()
thread3 = threading.Thread(target=rabbit.adminMsgLoop)
thread3.start()
thread1.join()
thread2.join()
thread3.join()

