from zope.i18nmessageid import MessageFactory
from plone.app.dexterity.behaviors.metadata import IBasic
from collective.dexteritytextindexer.utils import searchable


_ = MessageFactory('ftw.topics')

# Mark default dexterity title and description as searchable
# This should be later implemented in collective.dexterityindexer,
# see https://github.com/collective/collective.dexteritytextindexer/issues/2
searchable(IBasic, 'title')
searchable(IBasic, 'description')
