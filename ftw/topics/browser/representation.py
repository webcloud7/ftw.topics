from ftw.topics import _
from ftw.topics.interfaces import ITopicReferencePresentation
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import Interface
from zope.interface import implementer
from zope.component import adapter


@implementer(ITopicReferencePresentation)
@adapter(Interface, Interface)
class DefaultRepresentation(object):
    """Default representation"""

    template = ViewPageTemplateFile(
        'templates/default_representation.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.objects = []

    def consume(self, objects):
        """Consume all objects left"""
        self.objects = list(objects)

    def render(self):
        return self.template()

    def title(self):
        return _(u'label_further_content', default=u'Further content')

    def position(self):
        return 1000

    def available(self):
        return bool(self.objects)
