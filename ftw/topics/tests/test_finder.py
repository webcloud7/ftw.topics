from ftw.testing import MockTestCase
from ftw.topics.finder import DefaultTopicTreeFinder
from ftw.topics.interfaces import ITopicRootFinder
from ftw.topics.testing import ZCML_LAYER
from plone.app.layout.navigation.interfaces import INavigationRoot
from zope.component import queryAdapter
from zope.interface.verify import verifyClass


class TestDefaultTopicTreeFinder(MockTestCase):

    layer = ZCML_LAYER

    def test_implements_interface(self):
        self.assertTrue(ITopicRootFinder.implementedBy(DefaultTopicTreeFinder))
        verifyClass(ITopicRootFinder, DefaultTopicTreeFinder)

    def test_component_registered(self):
        self.assertTrue(queryAdapter(self.create_dummy(), ITopicRootFinder),
                        'DefaultTopicTreeFinder is not registered correctly.')

    def test_finds_navigation_root(self):
        site = self.providing_stub(INavigationRoot)
        self.expect(site.getPhysicalPath()).result(
            ['', 'plone'])

        obj =  self.set_parent(
            self.stub(),
            self.set_parent(self.stub(), site))

        self.replay()

        self.assertEquals(
            DefaultTopicTreeFinder(obj).get_topic_root_path(),
            '/plone')
