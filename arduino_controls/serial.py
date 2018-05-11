class Controls:

    def __init__(self, port):
        self._port = port

        while self._port.available() <= 0:
            continue

        self.handshake()

    def handshake(self):
        while self._port.available() <= 0:
            continue
        res = self._port.readStringUntil(ord('\n'))
        while res != '[PONG]':
            while self._port.available() <= 0:
                continue
            res = self._port.readStringUntil(ord('\n'))
            if res:
                res = res.strip()
                print('[DEBUG] [SERIAL] %s' % res)
            self._port.write('PING\n')
            delay(100)

    def check(self):
        if self._port.available() > 0:
            res = self._port.readStringUntil(ord('\n'))
            if res:
                res = res.strip()
                print('[DEBUG] [SERIAL] %s' % res)
                res = res.split()
                if res[0] == '[Button]':
                    return res[1]
        return None