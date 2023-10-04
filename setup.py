from setuptools import setup, find_packages
setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    scripts      = ['main.py'],
    entry_points = {'scrapy': ['settings = crawler.settings']},
)