ftw.topics
==========

This package integrates a subject tree into Plone.

Features
--------

- Dexterity based content types "Topic Tree" and "Topic" for
  creating a topic tree (subject tree).

- Archetypes schema extender, adding a reference field "topics" to
  all objects prividing `ITopicSupport` for assigning content to
  a topic.

- The topic-view lists all content referenced the topic.

- `Simplelayout`_ support for topics, so that additional content
  can be added to the topic view.


Usage
-----

- Add ``ftw.topics`` to your buildout configuration:

.. code:: ini

    [instance]
    eggs +=
        ftw.topics

- Install the default generic import profile.


ITopicSupport for Archetypes
----------------------------

For activating the schema extender install the `archetypes` extras:

.. code:: ini

    [instance]
    eggs +=
        ftw.topics [archetypes]


Enable the `ITopicSupport` interface on the archetypes content type classes
you want to have the `topics` reference field:


.. code:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        i18n_domain="my.package">

        <class class="my.package.content.mytype.MyTyp">
            <implements interface="ftw.topics.interfaces.ITopicSupport" />
        </class>

    </configure>

If you have `ftw.contentpage`_ installed, `ITopicSupport` is automatically enabled
for content pages.


ITopicSupport for Dexterity
---------------------------

If you would like to have the topics field on dexterity based types, use
the `ITopicSupportSchema` behavior:

.. code:: xml

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       xmlns:i18n="http://xml.zope.org/namespaces/i18n"
       i18n:domain="example.conference">

         <!-- enabled behaviors -->
         <property name="behaviors">
             <element value="ftw.topics.behavior.ITopicSupportSchema" />
         </property>

    </object>



Simplelayout support
--------------------

The `Simplelayout`_ support is using the block types of the `ftw.contentpage`_
package, so it installs the contentpage package.
Use the `simplelayout` extras for installing the required packages:

.. code:: ini

    [instance]
    eggs +=
        ftw.topics [simplelayout]

Install the simplelayout generic setup profile (`profile-ftw.topics:simplelayout`).


Customizing reference representations
-------------------------------------
First there's a default representation adapter for all content which does not have
a specific adapter registered. It just lists the referenced items as link list.

Second there's is a ``ContentPage``specific representation adapter which renders
all ``ContentPage`` content in a seperate section on the topic view.

If you want your own representation of a specific content you have to register your
own representation adapter.

1. Create a MultiAdapter which inherhits from `DefaultRepresentation`,
  this way the `ITopicReferencePresentation` is already implemented.
  Checkout the `ContentPageRepresentation` adapter

2. Override the consume function, basically replace the check for the
  content marker interface, or however you regonize your content.

3. Override the title and position function.

Some further informations:
The position of the representation adapters is defined by the return value
of the position function:

- DefaultRepresentation adapter: 1000
- ContentPageRepresentation: 100

The title will be show as groupt title on the topic view.


Links
-----

- Main github project repository: https://github.com/4teamwork/ftw.topics
- Issue tracker: https://github.com/4teamwork/ftw.topics/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.topics
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.topics


Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.topics`` is licensed under GNU General Public License, version 2.
