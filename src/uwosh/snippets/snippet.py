from uwosh.snippets.browser.interfaces import ISnippet
from zope.interface import implements
import re

class Snippet():

	implements(ISnippet)

	def getDescription(self):
		return self.description

	def getId(self):
		#we return a "cleaned" ID. It should have been cleaned already at creation time....
		#but better to error on the side of caution
		return re.sub(r'\W', '', self.id)

	def getText(self):
		return self.text

	def getTitle(self):
		return self.title

	def getWorkflowState(self):
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
		self.state = state







