# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument

from zope.interface import Interface


class ITopicBrowserLayer(Interface):
    """ftw.topics specific browser layer.
    """


class ITopicTree(Interface):
    """Marker interface for the root object of the topic tree.
    """


class ITopic(Interface):
    """Marker interface for topic objects.
    """


class ITopicRootFinder(Interface):
    """This adapter is used for finding the root of the selectable
    topic trees for the widget.
    Usually all topics in the plone site are referenceable.
    """

    def __init__(context):
        """Adapts any object.
        """

    def get_topic_root_path():
        """Returns the path to the topic root.
        A topic root is usually the parent of the ITopicTree.
        """


class ITopicSupport(Interface):
    """Archetypes object providing this interface are extended
    with an additional reference field "topics" for adding
    references on the topic.
    """
