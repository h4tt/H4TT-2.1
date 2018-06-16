import SocketServer
import string
import sys
import random
import time

millis = lambda: int(round(time.time() * 1000))

HOST = "0.0.0.0"
PORT = 6043

TIME = 20
CRACKS = 10

class connectionHandler(SocketServer.BaseRequestHandler):

    def recvall(self):
        s = self.request.recv(128)
        s.replace("\n", "")
        return s
    
    def handle(self):
        random.seed()

        mod = 0

        a = random.randint(1000000, 10000000)
        b = random.randint(1000000, 10000000)
        c = random.randint(100000000, 1000000000)

        mod = pow(a, b, c)

        self.request.sendall('\nFsociety passkey attacker 1.0\n\n'\
                                'Changelog:\n\n'\
                                'This is the Fsociety l33t passkey attacker.\n\n' \
                                'Evilcorp generates new passkeys every ' + str(TIME) + ' seconds.\n' \
                                'You need to submit a valid passkey before the time limit.\n'\
                                'We need to successfully authenticate ' + str(CRACKS) + ' consecutive passkeys to gain access to the classified data.\n' \
                                '' + str(a) + ' ^ (your_passkey) % ' + str(c) + ' = ' + str(mod) + '\n\n' \
                                'You need to crack ' + str(CRACKS) + ' more passkeys\n'\
                                'Enter your provided demo passkey. You have ' + str(TIME) + ' seconds\n')

        for i in range(1, CRACKS):
            startTime = millis()
            try:
                l = int(self.recvall().strip())
            except:
                self.request.sendall("No, that was not in the right format\n")
                return

            if millis() - startTime > TIME * 1000:
                self.request.sendall('Your response was too slow, that is an old password.\n')
                return

            if pow(a, l, c) == mod:
                a = random.randint(1000000, 10000000)
                b = random.randint(1000000, 10000000)
                c = random.randint(100000000, 1000000000)

                mod = pow(a, b, c)

                self.request.sendall("\nThat passkey has authenticated correctly. Here is the next one,\n"
                                '' + str(a) + ' ^ (your_passkey) % ' + str(c) + ' = ' + str(mod) + '\n' \
                                'You need to crack ' + str(CRACKS - i) + ' more passkeys\n'\
                                'Enter your provided demo passkey. You have ' + str(TIME) + ' seconds\n')
            else:
                self.request.sendall("That passkey did not authenticate properly.\n")
                return
        self.request.sendall('Well done, we have all of the passwords that we need, and can now access the archives.\n' \
                            'You\'ll need this: flag{m0dul4r_3xp0n3nti4ti0n_i5_trivi4l}')

if __name__ == '__main__':
    SocketServer.ForkingTCPServer.allow_reuse_address = True
    server = SocketServer.ForkingTCPServer((HOST, PORT), connectionHandler)
    server.serve_forever()