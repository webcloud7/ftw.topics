from ftw.topics import _
from ftw.topics.interfaces import ITopic
from plone.dexterity.content import Container
from plone.supermodel import model
from zope import schema
from zope.interface import implementer

class ITopicSchema(model.Schema):

    show_backrefs = schema.Bool(
        title=_("Show backreferences"),
        default=True,
        required=False
    )


@implementer(ITopic)
class Topic(Container):
    pass
