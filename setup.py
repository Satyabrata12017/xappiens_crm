from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in xappiens_crm/__init__.py
from xappiens_crm import __version__ as version

setup(
	name="xappiens_crm",
	version=version,
	description="xappiens_crm",
	author="saty",
	author_email="satyabrata12017@gmmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
