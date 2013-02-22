from Products.CMFCore.utils import getToolByName
from ftw.topics.testing import EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
from ftw.topics.testing import EXAMPLE_CONTENT_SIMPLELAYOUT_FUNCTIONAL
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing.z2 import Browser
from pyquery import PyQuery
from unittest2 import TestCase


class TestDefaultTopicView(TestCase):

    layer = EXAMPLE_CONTENT_DEFAULT_FUNCTIONAL
    viewname = 'topic_view'

    def setUp(self):
        self.portal = self.layer['portal']
        self.tree = self.portal.get('topics')
        self.node = self.tree.get('manufacturing')
        self.subnode = self.node.get('agile-manufacturing')

        self.browser = Browser(self.layer['app'])
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.handleErrors = False

    def test_default_topic_view(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        fti = portal_types.get('ftw.topics.Topic')
        self.assertEqual(
            fti.default_view, self.viewname,
            'Expected default view to be %s on "ftw.topics.Topic"'
            ' since only the default GS profile was installed' % (
                self.viewname))

    def test_subnode_listed(self):
        self.browser.open(self.node.absolute_url() + '/' + self.viewname)
        doc = PyQuery(self.browser.contents)

        # there should be a heading "Topics"
        self.assertEqual(doc('h3').text(), 'Topics')

        # on node (Manufacturing) should be subnode (Agile Manufacturing)
        links = doc('.subelements-listing a')
        self.assertEqual(len(links), 1,
                         'Found more or less links than expected')

        self.assertEqual(links.text(), 'Agile Manufacturing')

    def test_subnode_has_no_children(self):
        self.browser.open(self.subnode.absolute_url() + '/' + self.viewname)
        doc = PyQuery(self.browser.contents)

        self.assertEqual(len(doc('h3')), 0, 'No <h3> expected')


class TestSimplelayoutTopicView(TestDefaultTopicView):

    layer = EXAMPLE_CONTENT_SIMPLELAYOUT_FUNCTIONAL
    viewname = 'simplelayout'
