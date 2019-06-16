from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from Pop import Pop
import email
from email.parser import Parser
from email.header import decode_header


class Defealt(Screen):
	def __init__(self,**kwargs):
		super(Defealt,self).__init__(**kwargs)

	def connect(self):
		SERVER = self.ids.server.text
		USERNAME = self.ids.username.text
		PASSWORD = self.ids.password.text
		PORT = int(self.ids.port.text)
		

		try:
			# connect to server
			self.server = Pop(SERVER,PORT)
			App.get_running_app().server = self.server
			# log in
			self.server.user(USERNAME)
			self.server.passw(PASSWORD)
			self.manager.current = 'emailscreen'
		except:
			popup = Popup(title='Warning',content=Label(text='Connection Failed!'),size_hint=(None, None), size=(200, 200))
			popup.open()
		