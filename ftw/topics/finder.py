from Acquisition import aq_parent, aq_inner
from ftw.topics.interfaces import ITopicRootFinder
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements


class DefaultTopicTreeFinder(object):
    implements(ITopicRootFinder)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def get_topic_root_path(self):
        obj = self.context

        while obj and not INavigationRoot.providedBy(obj):
            obj = aq_parent(aq_inner(obj))

        return '/'.join(obj.getPhysicalPath())
