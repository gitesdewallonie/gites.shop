from setuptools import setup, find_packages

version = '0.1'

long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(
    name='gites.shop',
    version=version,
    description="Boutique for Gites",
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
      "Environment :: Web Environment",
      "Framework :: Plone",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 2.6",
      "Topic :: Software Development :: Libraries :: Python Modules",
      ],
    keywords='',
    author='',
    author_email='',
    url='http://svn.plone.org/svn/collective/',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['gites', ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'Products.PloneGetPaid',
        'gites.core',
        'getpaid.ogone'
    ],
    extras_require={
        'test': [
            'unittest2',
            'plone.app.testing',
    ]})
