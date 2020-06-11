import setuptools
from os import path
# read the contents of your README file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(name='nano_prom_exporter',
                 version='0.1.5',
                 description='Export nano_node stats for prometheus',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 author='Russel Waters',
                 author_email='Russel@nano.org',
                 python_requires=">=3.7",
                 packages=setuptools.find_packages(),
                 url="https://github.com/nanocurrency/nano_prom_exporter",
                 install_requires=[
                     'requests',
                     'prometheus-client',
                     'psutil'
                 ],
                 entry_points={
                     'console_scripts': ['nano-prom=nano_prom_exporter.__main__:main']
                 })
