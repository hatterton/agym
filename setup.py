import os
import configparser

from os.path import (join, dirname)
from setuptools import find_packages, setup
from setuptools.command.install import install


# class InstallCommand(install):
#     """Customized setuptools install command - inits configuration file."""

#     def run(self):
#         # init configuration file
#         config = configparser.ConfigParser()
#         config.read('console_tea/default_configuration.ini')

#         init_tea_directory()
#         with open(get_default_config_path(), 'w') as f:
#             config.write(f)

#         super().run()


# def init_tea_directory():
#     dir_path = os.path.join(os.path.expanduser('~'), '.tea')
#     if not os.path.exists(dir_path):
#         os.mkdir(dir_path)


with open('requirements.txt') as f:
    requirements = list(f)

setup(
    # cmdclass={
    #     'install': InstallCommand
    # },
    name='agym',
    version='1.0',
    packages=find_packages(),
    package_dir={
        './src/agym': 'agym',
    },
    # test_suite="tea.tests.test_runner.get_test_suite",

    long_description=open(join(dirname(__file__), 'README.md')).read(),
    entry_points={
        'console_scripts':
            [
                'run_agym = agym.agym:run_app',
            ],
    },
    install_requires=requirements
)
