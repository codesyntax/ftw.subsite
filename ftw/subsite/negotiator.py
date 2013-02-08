from ftw.subsite.interfaces import ISubsite
from ftw.subsite.utils import find_context
from ftw.subsite.utils import get_nav_root
from Products.CMFCore.interfaces import IContentish
from Products.CMFCore.interfaces import IFolderish
from zope.i18n.interfaces import INegotiator
from zope.i18n.negotiator import negotiator as base_negotiator
from zope.interface import implements


class Negotiator(object):
    """A language negotiator whicht gets the language from an attribute stored
       on the subsite
    """
    implements(INegotiator)

    def getLanguage(self, langs, env):
        # Get current published object
        obj = find_context(env)

        # Filter out CSS/JS and other non contentish objects
        # IFolderish check includes site root
        if not (IContentish.providedBy(obj) or not IFolderish.providedBy(obj)):
            return base_negotiator.getLanguage(langs, env)

        nav_root = get_nav_root(obj)

        if ISubsite.providedBy(nav_root):
            # Get language stored on Subsite

            language = nav_root.Schema().get('forcelanguage').get(nav_root)
            if language:
                return language
        else:
            # Use normal Negotiator
            return base_negotiator.getLanguage(langs, env)

negotiator = Negotiator()
