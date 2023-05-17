from flask import Flask, request

app = Flask(__name__)

@app.route("/shutdown", methods = ['POST'])
def shutdown_server():
    print("SHUTDOWN CONTEXT HIT WITH POST")
    shutdown= request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        print('FAILURE')
        raise RuntimeError('The function is unavailable')
    else:
        shutdown()
        print("SUCCESS")
    
if __name__ == '__main__':
    app.run(port = 5000, host = '127.0.0.1', debug = True)

# result of this prototype is FAILURE: Does NOT work on Windows 11. Have to consider other approach to shut down the server.
# UPDATE: Managed to shut down server by shutting down the thread containing the server instead.