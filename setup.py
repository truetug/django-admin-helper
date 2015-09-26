#!/usr/bin/env python

from setuptools import setup, find_packages
from admin_helper import VERSION

repo_url = 'https://github.com/truetug/django-admin-helper'
long_desc = '''
%s
%s
''' % (open('README.md').read(), open('CHANGELOG').read())

setup(
    name='django-admin-helper',
    version=VERSION.replace(' ', '-'),
    description='A tool for the django to list users and authorization as any of them from user interface',
    long_description=long_desc,
    author='Sergey Trofimov',
    author_email='truetug@gmail.com',
    url=repo_url,
    download_url='https://pypi.python.org/packages/source/d/django-admin-helper/django-admin-helper-%s.tar.gz' % VERSION,
    packages=find_packages(exclude=['test_proj*']),
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False,
)
