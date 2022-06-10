from ftw.topics.interfaces import ITopicBrowserLayer
from plone.browserlayer.utils import registered_layers
from ftw.topics.tests import FunctionalTesting


class TestBrowserLayer(FunctionalTesting):

    def test_request_layer_active(self):
        layers = registered_layers()
        self.assertIn(ITopicBrowserLayer, layers)
