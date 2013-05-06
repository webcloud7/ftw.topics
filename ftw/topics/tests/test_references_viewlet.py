from ftw.topics.interfaces import ITopicBrowserLayer
from ftw.topics.testing import SIMPLELAYOUT_TOPICS_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.Five.browser import BrowserView
from unittest2 import TestCase
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager


class TestReferencesViewlet(TestCase):

    layer = SIMPLELAYOUT_TOPICS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        self.tree = self.portal.get(
            self.portal.invokeFactory('ftw.topics.TopicTree', 'tree'))

        self.topic1 = self.tree.get(
            self.tree.invokeFactory('ftw.topics.Topic', 'topic1',
                                    title="A topic"))
        self.topic2 = self.tree.get(
            self.tree.invokeFactory('ftw.topics.Topic', 'topic2',
                                    title="B topic"))

        self.page = self.portal.get(
            self.portal.invokeFactory('ContentPage', 'page'))

    def tearDown(self):
        super(TestReferencesViewlet, self).tearDown()
        login(self.portal, TEST_USER_NAME)

        self.portal.manage_delObjects(['tree', 'page'])
        logout()

    def _get_viewlet(self, context):
        alsoProvides(context.REQUEST, ITopicBrowserLayer)

        view = BrowserView(context, context.REQUEST)
        manager_name = 'plone.belowcontent'
        manager = queryMultiAdapter(
            (context, context.REQUEST, view),
            IViewletManager,
            manager_name)
        self.failUnless(manager)

        # Set up viewlets
        manager.update()
        name = 'ftw.topics.references'
        return [v for v in manager.viewlets if v.__name__ == name]

    def test_registered(self):
        # Only Registered for ITopicSupport
        self.assertFalse(self._get_viewlet(self.portal))

        self.assertTrue(self._get_viewlet(self.page))

    def test_references(self):
        viewlet = self._get_viewlet(self.page)[0]
        # No references
        self.assertFalse(viewlet.available())

        self.page.Schema()['topics'].set(
            self.page, (self.topic2.UID(), self.topic1.UID()))

        viewlet = self._get_viewlet(self.page)
        result = [
            dict(title='A topic',
                 description='',
                 url=self.topic1.absolute_url()),
            dict(title='B topic',
                 description='',
                 url=self.topic2.absolute_url()), ]
        self.assertEquals(viewlet[0].get_references(), result)

    def test_permission_on_references(self):
        self.page.Schema()['topics'].set(
            self.page, (self.topic2.UID(), self.topic1.UID()))

        self.topic2.manage_permission('View', roles=[], acquire=False)

        viewlet = self._get_viewlet(self.page)
        result = [
            dict(title='A topic',
                 description='',
                 url=self.topic1.absolute_url()), ]
        self.assertEquals(viewlet[0].get_references(), result)
