from setuptools import setup, find_packages

setup(
    name='usd_to_rub',
    version='1.0',
    author='Afanasev Nikolay',
    author_email='mcridednb@gmail.com',
    packages=find_packages(),
    entry_points={'console_scripts': ['usd-to-rub = src.converter:start']}
)