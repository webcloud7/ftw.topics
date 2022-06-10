from ftw.topics import _
from ftw.topics.interfaces import ITopicRootFinder
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.relationfield.schema import RelationList
from zope.component import getMultiAdapter
from zope.interface import provider
from plone.app.relationfield.event import extract_relations
from z3c.relationfield.event import _setRelation


def get_topic_root(widget):
    finder = getMultiAdapter((widget.context, widget.request),
                             ITopicRootFinder)
    return finder.get_topic_root_path()


@provider(IFormFieldProvider)
class ITopicSupportSchema(model.Schema):
    """Schema interface for the `ITopicSupport` behavior, adding
    a reference field `topics` to the content type.
    """
    directives.write_permission(topics='ftw.topics.SetTopicReference')
    topics = RelationList(
        title=_('label_topics', default='Topics'),
        required=False,
    )



# From: https://github.com/4teamwork/opengever.core/commit/88e015d
def add_behavior_relations(obj, event):
    """Register relations in behaviors.

    This event handler fixes a bug in plone.app.relationfield, which only
    updates the zc.catalog when an object gets modified, but not when it gets
    added.
    """
    for behavior_interface, name, relation in extract_relations(obj):
        _setRelation(obj, name, relation)
