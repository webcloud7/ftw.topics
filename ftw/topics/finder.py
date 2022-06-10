from Acquisition import aq_parent
from ftw.topics.interfaces import ITopicRootFinder
from ftw.topics.interfaces import ITopicTree
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface


@implementer(ITopicRootFinder)
@adapter(Interface, Interface)
class DefaultTopicTreeFinder(object):
    """The topic tree finder is used for deciding where the topic
    trees are to select from in the "topics" widget.

    It walks up from the current context and returns the next
    INavigationRoot which contains ITopicTree objects,
    or the IPloneSiteRoot if it is reached.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_topic_root_path(self):
        obj = self.context
        while obj:
            if INavigationRoot.providedBy(obj) and \
                    self._has_direct_topic_trees(obj):
                return '/'.join(obj.getPhysicalPath())

            if IPloneSiteRoot.providedBy(obj):
                return '/'.join(obj.getPhysicalPath())

            obj = aq_parent(obj)

        return '/'.join(getSite().getPhysicalPath())

    def _has_direct_topic_trees(self, context):
        # use contentValues not objectValues because of ftw.trash
        for obj in context.contentValues():
            if ITopicTree.providedBy(obj):
                return True

        return False
