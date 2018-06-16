import SocketServer
import string
import sys
import random
import time

millis = lambda: int(round(time.time() * 1000))

HOST = "0.0.0.0"
PORT = 6042

TIME = 3

class connectionHandler(SocketServer.BaseRequestHandler):

    def recvall(self):
        s = self.request.recv(128)
        s.replace("\n", "")
        return s

    def handle(self):
        random.seed()
    
        mod = 0

        while (mod < 50):
            a = random.randint(100000, 1000000)
            b = random.randint(100000, 1000000)
            c = random.randint(100000, 1000000)

            mod = pow(a, b, c)

        startTime = millis()

        self.request.sendall('\nPasskey Demo 1.3\n\n'\
                                'Changelog:\n'\
                                '- So that people stop guessing, you now have to enter your passcode quickly\n'\
                                '- Increased the base and the modulus\n\n'\
                                'This is a demo to show how your passkey will be entered.\n\n' \
                                'Hint, remember that your password fits in the equation\n' \
                                '' + str(a) + ' ^ (your_passkey) % ' + str(c) + ' = ' + str(mod) + '\n\n' \
                                'Please enter your provided demo passkey. You have ' + str(TIME) + ' seconds\n')

        while True:
            try:
                l = int(self.recvall().strip())
            except:
                self.request.sendall("No, that was not in the right format\n")
                return

            if millis() - startTime > TIME * 1000:
                self.request.sendall('Your response was too slow.\n')
                return

            if pow(a, l, c) == mod:
                self.request.sendall("That is correct, you have completed the demo. flag{tim3_t0_4ut0m4t3}\n")
                return
            else:
                self.request.sendall("No, that is not your passkey.\n")
                return

if __name__ == '__main__':
    SocketServer.ForkingTCPServer.allow_reuse_address = True
    server = SocketServer.ForkingTCPServer((HOST, PORT), connectionHandler)
    server.serve_forever()