from setuptools import setup

setup(
    name='rillian-grant-university-project-covid19-dashboard',
    version='1.0.0',
    description='My covid19 dashboard university project',
    url='https://github.com/Rillian-Grant/university-project-covid19-dashboard.git',
    author='Rillian Grant',
    author_email='rillian.grant@gmail.com',
    license='GPLv3',
    packages=['dashboard'],
    install_requires=[
        'Flask==2.0.2',
        'uk-covid19==1.2.2'
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)