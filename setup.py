import setuptools

# Set the VERSION variable by sourcing this one line python file.
exec(open('OpenAFSLibrary/__version__.py').read())

setuptools.setup(
    name='robotframework_openafslibrary',
    version=VERSION,
    description='Robot Framework test library for OpenAFS',
    long_description=open('README.rst').read(),
    author='Michael Meffie',
    author_email='mmeffie@sinenomine.net',
    url='https://github.com/openafs-contrib/robotframework-openafslibrary',
    license='BSD-2-Clause',
    packages=[
        'OpenAFSLibrary',
        'OpenAFSLibrary.keywords',
    ],
    install_requires=[
        'robotframework>=6.1.1',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
    ],
)

