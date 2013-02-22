from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.topics.interfaces import ITopic
from plone.app.layout.viewlets import ViewletBase
from zope.component import getAdapters
from ftw.topics.interfaces import ITopicReferencePresentation
from Products.Archetypes.interfaces.referenceable import IReferenceable


class TopicListing(object):

    listing_template = ViewPageTemplateFile('templates/topic_listing.pt')

    def get_child_topics(self):
        query = {'object_provides': ITopic.__identifier__,
                 'path': {'query': '/'.join(self.context.getPhysicalPath()),
                          'depth': 1},
                 'sort_index': 'sortable_title'}

        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(query)

    def get_represenations(self):
        referencable = IReferenceable(self.context)
        objects = referencable.getBRefs()
        adapters = dict(getAdapters((self.context, self.request),
                                     ITopicReferencePresentation)).values()

        adapters.sort(key=lambda adapter: adapter.position())

        for adapter in adapters:
            objects = adapter.consume(objects)

        return adapters


class TopicView(BrowserView, TopicListing):

    def subtopics(self):
        return self.listing_template()


class SimplelayoutTopicListingViewlet(ViewletBase, TopicListing):

    def render(self):
        return self.listing_template()
