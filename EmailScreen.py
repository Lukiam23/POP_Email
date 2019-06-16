import os
import email
from kivy.app import App
from kivy.clock import Clock
from functools import partial
from email.parser import Parser
from kivy.uix.button import Button
from email.header import decode_header
from kivy.uix.screenmanager import Screen

class EmailScreen(Screen):
	mensagens = dict()
	refesh = True
	def __init__(self,**kwargs):
		super(EmailScreen,self).__init__(**kwargs)
		self.server = None
		self.buttons = []

	def on_enter(self):
		if self.refesh:
			Clock.schedule_once(self._loadEmails)
			self.refesh = False

	def _clean(self,screen):
		for b in self.buttons:
			screen.ids.box.remove_widget(b)
		self.buttons = []


	def load(self):
		self.server = App.get_running_app().server
		return self.server.list()

	def decode_str(self,s):
	    value, charset = decode_header(s)[0]
	    if charset:
	        value = value.decode(charset)
	    return value

	def _getInfo(self,id):

		resp,msg = self.server.retr(id)

		msg_content = b'\r\n'.join(msg).decode('utf-8')
		msg = Parser().parsestr(msg_content)

		email_subject = self.decode_str(msg.get('Subject'))
		self.mensagens[id] = (email_subject,msg)
		if len(email_subject)>60:
			email_subject = email_subject.split()
			email_subject = " ".join(email_subject[0:5]) + "..."
		return email_subject

	def _downloadFile(self,part,filename,*args):
		att_path = 'C:/Users/mscor/Documents/2019.1/trabalhos de rede/POP_Email/downloadedFiles/'
		att_path = os.path.join(att_path, filename)
		if not os.path.isfile(att_path):
			fp = open(att_path, 'wb')
			fp.write(part.get_payload(decode=True))
			fp.close()

	def _getAttachments(self,msg):
		attachments = []
		for part in msg.walk():
			if part.get_content_maintype() == 'multipart':
				continue
			if part.get('Content-Disposition') is None:
				continue

			filename = self.decode_str(part.get_filename())
			attachments.append((part,filename))
		return attachments

	def _gotoEmail(self,id,*args):
		generic = self.manager.get_screen(name='generic')
		self.manager.current = 'generic'
		
		msg = self.mensagens[id][1]
		generic.ids.title.text = self.mensagens[id][0]
		generic.ids.info.text = "From: %s\nTo: %s\nDate:%s" %(msg.get("From"),msg.get("To"),msg.get("Date"))
		content = ''
		if self.mensagens[id][1].is_multipart():
			for part in self.mensagens[id][1].walk():
			    if part.get_content_type() == 'text/plain':
			        content += part.get_payload(decode=True).decode("utf-8")
		else:
			content += part.get_payload(decode=True).decode("utf-8")
		generic.ids.content.text = content

		self._clean(generic)
		attachments = self._getAttachments(msg)
		for att in attachments:
			btn = Button(text="[u][color=00BFFF]%s[/color][/u]" %att[1],font_size=14,size_hint_y=None,height=50,halign="left",text_size = self.size,valign='middle',background_color=(0.1,0.1,0.1,1),padding_x = 80,markup =True)
			btn.bind(on_press=partial(self._downloadFile,att[0],att[1]))
			self.buttons.append(btn)
			generic.ids.box.add_widget(btn)


	def _loadEmails(self,*args):
		self.ids.box.clear_widgets()
		resp,list_ =  self.load()
		
		for i in reversed(list_):
			id,size = i.split()
			id = id.decode()

			btn = Button(text=self._getInfo(id),font_size=20,size_hint_y=None,height=50,halign="left",text_size = self.size,valign='middle',background_color=(0.1,0.1,0.1,1),id = str(id),padding_x = 80)
			btn.bind(on_press=partial(self._gotoEmail,id))
			self.ids.box.add_widget(btn)
		App.get_running_app().mensagens = self.mensagens

	def _return(self):
		self.ids.box.clear_widgets()
		self.server._close()
		self.refesh = True
		self.manager.current = 'defealt'

