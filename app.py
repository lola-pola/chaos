from fastapi import FastAPI
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import time
import os
import socket


app = FastAPI()

@app.get('/')
def index():
    hostname = socket.gethostname()
    return {"message": f"Hello World {hostname} "}




@app.post("/send-message")
def send_message(connection_string: str ,queue: str  , message: str = 'elhays', delay: int = 0,how_many: int = 1, message_length: int = 1024):
    try:
    # Create a ServiceBusClient using the connection string
        servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_string, logging_enable=True)
        client = servicebus_client.get_queue_sender(queue_name=queue)
        for msg in range(how_many):
            tmp_message = f"{message}-{msg}"
            tmp_message = str(tmp_message*message_length)
            _message = ServiceBusMessage(tmp_message)
            client.send_messages(_message)
            time.sleep(delay)
        return {"message": f"{how_many} Message sent successfully {message}"}
    except Exception as e:
        return {"message": f"Error: {e}"}
    finally:
        client.close()
        
        
@app.get("/receive-message")
def receive_message(connection_string: str ,queue: str  , ):
    try:
        # Create a ServiceBusClient using the connection string
        servicebus_client = ServiceBusClient.from_connection_string(conn_str=connection_string, logging_enable=True)
        # Receive the message from the queue
        res = []
        with servicebus_client:
            receiver = servicebus_client.get_queue_receiver(queue_name=queue, max_wait_time=5)
            with receiver:
                for msg in receiver:
                    receiver.complete_message(msg)
                    res.append(str(msg))
                    
            return {"message": "Message received successfully"+ str(res)}
    except Exception as e:
        return {"message": f"Error: {e}"}
    finally:
        receiver.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)