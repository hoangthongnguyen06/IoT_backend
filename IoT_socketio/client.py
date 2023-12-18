import socketio
import sys
sio = socketio.Client()

# connect server
@sio.event
def connect():
    print('Connected to server')

# event ouput
@sio.on('output')
def handle_output(data):
    sys.stdout.write(data['output'])
    sys.stdout.flush()
# Disconnect
@sio.event
def disconnect():
    print('Disconnected from server')

if __name__ == '__main__':
    custom_sid = '1'
    # websocket address
    websocket_url = 'http://localhost:5000'

    # connect websocket
    sio.connect(websocket_url, headers={'SID': custom_sid})

    try:
        while True:
            # send command
            command = input("Enter command (or type 'exit' to quit): ")
            
            if command.lower() == 'exit':
                break

            sio.emit('command', command)

    except KeyboardInterrupt:
        pass  

    finally:
        # Disconnect
        sio.disconnect()
