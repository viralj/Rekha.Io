from setuptools import setup, find_packages

"""
Created by Viral Joshi.
"""

INSTALL_REQUIREMENTS = [
    'Django>=2.0',
    'mysqlclient>=1.3.10',
    'setuptools>=36.2.2',
    'pytz>=2017.2',
    'django_compressor>=2.2',
    'PyReact==0.6.0',
    'django-pipeline==1.6.13',
]

CLASSIFIERS = [
    'Development Status :: 1 - Development',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Programming Language :: Python :: 3.6',
    'Framework :: Django',
    'Framework :: Django :: 2.0',
]

setup(
    author='Viral Joshi and contributors',
    author_email='',
    name='Rekha.Io',
    version='1.0.0',
    description='Rekha.Io : Open Source project to share programming skills',
    url='https://github.com/viralj/Rekha.Io',
    license='',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIREMENTS,
    packages=find_packages(exclude=['project', 'project.*']),
    include_package_data=True,
    zip_safe=False,
)
