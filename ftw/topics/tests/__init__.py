from ftw.builder import Builder
from ftw.builder import create
from ftw.topics.testing import TOPICS_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest import TestCase
import transaction
import ftw.topics.tests.builders  # noqa


class FunctionalTesting(TestCase):
    layer = TOPICS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def createContent(self):
        self.tree = create(Builder('topic tree').titled('Topics'))
        self.topic1 = create(Builder('topic').titled('Manufacturing').within(self.tree))
        self.topic11 = create(Builder('topic').titled('Agile Manufacturing').within(self.topic1))
        self.topic12 = create(Builder('topic').titled('Quality').within(self.topic1))
        self.topic2 = create(Builder('topic').titled('Technology').within(self.tree))

        self.document = create(Builder('document')
                               .titled('Manufacturing processes')
                               .having(topics=[self.topic1, self.topic2])
                               )

    def grant(self, *roles):
        setRoles(self.portal, TEST_USER_ID, list(roles))
        transaction.commit()
