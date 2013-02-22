from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from ftw.topics.interfaces import ITopicReferencePresentation
from ftw.topics import _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DefaultRepresentation(object):
    """Default representation"""
    implements(ITopicReferencePresentation)
    adapts(Interface, Interface)

    template = ViewPageTemplateFile(
        'templates/default_representation.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.objects = []

    def consume(self, objects):
        """Consume all objects left"""
        self.objects = objects

    def render(self):
        return self.template()

    def title(self):
        return _(u'label_further_content', default=u'Further content')

    def position(self):
        return 1000


class ContentPageRepresentation(DefaultRepresentation):
    template = ViewPageTemplateFile(
        'templates/default_representation.pt')

