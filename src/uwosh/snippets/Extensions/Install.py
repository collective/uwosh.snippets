# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite

def uninstall(self, reinstall=False):
	if not reinstall:
		ps = getToolByName(self, 'portal_setup')

		site = getSite()
		pt = getToolByName(site, 'portal_tinymce')

		ps.runAllImportStepsFromProfile('profile-uwosh.snippets:uninstall')

		pt.customplugins = pt.customplugins.replace(u'\nsnippets|++resource++uwosh.snippets/snippets.js', u'')
		pt.customtoolbarbuttons = pt.customtoolbarbuttons.replace(u'\nsnippetbutton', u'')

		return "Uninstall successful."
