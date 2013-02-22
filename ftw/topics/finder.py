from ftw.topics.interfaces import ITopicRootFinder
from zope.component import adapts
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.interface import implements


class DefaultTopicTreeFinder(object):
    implements(ITopicRootFinder)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def get_topic_root_path(self):
        return '/'.join(getSite().getPhysicalPath())
