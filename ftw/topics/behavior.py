from ftw.topics import _
from ftw.topics.interfaces import ITopicRootFinder
from plone.app.relationfield.event import extract_relations
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives.form import widget
from plone.formwidget.contenttree import MultiContentTreeFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.formwidget.contenttree.utils import closest_content
from z3c.relationfield.event import _setRelation
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.component import getMultiAdapter
from zope.interface import alsoProvides
from zope.interface import Interface


class TopicsObjPathSourceBinder(ObjPathSourceBinder):

    def __call__(self, context):
        if not self.navigation_tree_query:
            self.navigation_tree_query = {}

        finder = getMultiAdapter((context, context.REQUEST),
                                 ITopicRootFinder)
        self.navigation_tree_query['path'] = {
            'query': finder.get_topic_root_path()}

        return self.path_source(
            closest_content(context),
            selectable_filter=self.selectable_filter,
            navigation_tree_query=self.navigation_tree_query)


class ITopicSupportSchema(Interface):
    """Schema interface for the `ITopicSupport` behavior, adding
    a reference field `topics` to the content type.
    """

    widget(topics=MultiContentTreeFieldWidget)
    topics = RelationList(
        title=_(u'label_topics', default=u'Topics'),
        value_type=RelationChoice(
            source=TopicsObjPathSourceBinder(
                # portal_type=['ftw.topics.Topic']
                )))


alsoProvides(ITopicSupportSchema, IFormFieldProvider)


# From: https://github.com/4teamwork/opengever.core/commit/88e015d
def add_behavior_relations(obj, event):
    """Register relations in behaviors.

    This event handler fixes a bug in plone.app.relationfield, which only
    updates the zc.catalog when an object gets modified, but not when it gets
    added.
    """
    for behavior_interface, name, relation in extract_relations(obj):
        _setRelation(obj, name, relation)
