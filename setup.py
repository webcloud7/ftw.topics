import os
from setuptools import setup, find_packages


version = '3.0.0.dev0'


extras_require = {
    'restapi': [
        'plone.restapi',
    ]
}


tests_require = [
    'ftw.testing',
    'ftw.testbrowser',
    'ftw.builder',
]

extras_require['tests'] = tests_require + extras_require['restapi']


setup(name='ftw.topics',
      version=version,
      description='Create subject trees in Plone',

      long_description=open('README.rst').read() + '\n' +
      open(os.path.join('docs', 'HISTORY.txt')).read(),

      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 6.0",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.9",
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],

      keywords='ftw topics',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.topics',

      license='GPL2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw', ],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
          'setuptools',
          'ftw.referencewidget',
          'Plone',
          'ftw.upgrade',
      ],

      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [plone.autoinclude.plugin]
      target = plone
      """,
      )
