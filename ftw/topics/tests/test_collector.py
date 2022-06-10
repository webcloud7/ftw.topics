from DateTime import DateTime
from ftw.topics.interfaces import IBackReferenceCollector
from plone.uuid.interfaces import IUUID
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface.verify import verifyObject
from ftw.topics.tests import FunctionalTesting


class TestDefaultCollector(FunctionalTesting):

    def setUp(self):
        self.portal = self.layer['portal']
        self.createContent()
        self.tree = self.portal.get('topics')
        self.node = self.tree.get('manufacturing')
        self.doc = self.portal.get('manufacturing-processes')

    def test_component_registered(self):
        self.assertTrue(
            queryMultiAdapter((self.node, None), IBackReferenceCollector),
            'No default IBackReferenceCollector adapter registered.')

    def test_component_implements_interface(self):
        comp = getMultiAdapter((self.node, None), IBackReferenceCollector)
        self.assertTrue(IBackReferenceCollector.providedBy(comp))
        verifyObject(IBackReferenceCollector, comp)

    def test_calling_returns_result(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)
        result = comp()
        self.assertEquals([self.doc, ], result)
        
    def test_exclude_expired_content(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)

        self.assertIn(self.doc, comp())

        self.doc.setExpirationDate(DateTime() - 10)
        self.doc.reindexObject()

        self.assertNotIn(self.doc, comp())

    def test_exclude_future_content(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)

        self.assertIn(self.doc, comp())

        self.doc.setEffectiveDate(DateTime() + 10)
        self.doc.reindexObject()

        self.assertNotIn(self.doc, comp())
