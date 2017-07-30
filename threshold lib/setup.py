from distutils.core import setup, Extension

setup(
	name='th',
	version='1.0',
	ext_modules = [
		Extension('th', ['libreria.cpp'])
	]
)