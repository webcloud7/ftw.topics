from ftw.testing import MockTestCase
from ftw.topics.browser import tree
from ftw.topics.testing import TOPICS_FUNCTIONAL_TESTING
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.dexterity.utils import createContentInContainer
from plone.testing.z2 import Browser
from pyquery import PyQuery
from unittest2 import TestCase
import transaction


class TestHelperFunctions(MockTestCase):

    def setUp(self):
        super(TestHelperFunctions, self).setUp()

        self.brain_mocks = [
            self.create_dummy(Title='Foo',
                              getPath=lambda: '/plone/foo',
                              getURL=lambda: 'http://nohost/plone/foo'),

            self.create_dummy(Title='Bar',
                              getPath=lambda: '/plone/foo/bar',
                              getURL=lambda: 'http://nohost/plone/foo/bar'),

            self.create_dummy(Title='Baz',
                              getPath=lambda: '/plone/foo/baz',
                              getURL=lambda: 'http://nohost/plone/foo/baz')]

    def test_get_brain_data(self):
        self.assertEqual(map(tree.get_brain_data, self.brain_mocks),

                         [{'title': 'Foo',
                           'path': '/plone/foo',
                           'url': 'http://nohost/plone/foo',
                           'children': []},

                          {'title': 'Bar',
                           'path': '/plone/foo/bar',
                           'url': 'http://nohost/plone/foo/bar',
                           'children': []},

                          {'title': 'Baz',
                           'path': '/plone/foo/baz',
                           'url': 'http://nohost/plone/foo/baz',
                           'children': []}])

    def test_make_treeish(self):
        data = map(tree.get_brain_data, self.brain_mocks)

        self.maxDiff = None
        self.assertEqual(
            tree.make_treeish(data),

            [{'title': 'Foo',
              'path': '/plone/foo',
              'url': 'http://nohost/plone/foo',

              'children': [

                        {'title': 'Bar',
                         'path': '/plone/foo/bar',
                         'url': 'http://nohost/plone/foo/bar',
                         'children': []},

                        {'title': 'Baz',
                         'path': '/plone/foo/baz',
                         'url': 'http://nohost/plone/foo/baz',
                         'children': []},

                        ]},
             ])


class TestTreeView(TestCase):

    layer = TOPICS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.tree = createContentInContainer(self.portal,
                                             'ftw.topics.TopicTree',
                                             title='Topics')

        node1 = createContentInContainer(self.tree, 'ftw.topics.Topic',
                                         title='Manufacturing')
        node1a = createContentInContainer(node1, 'ftw.topics.Topic',
                                          title='Agile Manufacturing')
        createContentInContainer(node1a, 'ftw.topics.Topic',
                                 'Benchmarks')

        node2 = createContentInContainer(self.tree, 'ftw.topics.Topic',
                                         title='Telecom')
        node2a = createContentInContainer(node2, 'ftw.topics.Topic',
                                          title='Billing')
        createContentInContainer(node2a, 'ftw.topics.Topic',
                                 'Customers')

        transaction.commit()

        self.browser = Browser(self.layer['app'])
        self.browser.addHeader('Authorization', 'Basic %s:%s' % (
                TEST_USER_NAME, TEST_USER_PASSWORD,))
        self.browser.handleErrors = False

    def test_tree_view(self):
        self.browser.open(self.tree.absolute_url())
        doc = PyQuery(self.browser.contents)

        # "Benchmarks" and "Customers" are level 3 - should not be visible
        self.assertNotIn('Benchmarks', self.browser.contents)
        self.assertNotIn('Customers', self.browser.contents)

        # there should be two columns
        columns = doc('#content .listing-column')
        self.assertEquals(len(columns), 2, 'Expected exactly two columns')

        # "Telecom" should be in the first column,
        self.assertEqual(columns.eq(0).find('h2 a:first').text(),
                         'Telecom')

        # "Manufacturing" in the second.
        # This is because it's sorted by title.
        self.assertEqual(columns.eq(1).find('h2 a:first').text(),
                         'Manufacturing')
