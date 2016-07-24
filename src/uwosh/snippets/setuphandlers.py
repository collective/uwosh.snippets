# -*- coding: utf-8 -*-

from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        """
        Prevents all profiles but 'default' from showing up in the
        profile list when creating a Plone site.
        """
        return [
            u'uwosh.snippets:uninstall',
        ]


def setupVarious(context):
    site = context.getSite()

    if '.snippets' not in site.objectIds():
        folder = api.content.create(
            type='Folder', id='.snippets', title='Snippets', container=site)
        try:
            api.content.transition(folder, to_state='published')
        except:
            pass
