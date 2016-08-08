from setuptools import setup
from config import Config

setup (
		name=Config.progName,
		version=Config.progVersion,
		py_modules=['laser'],
		install_requires=[
			'Click',
			'PyMySQL',
			'python-nginx',
			'selenium',
		],
		entry_points='''
            [console_scripts]
            laser=laser:cli
        ''',
)
