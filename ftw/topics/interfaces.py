# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument

from zope.interface import Interface


class ITopicTree(Interface):
    """Marker interface for the root object of the topic tree.
    """


class ITopic(Interface):
    """Marker interface for topic objects.
    """
