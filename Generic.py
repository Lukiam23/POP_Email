from kivy.app import App
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

class Generic(Screen):
	def __init__(self,**kwargs):
		super(Generic,self).__init__(**kwargs)
		self.server = None
		self.mensagens = dict()
	def _return(self):
		self.manager.current = 'emailscreen'