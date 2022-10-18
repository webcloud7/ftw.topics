from DateTime import DateTime
from ftw.builder import Builder
from ftw.builder import create
from ftw.topics.interfaces import IBackReferenceCollector
from ftw.topics.tests import FunctionalTesting
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface.verify import verifyObject


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
        self.assertEqual([self.doc, ], result)

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

    def test_filterd_by_interface(self):
        folder = create(
            Builder('folder')
            .titled('random content with reference')
            .having(relatedItems=[self.topic1, self.topic2])
        )

        comp = getMultiAdapter((self.topic1, None),
                               IBackReferenceCollector)
        self.assertNotIn(folder, comp())

        comp = getMultiAdapter((self.topic2, None),
                               IBackReferenceCollector)
        self.assertNotIn(folder, comp())

    def test_filterd_by_from_attribute(self):
        folder = create(
            Builder('document')
            .titled('random content with reference and interface')
            .having(relatedItems=[self.topic1, self.topic2])
        )

        comp = getMultiAdapter((self.topic1, None),
                               IBackReferenceCollector)
        self.assertNotIn(folder, comp())

        comp = getMultiAdapter((self.topic2, None),
                               IBackReferenceCollector)
        self.assertNotIn(folder, comp())
