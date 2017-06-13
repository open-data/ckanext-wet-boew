from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-wet-boew',
	version=version,
	description="Integrate the Web Experience Toolkit into CKAN 2.0",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Ross Thompson',
	author_email='ross.thompson@statcan.gc.ca',
	url='https://github.com/wet-boew/wet-boew',
	license='Crown Copyright, Government of Canada, and is distributed under the MIT License',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.wet_boew'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
    [ckan.plugins]
	# Add plugins here, eg
	wet_boew=ckanext.wet_boew.plugins:WetTheme
    wet_boew_theme_gc_intranet=ckanext.wet_boew.plugins:GCIntranetTheme
    wet_boew_gcweb=ckanext.wet_boew.plugins:GCWebTheme
	""",

)
