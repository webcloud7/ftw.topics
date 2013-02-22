from ftw.testing import MockTestCase
from ftw.topics.browser.representation import DefaultRepresentation
from ftw.topics.interfaces import ITopicReferencePresentation
from ftw.topics.testing import ZCML_LAYER
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface.verify import verifyClass


class TestDefaultReferenceRepresentation(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestDefaultReferenceRepresentation, self).setUp()

        self.request = self.stub_request()
        self.context = self.create_dummy()

    def test_implements_interface(self):
        self.replay()

        self.assertTrue(
            ITopicReferencePresentation.implementedBy(DefaultRepresentation))
        verifyClass(ITopicReferencePresentation, DefaultRepresentation)

    def test_component_registered(self):
        self.replay()

        self.assertTrue(
            queryMultiAdapter(
                (self.context, self.request),
                ITopicReferencePresentation, name="default_representation"),
            'DefaultRepresentation is not registered correctly.')

    def test_default_consum(self):
        objects = [self.create_dummy(), self.create_dummy()]
        self.replay()

        adapter = getMultiAdapter(
            (self.context, self.request),
            ITopicReferencePresentation, name="default_representation"),
        # Default representation adapter consume everything
        adapter[0].consume(objects)

        self.assertEquals(len(adapter[0].objects),
                          len(objects))

    def test_render(self):
        objects = [
            self.create_dummy(absolute_url=lambda: '/path1',
                              title_or_id='Title 1'),
            self.create_dummy(absolute_url=lambda: '/path2',
                              title_or_id='Title 2')]

        self.replay()

        adapter = getMultiAdapter(
            (self.context, self.request),
            ITopicReferencePresentation, name="default_representation"),
        # Default representation adapter consume everything
        adapter[0].consume(objects)

        rendered = adapter[0].render()

        self.assertIn('Title 1', rendered)
        self.assertIn('Title 2', rendered)
        self.assertIn('/path1', rendered)
        self.assertIn('/path2', rendered)


# class TestContentPageReferenceRepresentation(MockTestCase):

