from ftw.topics.interfaces import ITopicTree
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ITopicTreeSchema(model.Schema):
    pass


@implementer(ITopicTree)
class TopicTree(Container):
    pass
