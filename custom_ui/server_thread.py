from threading import Thread
from werkzeug.serving import make_server


# It is important to declare the thread global, so it can be referenced from anywhere.
# Declare the ServerThread global like this:
# global server
# server = ServerThread(app)
# server.start()
class ServerThread(Thread):

    def __init__(self, app, port = 5000):
        self.port = port
        Thread.__init__(self)
        # Maybe some algorithm to look for free ports instead of hardcoding/receiving one would be a good idea.
        # But thats out the scope of this project
        try:
            self.server = make_server('127.0.0.1', port, app)
        except:
            print("ServerThread: ERROR: Something went wrong while making the server. Probably port already in use.")
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.server.serve_forever()

    def getURL(self):
        return "http://127.0.0.1:"+str(self.port)

    def shutdown(self):
        self.server.shutdown()
