from channels.generic.websocket import WebsocketConsumer

class LeaveJoinConsumer(WebsocketConsumer):
    def connect(self):
        print('connected')
        self.accept()
        self.send('ya zakonnectilsya')
    def receive(self, text_data=None, bytes_data=None):
        print('received message', text_data)
    def disconnect(self, code):
        print('disconnect')