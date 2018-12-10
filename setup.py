from setuptools import setup, find_packages

requires = [
    'plaster_pastedeploy==0.6.*',
    'pyramid==1.9.*',
    'pyramid_debugtoolbar==4.5.*',
    'waitress==1.1.*',
    'SQLAlchemy==1.2.*',
    'zope.sqlalchemy==1.0.*',
    'dependency_injector==3.14.*'
]

tests_require = [
    'WebTest==2.0.*',
    'pytest==3.9.*',
    'pytest-cov==2.6.*',
]

setup(
    name='hackathon_la',
    version='0.0',
    description='hackathon_la-iq',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = bundelz_iq:main',
        ],
    },
)
