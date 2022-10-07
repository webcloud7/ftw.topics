from ftw.topics.interfaces import IBackReferenceCollector
from ftw.topics.interfaces import ITopic
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(ITopic, Interface)
class TopicBackreferences(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):

        if not self._is_top_level_context():
            expand = False

        result = {
            "backreferences": {
                "@id": "{}/@backreferences".format(self.context.absolute_url())
            }
        }
        if not expand:
            return result

        collector = getMultiAdapter((self.context, self.request),
                                    IBackReferenceCollector)

        items = []
        for reference in collector():
            item = getMultiAdapter(
                (reference, self.request), ISerializeToJson
            )(include_items=False)
            items.append(item)

        result["backreferences"]["items"] = items
        return result

    def _is_top_level_context(self):
        actual_url = self.context.REQUEST.ACTUAL_URL.removesuffix('/++api++')
        return self.context.absolute_url() == actual_url.removesuffix('/')


class TopicBackreferencesGet(Service):
    def reply(self):
        backreferences = TopicBackreferences(self.context, self.request)
        return backreferences(expand=True)["backreferences"]
