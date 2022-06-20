from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def uninstalled(portal_setup):
    portal = api.portal.get()

    cleanup_registry(portal)


def cleanup_registry(portal):
    registry = getUtility(IRegistry)
    display_types = list(registry['plone.displayed_types'])
    display_types.remove('ftw.topics.TopicTree')
    display_types.remove('ftw.topics.Topic')
    registry['plone.displayed_types'] = tuple(display_types)
