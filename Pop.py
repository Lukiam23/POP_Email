"""
	Este programa teve como base a biblioteca poplib: https://github.com/python/cpython/blob/master/Lib/poplib.py#L412
"""
import socket
import ssl

CR = b'\r'
LF = b'\n'
CRLF = CR+LF

#tamanho máximo ao chamar readline
maxLength = 2048

class error_per(Exception):
	pass

class Pop:
	def __init__(self, host, port, timeout = socket._GLOBAL_DEFAULT_TIMEOUT):
		self.host = host
		self.port = port 
		self.sock = self._connect_to(timeout)
		self.file = self.sock.makefile('rb')
		self.firstMenssagem = self._getline()

	def _connect_to(self,timeout):
		context = ssl._create_stdlib_context(certfile=None,
                                                     keyfile=None)
		sock = socket.create_connection((self.host,self.port),timeout)
		sock = context.wrap_socket(sock,
                                            server_hostname=self.host)
		return sock

	def _sendCommand(self,line):
		line = bytes(line,"UTF8")
		self.sock.sendall(line+CRLF)

	def _getline(self):
		line = self.file.readline(maxLength + 1)
		
		if len(line)>maxLength:
			raise error_per('line length exceeded')

		if not line: 
			raise error_per('-ERR EOF')

		#Aqui eliminamos os ...LF, ...CRLF, CR...LF
		#que aparecem na linha lida
		if line[-2:] == CRLF:
			return line[:-2]
		if line[:1] == CR:
			return line[1:-1]
		return line[:-1]

	def _getresp(self):
		response = self._getline()
		if not response.startswith(b'+'):
			raise error_per(response)
		return response

	def user(self,user):
		comand = "USER %s" %user
		self._sendCommand(comand)
		return self._getresp()

	def passw(self,passw):
		comand = "PASS %s" %passw
		self._sendCommand(comand)
		return self._getresp()
	
	def _longResponse(self):
		response = self._getresp() #Retorna a mensagem do servidor -OK ou -ER
		list = []
		line = self._getline()
		#Enquanto não chegar ao final da mensagem ele pega a linha adiciona em list e 
		#soma o número de caracters menos um em n_char
		while line != b'.':			
			list.append(line)
			line = self._getline()
		return response, list

	def list(self):
		cmd = "LIST"
		self._sendCommand(cmd)
		return self._longResponse()

	def retr(self,id):
		cmd = "RETR %s" %id
		self._sendCommand(cmd)
		return self._longResponse()



	def _close(self):
		try:
			self.file.close()
		finally:
			try:
				self.sock.shutdown(socket.SHUT_RDWR)
			except:
				return "Connection error"
			finally:
				self.sock.close()