import socketio
import json

class NotificationHandler:
    def __init__(self, server_url):
        self.sio = socketio.Client()
        self.server_url = server_url
        self._setup_socketio()

    def _setup_socketio(self):
        @self.sio.event
        def connect():
            print('Notification: Connected to server')

        @self.sio.event
        def disconnect():
            print('Notification: Disconnected from server')

        self.sio.connect(self.server_url)

    def send_notification(self, message):
        if self.sio.connected:
            self.sio.emit('notification', {'message': message})

    def disconnect(self):
        self.sio.disconnect()

# Esempio di utilizzo
if __name__ == "__main__":
    notifier = NotificationHandler('http://localhost:12346')
    notifier.send_notification('Test notification')
    notifier.disconnect()
