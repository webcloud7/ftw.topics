from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.topics.tests import FunctionalTesting


class TestTopicRestapi(FunctionalTesting):

    def setUp(self):
        super().setUp()
        self.grant('Manager')
        self.createContent()

    @browsing
    def test_backreferences_expandable(self, browser):
        browser.login()
        topic = self.tree.get('manufacturing')
        document = self.portal.get('manufacturing-processes')

        browser.open(document.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})
        self.assertNotIn('backreferences', browser.json['@components'])

        browser.open(topic.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})
        self.assertIn('backreferences', browser.json['@components'])

    @browsing
    def test_node_json_representation(self, browser):
        browser.login()
        topic = self.tree.get('manufacturing')
        document = self.portal.get('manufacturing-processes')

        browser.open(topic.absolute_url() + '?expand=backreferences', method='GET',
                     headers={'Accept': 'application/json'})

        self.assertEqual(
            browser.json['@components']['backreferences']['@id'].replace(':80', ''),
            topic.absolute_url() + '/@backreferences',
        )

        self.assertEqual(
            len(browser.json['@components']['backreferences']['items']),
            1,
        )

        document_json = browser.json['@components']['backreferences']['items'][0]

        browser.open(document.absolute_url(), method='GET',
                     headers={'Accept': 'application/json'})

        self.assertEqual(browser.json, document_json)

    @browsing
    def test_do_not_expand_sub_elements(self, browser):
        document2 = create(Builder('document')
                           .titled('Another document')
                           .having(topics=[self.topic11, ])
                           )
        topic = self.tree.get('manufacturing')

        browser.login()
        query = '?include_items=1&fullobjects=1&expand=backreferences'
        browser.open(topic.absolute_url() + query, method='GET',
                     headers={'Accept': 'application/json'})

        self.assertNotIn('items', browser.json['items'][0]['@components']['backreferences'])
