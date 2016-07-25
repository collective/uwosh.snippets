# -*- coding: utf-8 -*-
from plone import api
from Products.CMFCore.WorkflowCore import WorkflowException
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
    if not context.readDataFile('uwosh.snippets.marker.txt'):
        return

    site = context.getSite()

    if '.snippets' not in site.objectIds():
        try:
            folder = api.content.create(
                type='Folder', id='.snippets', title='Snippets', container=site)
            api.content.transition(folder, to_state='published')
        except (api.exc.InvalidParameterError, WorkflowException):
            pass
