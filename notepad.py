from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton,MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivy.lang import Builder
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.core.window import Window
import os



screen_helper = """
ScreenManager:
	MenuScreen:  
   

<MenuScreen>:

	name: 'menu'
	id: ms
	inp:inp
	filename:filename

	GridLayout:
		rows:3
		orientation: 'vertical'


			
		MDToolbar:
			title: 'Notepad'
			
			padding:5
			spacing:10

			MDFloatingActionButton:
				elevation_normal:0
				icon: 'save.png'
				on_press:
					root.save()
				

			MDFloatingActionButton:
				elevation_normal:0
				icon: 'open.png'
				on_release:
					root.openfile()
			

		MDTextField:

			id : filename
			hint_text: "Enter File Name"
			size_hint_x:None
			width:300
			font_size:25
			multiline: False
		
		MDTextField:
			id : inp
			size_hint_x:None
			hint_text: "Enter Text Here"
			width:300
			font_size:20
			multiline: True


	MDFloatingActionButtonSpeedDial:
		data: root.data
		callback: root.callback
		rotation_root_button: False
		


"""
class ScreenManager(ScreenManager):
	pass

class MenuScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		Window.bind(on_keyboard=self.events)
		self.manager_open = False
		self.file_manager = MDFileManager(
			
			use_access=True,
			exit_manager=self.exit_manager,
			select_path=self.select_path,
			#previous=False,
			
		)
		


	def file_manager_open(self):
		self.file_manager.show('/')  # output manager to the screen
		self.manager_open = True

	def select_path(self, path):
		
		'''It will be called when you click on the file name
		or the catalog selection button.

		:type path: str;
		:param path: path to the selected directory or file;
		'''
		if self.fileopen == True:

			self.filepath = path

			self.exit_manager()
			print(self.filepath)
			toast(self.filepath)

			self.textfile = os.path.basename(self.filepath)
			self.file_data = os.path.splitext(self.textfile)
			self.filename.text = self.file_data[0]
			with open(self.filepath,"r") as f:
				self.txtdata = f.read()
			self.inp.text = self.txtdata

		else: # if saving as 

			self.data = self.inp.text
			self.ifilename = self.filename.text
			
			if self.ifilename =="":
				self.we = MDDialog( title="Incorrect File name",text="Please enter a File name",size_hint=[0.6,0.2])
				self.we.open()

			else:

				self.saveaspath = path

				self.saveasfilepath =f"{self.saveaspath}/{self.ifilename}.txt"

				self.CHECK_FILE = os.path.isfile(self.saveasfilepath)
				print(self.CHECK_FILE)

				if self.CHECK_FILE:
					self.asd = MDDialog( title=f"Warning, {self.ifilename}.txt already exists"
						,text="Do you want to replace it?",size_hint=[0.6,0.2],
						buttons=[
		                    MDFlatButton(
		                        text="No",on_release=self.fme_de),
		                    MDFlatButton(
		                        text="Yes", on_release=self.ss
		                    ),
                				],
						)
					self.asd.open()


					
				else:

					self.exit_manager()
					
					with open(f"{self.saveasfilepath}.txt","w",) as f:
						f.write(self.data)

					self.dialog = MDDialog( title=f"{self.ifilename}.txt Sucessfully saved in {self.saveaspath}",size_hint=[0.6,0.2])
					self.dialog.open()

	def ss(self,*args):
		self.exit_manager()
		self.asd.dismiss(force=True)
		

					
		with open(f"{self.saveasfilepath}.txt","w",) as f:
			f.write(self.data)

		self.dialog = MDDialog( title=f"{self.ifilename}.txt Sucessfully saved in {self.saveaspath}",size_hint=[0.6,0.2])
		self.dialog.open()



	def fme_de(self,*args):
		self.exit_manager()
		self.asd.dismiss(force=True)


	def exit_manager(self, *args):
		'''Called when the user reaches the root of the directory tree.'''

		self.manager_open = False
		self.file_manager.close()

	def events(self, instance, keyboard, keycode, text, modifiers):
		'''Called when buttons are pressed on the mobile device.'''

		if keyboard in (1001, 27):
			if self.manager_open:
				self.file_manager.back()
		return True
	

	data = {
		'info.png': 'About',
		'star.png': 'Rate',
		'saveas.png': 'Save as',
	}

	def openfile(self):
		self.fileopen = True
		self.file_manager_open()
		
	def saveasfile(self):
		self.fileopen = False
		self.file_manager_open()
		self.saveasfilepath = ""


		
	
	def save(self):


		self.data = self.inp.text
		self.ifilename = self.filename.text

		if self.ifilename =="":
			self.we = MDDialog( title="Incorrect File name",text="Please enter a File name",size_hint=[0.6,0.2])
			self.we.open()
		else:

			self.ddir = ("Notepad\\")
			CHECK_FOLDER = os.path.isdir(self.ddir)
			

			if not CHECK_FOLDER:
			    self.fsn = os.mkdir(self.ddir)
			else:
				self.fsn = self.ddir
			
			with open(f"{self.fsn}/{self.ifilename}.txt","w",) as f:
				f.write(self.data)
		

			self.dialog = MDDialog( title=f"{self.ifilename}.txt Sucessfully saved",size_hint=[0.6,0.2])
			self.dialog.open()



	def callback(self, instance):
		if instance.icon == 'info.png': 
			self.about = MDDialog(title="About",text="This is a Notepad made by Suyash",size_hint=[0.6,0.2])
			self.about.open()
		elif instance.icon == 'star.png':
			self.rate = MDDialog(title="RATE US",text="Please Rate us 5 Stars on Google play",size_hint=[0.6,0.2])
			self.rate.open()
		elif instance.icon == 'saveas.png':
			self.saveasfile()
	


		







class Notepad(MDApp):
	

	def build(self):
		self.root = Builder.load_string(screen_helper)






Notepad().run()