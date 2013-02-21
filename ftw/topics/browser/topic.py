from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.topics.interfaces import ITopic
from plone.app.layout.viewlets import ViewletBase


class SubtopicListing(object):

    listing_template = ViewPageTemplateFile('templates/subtopic_listing.pt')

    def get_child_topics(self):
        query = {'object_provides': ITopic.__identifier__,
                 'path': {'query': '/'.join(self.context.getPhysicalPath()),
                          'depth': 1},
                 'sort_index': 'sortable_title'}

        catalog = getToolByName(self.context, 'portal_catalog')
        return catalog(query)


class TopicView(BrowserView, SubtopicListing):

    def subtopics(self):
        return self.listing_template()


class SimplelayoutTopicListingViewlet(ViewletBase, SubtopicListing):

    def render(self):
        return self.listing_template()
