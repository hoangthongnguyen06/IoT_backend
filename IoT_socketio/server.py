import subprocess
import threading
import socketio
from collections import defaultdict

connections = defaultdict(dict)
# create a socketio
sio = socketio.Server()

# Create WSGI (Web Server Gateway Interface) 
app = socketio.WSGIApp(sio)

def get_sid_from_environ(environ):
    if isinstance(environ, dict):
        return environ.get('HTTP_SID') or environ.get('QUERY_STRING')
    return None
# event connect from client
@sio.event
def connect(sid, environ):
    client_sid = get_sid_from_environ(environ)
    
    print(f"Client connected: {client_sid}")
    connections[sid]['sid'] = client_sid
#  stream output  subprocess
def stream_output(process, sid):
    for line in process.stdout:
        sio.emit('output', {'output': line}, room=sid)
    process.stdout.close()

# request from client
@sio.event
def command(sid, data):
    client_sid = connections[sid].get('sid')
    print(f"Received command from {client_sid}: {data}")

    # run command and return output
    try:
        process = subprocess.Popen(data, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True)
        output_thread = threading.Thread(target=stream_output, args=(process, sid))
        output_thread.start()
        process.wait()
        output_thread.join()
    except subprocess.CalledProcessError as e:
        error_output = e.output if e.output else str(e)
        sio.emit('output', {'output': f"Error: {error_output}"}, room=sid)

# event when disconnect client
@sio.event
def disconnect(sid):
    client_sid = connections[sid].get('sid')
    
    print(f"Client disconnected: {client_sid}")
    if sid in connections:
        del connections[sid]

# run server port 5000
if __name__ == '__main__':
    import eventlet
    import socket

    eventlet.monkey_patch()
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
