from setuptools import setup

setup(
    name='rillian-grant-university-project-covid19-dashboard',
    version='1.0.1',
    long_description=__doc__,
    url='https://github.com/Rillian-Grant/university-project-covid19-covid19_dashboard.git',
    author='Rillian Grant',
    author_email='rillian.grant@gmail.com',
    license='GPLv3',
    packages=['covid19_dashboard'],
    include_package_data=True,
    package_data={
        'covid19_dashboard': ["static/*", "templates/*"]
    },
    zip_safe=False,
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
    entry_points={
        "console_scripts": [
            "covid19-dashboard = covid19_dashboard:run_app"
        ]
    }
)