import socket, time
from threading import Thread

connectMsg = "Connected"
disConnectMsg = "Disconnected"

host = "0.0.0.0"
port = 9090

cons = []

soc = socket.socket()
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind((host, port))
soc.listen(10)

def handleConnection(cona, addra):
	print(f"Accepted {addra}")

	if cons == []: cons.append([cona])
	else:
		for c in range(len(cons)):
			if len(cons[c]) < 2:
				cons[c].append(cona)
				for coner in cons[c]:
					shout(connectMsg, coner)
				break
			if c == len(cons) - 1:
				cons.append([cona])

	while True:
		data = cona.recv(1024).decode()
		if data:
			print(f"From {addra}: {data}")
			shout(data, cona)
		else:
			shout(disConnectMsg, cona)
			break
	print(f"Disconnected {addra}")
	for c in cons:
		for discon in c:
			if discon == cona:
				c.pop(c.index(discon))

def shout(dater, conn):
	for c in cons:
		for con1 in c:
			if con1 == conn:
				for con2 in c:
					if not con2 == conn:
						con2.sendall(dater.encode())

print(f"Listening on {port}")
while True:
	time.sleep(1)
	con, addr = soc.accept()
	Thread(target=handleConnection, args=[con, addr]).start()
