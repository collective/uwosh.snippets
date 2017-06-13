# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def uninstall(self, reinstall=False):
    if not reinstall:
        ps = getToolByName(self, 'portal_setup')
        ps.runAllImportStepsFromProfile('profile-uwosh.snippets:uninstall')
        return "Uninstall successful."
