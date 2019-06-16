from kivy.app import App
from Defealt import Defealt
from Generic import Generic
from Manager import Manager
from kivy.lang import Builder
from EmailScreen import EmailScreen
from kivy.properties import StringProperty


Builder.load_file('manager.kv')

class EmailReaderApp(App):
	server = None
	mensagens = dict()
	content = ''
	def build(self):
		return Manager()

myApp = EmailReaderApp()
if __name__ == "__main__":
	myApp.run()