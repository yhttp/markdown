import os.path
import re

from setuptools import setup, find_namespace_packages


# Reading package's version (same way sqlalchemy does)
with open(
    os.path.join(os.path.dirname(__file__), 'yhttp/markdown', '__init__.py')
) as v_file:
    package_version = \
        re.compile('.*__version__ = \'(.*?)\'', re.S)\
        .match(v_file.read())\
        .group(1)


dependencies = [
    'yhttp >= 7.0.1, < 8',
    'pymlconf',
    'easycli',
    'markdown2',
    'mako',
    'pygments',
    'libsass',
]


setup(
    name='yhttp-markdown',
    version=package_version,
    author='Vahid Mardani',
    url='https://github.com/yhttp/markdown',
    description='Markdown to HTML coverter and server with yhttp.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # This is important!
    license='APLv1',
    install_requires=dependencies,
    dependency_links=[
    ],
    packages=find_namespace_packages(
        where='.',
        include=['yhttp.markdown'],
        exclude=['tests']
    ),
    include_package_data=True,
    package_data={'yhttp.markdown': [
        'yhttp/markdown/templates',
        'yhttp/markdown/static',
        'yhttp/markdown/styles',
        'yhttp/markdown/defaultmetadata',
    ]},
    entry_points={
        'console_scripts': [
            'yhttp-markdown = yhttp.markdown.server:app.climain'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Development Status :: 5 - Production/Stable',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
