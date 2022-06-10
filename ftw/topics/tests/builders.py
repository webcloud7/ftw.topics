from ftw.builder import builder_registry
from ftw.builder.dexterity import DexterityBuilder


class TopicTreeBuilder(DexterityBuilder):
    portal_type = 'ftw.topics.TopicTree'


builder_registry.register('topic tree', TopicTreeBuilder, force=True)


class TopicBuilder(DexterityBuilder):
    portal_type = 'ftw.topics.Topic'


builder_registry.register('topic', TopicBuilder, force=True)
