from Acquisition import aq_inner
from DateTime import DateTime
from ftw.topics.interfaces import ITopicSupport
from ftw.topics.interfaces import IBackReferenceCollector
from ftw.topics.interfaces import ITopic
from operator import attrgetter
from plone import api
from plone.app.dexterity.behaviors.metadata import IPublication
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore.utils import getToolByName
from zc.relation.interfaces import ICatalog
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.intid.interfaces import IIntIds


@implementer(IBackReferenceCollector)
@adapter(ITopic, Interface)
class DefaultCollector(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.mtool = getToolByName(self.context, 'portal_membership')

    def __call__(self, group_by=INavigationRoot):
        return self._get_brefs_for(self.context)

    def _filter_view_permission(self, obj):
        if self.mtool.checkPermission('View', obj):
            return obj

    def _filter_by_interfaces(self, obj):
        return ITopicSupport.providedBy(obj)

    def _get_brefs_for(self, obj):
        objs = self._get_dx_brefs_for(obj)
        objs = filter(self._filter_view_permission, objs)
        objs = filter(self._filter_by_interfaces, objs)
        objs = filter(self._filter_inactive_content, objs)
        return list(objs)

    def _get_dx_brefs_for(self, obj):
        catalog = getUtility(ICatalog)
        obj_intid = getUtility(IIntIds).getId(aq_inner(obj))
        relations = catalog.findRelations(
            {'to_id': obj_intid,
             'from_attribute': 'topics'}
        )
        return map(attrgetter('from_object'), relations)

    def _filter_inactive_content(self, obj):
        effective_date, expiration_date = None, None
        if IDexterityContent.providedBy(obj):
            effective_date, expiration_date = self._get_dx_publication_dates(obj)

        if not effective_date and not expiration_date:
            return True

        now = DateTime()

        if not api.user.has_permission('Access inactive portal content') and expiration_date:
            if now > expiration_date:
                return False

        if not api.user.has_permission('Access future portal content') and effective_date:
            if now < effective_date:
                return False

        return True

    def _get_dx_publication_dates(self, obj):
        publication = IPublication(obj, None)
        if not publication:  # IPublication is not supported
            return None, None

        effective = publication.effective
        expiration = publication.expires

        # convert from datetime to DateTime as used by archetypes
        return DateTime(effective) if effective else None, \
            DateTime(expiration) if expiration else None
