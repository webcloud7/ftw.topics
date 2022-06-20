from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from ftw.testing.layer import ComponentRegistryLayer
from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from zope.configuration import xmlconfig


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()
        import ftw.topics
        self.load_zcml_file('tests.zcml', ftw.topics.tests)
        self.load_zcml_file('configure.zcml', ftw.topics)


ZCML_LAYER = ZCMLLayer()


class TopicsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        # self.loadZCML(package=wcs.simplelayout)
        # self.loadZCML(package=plone.restapi)

        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="plone.autoinclude" file="meta.zcml" />'
            '  <autoIncludePlugins target="plone" />'
            '  <autoIncludePluginsOverrides target="plone" />'
            '</configure>',
            context=configurationContext)

    def add_behaviors(self, type_to_configure, *additional_behaviors):
        fti = api.portal.get().portal_types.get(type_to_configure)
        behaviors = list(fti.behaviors)
        behaviors += list(additional_behaviors)
        fti.behaviors = tuple(set(behaviors))

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.topics:default')
        applyProfile(portal, 'plone.restapi:default')
        self.add_behaviors('Document', 'ftw.topics.behavior.ITopicSupportSchema')


TOPICS_FIXTURE = TopicsLayer()
TOPICS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(
        TOPICS_FIXTURE,
        set_builder_session_factory(functional_session_factory),
    ), name='ftw.topics:functional')
