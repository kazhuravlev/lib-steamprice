from distutils.core import setup

with open('./requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name='lib_steamprice',
    version='2.0.0',
    packages=['lib_steamprice'],
    url='https://bitbucket.org/DJon1/lib-steamprice',
    license='',
    author='Zhuravlev Kirill',
    author_email='kazhuravlev@fastmail.com',
    maintainer_email='kazhuravlev@fastmail.com',
    description='SteamPrice.pro client library',
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
