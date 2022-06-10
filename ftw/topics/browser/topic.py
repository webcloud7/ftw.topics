from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.topics.interfaces import IBackReferenceCollector
from ftw.topics.interfaces import ITopic
from ftw.topics.interfaces import ITopicReferencePresentation
from zope.component import getAdapters
from zope.component import getMultiAdapter


class TopicListing(object):

    listing_template = ViewPageTemplateFile('templates/topic_listing.pt')

    def __init__(self):
        self.objects = None
        self.representations = None

    def render_topic_listing(self):
        self.objects = self._get_objects()
        self.representations = self._get_representations()

        return self.listing_template()

    def get_child_topics(self):
        query = {'object_provides': ITopic.__identifier__,
                 'path': {'query': '/'.join(self.context.getPhysicalPath()),
                          'depth': 1},
                 'sort_on': 'sortable_title'}

        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(query)

    def _get_representations(self):
        adapters = dict(getAdapters((self.context, self.request),
                                    ITopicReferencePresentation)).values()

        sorted(adapters, key=lambda adapter: adapter.position())

        objects = self.objects
        for adapter in adapters:
            objects = adapter.consume(objects)

        return adapters

    def _get_objects(self):
        collector = getMultiAdapter((self.context, self.request),
                                    IBackReferenceCollector)
        objects = collector()
        if not objects:
            return []

        objects.sort(key=lambda obj: obj.Title())

        return objects


class TopicView(BrowserView, TopicListing):

    def __init__(self, *args, **kwargs):
        BrowserView.__init__(self, *args, **kwargs)
        TopicListing.__init__(self)

    def subtopics(self):
        return self.render_topic_listing()
