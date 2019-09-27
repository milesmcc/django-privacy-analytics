import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-privacy-analytics',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # example license
    description='Privacy-focused, performant, and server-side analytics for your Django project',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/milesmcc/django-privacy-analytics/',
    author='R. Miles McCain',
    author_email='opensource@sendmiles.email',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)