from ftw.testing import MockTestCase
from ftw.topics.finder import DefaultTopicTreeFinder
from ftw.topics.interfaces import ITopicRootFinder
from ftw.topics.testing import ZCML_LAYER
from zope.component import queryMultiAdapter
from zope.component.hooks import setSite
from zope.interface.verify import verifyClass


class TestDefaultTopicTreeFinder(MockTestCase):

    layer = ZCML_LAYER

    def test_implements_interface(self):
        self.assertTrue(ITopicRootFinder.implementedBy(DefaultTopicTreeFinder))
        verifyClass(ITopicRootFinder, DefaultTopicTreeFinder)

    def test_component_registered(self):
        self.assertTrue(
            queryMultiAdapter((self.create_dummy(), None), ITopicRootFinder),
            'DefaultTopicTreeFinder is not registered correctly.')

    def test_finds_navigation_root(self):
        site = self.stub()
        self.expect(site.getPhysicalPath()).result(
            ['', 'plone'])

        setSite(site)

        obj =  self.set_parent(
            self.stub(),
            self.set_parent(self.stub(), site))

        self.replay()

        self.assertEquals(
            DefaultTopicTreeFinder(obj, None).get_topic_root_path(),
            '/plone')
