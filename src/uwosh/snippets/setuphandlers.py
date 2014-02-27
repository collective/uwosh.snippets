__docformat__ = "epytext"

def setupVarious(context):

    if not context.readDataFile('uwosh.snippets.marker.txt'):
        return

    site = context.getSite()
