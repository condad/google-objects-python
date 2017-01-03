from distutils.core import setup


version = '0.0.1'
requires = ['google-api-python-client>=1.5.3']
test_requirements = ['pytest>=2.8.0']


setup(
    name='google_objects',
    packages=['google_objects'],
    version=version,
    description='A simple OO wrapper around google\'s python API client',
    author='Connor Sullivan',
    author_email='sully4792@gmail.com',
    install_requires=requires,
    tests_require=test_requirements,
    url='https://github.com/theconnor/google-objects',
    download_url='https://github.com/theconnor/google-objects/tarball/' + version,
    keywords=['google', 'api', 'wrapper'],
    classifiers=[],
)
