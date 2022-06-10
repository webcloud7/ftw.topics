from ftw.testbrowser import browsing
from ftw.topics.tests import FunctionalTesting
from ftw.topics.interfaces import IBackReferenceCollector
from plone.dexterity.fti import DexterityFTI
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
import transaction


class TestTopicSupportBehavior(FunctionalTesting):

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        self.grant('Manager')
        self.createContent()

        portal_types = getToolByName(self.portal, 'portal_types')

        fti = DexterityFTI('DxTopicSupport')
        fti.behaviors = (
            'plone.app.dexterity.behaviors.metadata.IBasic',
            'plone.app.content.interfaces.INameFromTitle',
            'ftw.topics.behavior.ITopicSupportSchema',)
        portal_types._setObject('DxTopicSupport', fti)
        fti.lookupSchema()
        transaction.commit()

    @browsing
    def test_behavior(self, browser):
        browser.login().open(self.portal.portal_url() + '/++add++DxTopicSupport')
        browser.fill({
            'Title': u'My Object',
            'form.widgets.ITopicSupportSchema.topics': self.topic12.UID(),
        })
        browser.find_button_by_label('Save').click()
        obj = self.portal.get('my-object')
       
        collector = getMultiAdapter((self.topic12, self.request),
                                    IBackReferenceCollector)
        objects = collector()
        self.assertCountEqual((obj,), objects)

    @browsing
    def test_write_permission(self, browser):
        # Create a content item having topic references.
        browser.login().open(self.portal.portal_url() + '/++add++DxTopicSupport')
        browser.fill({
            'Title': u'My Object',
            'form.widgets.ITopicSupportSchema.topics': '/plone/topics/manufacturing/quality',
        }).save()
        # The user sees the topic field on the edit form.
        obj = self.portal.get('my-object')
        browser.visit(obj, view='edit')
        expected = sorted([
            'form.widgets.IBasic.description',
            'form.widgets.IBasic.title',
            'form.widgets.ITopicSupportSchema.topics',
            ])
        actual = sorted([field for field in browser.forms['form'].fields.keys()
                         if field in expected])

        self.assertEqual(expected, actual)

        # Remove the permission to set topic references.
        self.portal.manage_permission('ftw.topics: Set Topic Reference', roles=[], acquire=False)
        transaction.commit()
        # The user no longer sees the topic field on the edit form.
        browser.login().visit(obj, view='edit')
        expected2 = sorted([
            'form.widgets.IBasic.description',
            'form.widgets.IBasic.title',
            ])
        actual2 = sorted([field for field in browser.forms['form'].fields.keys()
                         if field in expected])

        # Make sure anything else than the behavior is still there
        self.assertEqual(expected2, actual2)

        # Test that behavior is not there anymore
        self.assertNotIn(
            'form.widgets.ITopicSupportSchema.topics',
            browser.forms['form'].fields.keys())
