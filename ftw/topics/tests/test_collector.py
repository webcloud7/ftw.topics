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

        self.assertEquals(
            [
                {'label': u'Plone site',
                 'UID': 'root',
                 'path': '/plone',
                 'objects': [self.doc],
                 'is_current_section': True},

                {'label': 'Sub Site',
                 'UID': self.subsite_uid,
                 'path': '/plone/foo/subsite',
                 'objects': [self.subsite_doc]}],
            result)

    def test_SUBSITE_calling_returns_result(self):
        comp = getMultiAdapter((self.subsite_node, None),
                               IBackReferenceCollector)
        result = comp()

        self.assertEquals(
            [
                {'label': u'Plone site',
                 'UID': 'root',
                 'path': '/plone',
                 'objects': [self.doc]},

                {'label': 'Sub Site',
                 'UID': self.subsite_uid,
                 'path': '/plone/foo/subsite',
                 'objects': [self.subsite_doc],
                 'is_current_section': True}],
            result)

    def test_get_sections(self):
        comp = getMultiAdapter((self.node, None), IBackReferenceCollector)
        self.assertEquals(
            [
                {'label': u'Plone site',
                 'UID': 'root',
                 'path': '/plone',
                 'objects': [],
                 'is_current_section': True},

                {'label': 'Sub Site',
                 'UID': self.subsite_uid,
                 'objects': [],
                 'path': '/plone/foo/subsite'},

                {'label': "Empty sub site",
                 'UID': self.empty_subsite_uid,
                 'objects': [],
                 'path': '/plone/empty-subsite'}],
            comp.get_sections())

    def test_get_brefs_per_section(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)
        result = comp._get_brefs_per_section()

        self.assertEquals(
            [
                {'label': u'Plone site',
                 'UID': 'root',
                 'path': '/plone',
                 'objects': [self.doc],
                 'is_current_section': True},

                {'label': 'Sub Site',
                 'UID': self.subsite_uid,
                 'path': '/plone/foo/subsite',
                 'objects': [self.subsite_doc]}],
            result)

    def test_SUBSITE_get_brefs_per_section(self):
        comp = getMultiAdapter((self.subsite_node, None),
                               IBackReferenceCollector)
        result = comp._get_brefs_per_section()

        self.assertEquals(
            [
                {'label': u'Plone site',
                 'UID': 'root',
                 'path': '/plone',
                 'objects': [self.doc]},

                {'label': 'Sub Site',
                 'UID': self.subsite_uid,
                 'path': '/plone/foo/subsite',
                 'objects': [self.subsite_doc],
                 'is_current_section': True}],
            result)

    def test_get_merged_brefs(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)

        result = comp._get_merged_brefs()
        self.assertIn(self.doc, result)
        self.assertIn(self.subsite_doc, result)

    def test_SUBSITE_get_merged_brefs(self):
        comp = getMultiAdapter((self.subsite_node, None),
                               IBackReferenceCollector)

        result = comp._get_merged_brefs()
        self.assertIn(self.doc, result)
        self.assertIn(self.subsite_doc, result)

    def test_get_similar_topic_objects(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)

        result = comp._get_similar_topic_objects()
        self.assertIn(self.node, result)
        self.assertIn(self.subsite_node, result)

    def test_SUBSITE_get_similar_topic_objects(self):
        comp = getMultiAdapter((self.subsite_node, None),
                               IBackReferenceCollector)

        result = comp._get_similar_topic_objects()
        self.assertIn(self.node, result)
        self.assertIn(self.subsite_node, result)

    def test_exclude_expired_content(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)

        self.assertIn(self.doc, comp._get_merged_brefs())

        self.doc.setExpirationDate(DateTime() - 10)
        self.doc.reindexObject()

        self.assertNotIn(self.doc, comp._get_merged_brefs())

    def test_exclude_future_content(self):
        comp = getMultiAdapter((self.node, None),
                               IBackReferenceCollector)

        self.assertIn(self.doc, comp._get_merged_brefs())

        self.doc.setEffectiveDate(DateTime() + 10)
        self.doc.reindexObject()

        self.assertNotIn(self.doc, comp._get_merged_brefs())
