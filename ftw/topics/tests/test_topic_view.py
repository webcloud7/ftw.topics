from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.testing.testcase import Dummy
from ftw.topics.tests import FunctionalTesting
from plone.browserlayer.layer import mark_layer
from Products.CMFCore.utils import getToolByName
import transaction


class TestDefaultTopicView(FunctionalTesting):

    viewname = 'topic_view'

    def setUp(self):
        super().setUp()
        self.grant('Manager')
        self.createContent()
        self.tree = self.portal.get('topics')
        self.node = self.tree.get('manufacturing')
        self.subnode = self.node.get('agile-manufacturing')
        self.topic_technology = self.tree.get('technology')

        mark_layer(None, Dummy(request=self.request))

    def test_default_topic_view(self):
        portal_types = getToolByName(self.portal, 'portal_types')
        fti = portal_types.get('ftw.topics.Topic')
        self.assertEqual(
            fti.default_view, self.viewname,
            'Expected default view to be %s on "ftw.topics.Topic"'
            ' since only the default GS profile was installed' % (
                self.viewname))

    @browsing
    def test_subnode_listed(self, browser):
        browser.open(self.node, view=self.viewname)
        doc = browser.css('h2.subelements-heading').first.text

        self.assertEqual(doc, 'Topics', 'Expected a "Topics" heading')

        # on node (Manufacturing) should be subnode (Agile Manufacturing)
        link_nodes = browser.css('.subelements-listing a')
        self.assertEqual(len(link_nodes), 2,
                         'Found more or less links than expected')

        self.assertEqual(' '.join(link_nodes.text), 'Agile Manufacturing Quality')

    @browsing
    def test_subnode_has_no_children(self, browser):
        browser.open(self.subnode, view=self.viewname)

        self.assertFalse(browser.css('h2.subelements-heading'),
                         'Expected no "Topics" heading')

    @browsing
    def test_backreferences_without_view_permissions_are_not_visible(self, browser):
        # setup content and relation
        document = create(Builder('document').titled('Foo'))
        browser.login().visit(document, view='edit')
        browser.fill({'form.widgets.ITopicSupportSchema.topics': self.subnode.UID()})
        browser.find('form.buttons.save').click()

        browser.open(self.subnode, view='topic_view')
        foo_logged_in = browser.css(
                '.topic-reference-listings li a').first.text

        self.assertEqual('Foo', foo_logged_in)

        # remove permissions
        document.manage_permission('View', roles=[], acquire=False)
        transaction.commit()

        browser.open(self.subnode, view='topic_view')
        foo_logged_out = browser.css('.topic-reference-listings li a')

        self.assertEqual([], foo_logged_out)

    @browsing
    def test_settings_can_hide_backreferences(self, browser):
        browser.login()

        browser.visit(self.topic_technology)
        self.assertTrue(browser.css('.referenceRepresentationListing'))

        browser.visit(self.topic_technology, view='edit')
        browser.fill({'Show backreferences': False}).submit()

        self.assertFalse(browser.css('.referenceRepresentationListing'))
