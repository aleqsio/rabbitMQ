import rabbit
import json
import threading
id = rabbit.randId()
print("technicianType1 [Knee, Hip, Elbow])")
technicianType = {"k":"knee", "h": "hip", "e": "elbow", "knee":"knee", "hip":"hip","elbow":"elbow"}[input()]
print("technicianType2 [Knee, Hip, Elbow])")
technicianType2 = {"k":"knee", "h": "hip", "e": "elbow", "knee":"knee", "hip":"hip","elbow":"elbow"}[input()]



def examLoop():
  channel = rabbit.setup()

  def msgCallback(ch, method, properties, body):
    print("Received exam order %r" % body, flush=True)
    print("Received exam order %r" % body)
    rabbit.log("received exam order "+str(body))

    order = json.loads(body.decode())
    channel.basic_publish(exchange='exchange',
                        routing_key='doctor.examResult.'+order["docId"],
                        body=json.dumps({"name": order["name"], "opType": order["opType"], "ok":True}))
  channel.basic_consume(queue=technicianType+"Operations",
                      auto_ack=True,
                      on_message_callback=msgCallback)
  channel.start_consuming()

def examLoop2():
  channel = rabbit.setup()

  def msgCallback(ch, method, properties, body):
    print("Received exam order %r" % body)
    rabbit.log("received exam order "+str(body))

    order = json.loads(body.decode())
    channel.basic_publish(exchange='exchange',
                        routing_key='doctor.examResult.'+order["docId"],
                        body=json.dumps({"name": order["name"], "opType": order["opType"], "ok":True}))
  channel.basic_consume(queue=technicianType2+"Operations",
                      auto_ack=True,
                      on_message_callback=msgCallback)
  channel.start_consuming()


thread2 = threading.Thread(target=examLoop)
thread2.start()
thread1 = threading.Thread(target=examLoop2)
thread1.start()
thread3 = threading.Thread(target=rabbit.adminMsgLoop)
thread3.start()
thread1.join()
thread2.join()
thread3.join()

