# -*- coding: utf-8 -*-
from uwosh.snippets.browser.interfaces import ISnippet
from zope.interface import implements
import re

class Snippet():
	#The Snippet class is an intermediary between the ATDocument object and the snippet UI.
	#Each ATDocument in the .snippets folder represents 1 snippet definition.
	#A separate class was created to cut down on extra, unneeded data when passing 
	#info to the UI.

	implements(ISnippet)

	def getDescription(self):
		return self.description

	def getId(self):
		#we return a "cleaned" ID. It should have been cleaned already at creation time....
		#but better to err on the side of caution
		return re.sub(r'\W', '', self.id)

	def getText(self):
		return self.text

	def getTitle(self):
		return self.title

	def getWorkflowState(self):
		#current unused
		return self.state

	def setDescription(self, description):
		self.description = description

	def setId(self, snippetId):
		self.id = snippetId

	def setText(self, snippetText):
		self.text = snippetText

	def setTitle(self, snippetTitle):
		self.title = snippetTitle

	def setWorkflowState(self, state):
		#currently unused
		self.state = state







