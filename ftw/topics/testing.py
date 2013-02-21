from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import ploneSite
from plone.testing import Layer
from plone.testing import z2
from plone.testing import zodb
from zope.configuration import xmlconfig


class TopicsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import z3c.autoinclude
        xmlconfig.file('meta.zcml', z3c.autoinclude,
                       context=configurationContext)
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <includePlugins package="plone" />'
            '</configure>',
            context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.topics:default')


TOPICS_FIXTURE = TopicsLayer()
TOPICS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TOPICS_FIXTURE, ), name='ftw.topics:integration')
TOPICS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TOPICS_FIXTURE, ), name='ftw.topics:functional')


class SimplelayoutTopicsLayer(Layer):

    defaultBases = (TOPICS_FIXTURE, )

    def setUp(self):
        # Stack a new DemoStorage
        self['zodbDB'] = zodb.stackDemoStorage(
            self.get('zodbDB'), name='SimplelayoutTopicsLayer')

        with z2.zopeApp() as app:
            z2.installProduct(app, 'simplelayout.types.common')
            z2.installProduct(app, 'ftw.contentpage')

        with ploneSite() as portal:
            applyProfile(portal, 'ftw.topics:simplelayout')

    def tearDown(self):
        # Zap the stacked ZODB
        self['zodbDB'].close()
        del self['zodbDB']


SIMPLELAYOUT_TOPICS_FIXTURE = SimplelayoutTopicsLayer()
SIMPLELAYOUT_TOPICS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SIMPLELAYOUT_TOPICS_FIXTURE, ),
    name='ftw.topics:sl:integration')
SIMPLELAYOUT_TOPICS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SIMPLELAYOUT_TOPICS_FIXTURE, ),
    name='ftw.topics:sl:functional')
