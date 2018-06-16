import SocketServer
import string
import sys
import random
import time

millis = lambda: int(round(time.time() * 1000))

HOST = "0.0.0.0"
PORT = 6040

class connectionHandler(SocketServer.BaseRequestHandler):

    def recvall(self):
        s = self.request.recv(128)
        s.replace("\n", "")
        return s
    
    def handle(self):
        random.seed()

        mod = 0

        while (mod < 3):
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            c = 10

            mod = pow(a, b, c)

        startTime = millis()

        self.request.sendall('\nPasskey Demo 1.0\n\n'\
                                'Changelog: <empty>\n\n'\
                                'This is a demo to show how your passkey will be entered.\n\n' \
                                'Hint, remember that your password fits in the equation\n' \
                                '' + str(a) + ' ^ (your_passkey) % 10 = ' + str(mod) + '\n\n' \
                                'Please enter your provided demo passkey.\n')

        while True:
            try:
                l = int(self.recvall().strip())
            except:
                self.request.sendall("No, that was not in the right format\n")
                return

            if pow(a, l, c) == mod:
                self.request.sendall("That is correct, you have completed the demo. flag{pr0bably_4_1ucky_gu3ss}\n")
                return
            else:
                self.request.sendall("No, that is not your passkey. Try again.\n")

if __name__ == '__main__':
    SocketServer.ForkingTCPServer.allow_reuse_address = True
    server = SocketServer.ForkingTCPServer((HOST, PORT), connectionHandler)
    server.serve_forever()