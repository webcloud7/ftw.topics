from ftw.testbrowser import browsing
from ftw.testbrowser.pages import factoriesmenu
from ftw.topics.interfaces import ITopic
from ftw.topics.interfaces import ITopicTree
from ftw.topics.tests import FunctionalTesting


class TestContentTypeCreation(FunctionalTesting):

    def setUp(self):
        super().setUp()
        self.grant('Manager')

    @browsing
    def test_create_topic_tree(self, browser):
        browser.login().open(self.portal)
        factoriesmenu.add('Topic Tree')
        browser.fill({'Title': 'Topical'})
        browser.find_button_by_label('Save').click()

        self.assertTrue(
            browser.url.endswith('topical/view'),
            'Should be on "topical" view, but url is: %s' % (
                browser.url))
        self.assertIn('Topical', browser.contents)

        tree = self.portal.get('topical')
        self.assertTrue(ITopicTree.providedBy(tree))

    @browsing
    def test_create_topic(self, browser):
        # first create a tree
        browser.login().visit(self.portal)
        factoriesmenu.add('Topic Tree')
        browser.fill({'Title': 'Topical'})
        browser.find_button_by_label('Save').click()

        factoriesmenu.add('Topic')
        browser.fill({'Title': 'Manufacturing'})
        browser.find_button_by_label('Save').click()

        self.assertEqual(browser.url,
                         'http://nohost/plone/topical/manufacturing/view')
        self.assertIn('Manufacturing', browser.contents)

        topic = self.portal.get('topical').get('manufacturing')
        self.assertTrue(ITopic.providedBy(topic))
