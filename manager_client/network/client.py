import socket
import selectors
import threading
import json

from manager_network.messagedata import MessageData, RPCMessage, NetworkMessage

# Network client with rpc support
class Client:
    def __init__(self):
        self.last_message_id = 0
        self.waiting_rpcs = {}
        self.resolved_rpcs = {}
        self.should_run = False

    def loop(self):
        try:
            while self.should_run:
                # receiving packet length, if nothing was received the server dropped the connection
                # in that case stopping the thread, and trying to reconnect
                data_len = int.from_bytes(self.sock.recv(4, socket.MSG_WAITALL), 'little')

                if data_len is None:
                    break

                # Receiving full message into basic NetworkMessage
                message = self.sock.recv(data_len, socket.MSG_WAITALL)
                network_message = NetworkMessage.from_json(json.loads(message.decode()))

                # If the message was associated with any rpc calls, resolve them and release the mutex
                if self.waiting_rpcs[network_message.message_id] is not None:
                    self.resolved_rpcs[network_message.message_id] = network_message.data
                    self.waiting_rpcs[network_message.message_id].release()
        except Exception:
            pass
        self.logout()

    def connect(self, host):
        self.host = host
        self.should_run = True
        self.thread = threading.Thread(target=lambda: self.loop())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, 1589))
        self.thread.start()

    def disconnect(self):
        self.should_run = False
        self.sock.close()

    def logout(self):
        self.disconnect()
        self.connect(self.host)

    def send(self, data: MessageData) -> NetworkMessage:
        # Packing the message data into json
        json_data = json.dumps(data.to_json())

        # Allocating a new message id for rpc calls
        self.last_message_id += 1
        network_message = NetworkMessage(self.last_message_id, data.message_type(), json_data)

        # Encoding full NetworkMessage into json and sending it over the network
        message_data = json.dumps(network_message.to_json()).encode()
        self.sock.send(len(message_data).to_bytes(4, 'little'))
        self.sock.send(message_data)
        return network_message

    # Sending a message using RPC will block until a response is received
    def send_rpc(self, data: RPCMessage) -> MessageData:
        # sendind message as usual
        message = self.send(data)

        # creating a signaled mutex for rpc and putting it into the waiting queue
        lock = threading.Lock()
        lock.acquire()
        self.waiting_rpcs[message.message_id] = lock

        # waiting for the mutex to be released by the rpc response
        lock.acquire()

        # removing the mutex from the waiting queue
        self.waiting_rpcs[message.message_id] = None

        # getting the response and parsing it into a dictionary
        response = self.resolved_rpcs[message.message_id]
        response_data = json.loads(response)
        # removing the response data from the queue
        self.resolved_rpcs[message.message_id] = None

        # releasing the mutex
        lock.release()

        # parsing the response from json and returning to the caller
        response_obj = data.response_from_json(response_data)

        return response_obj
