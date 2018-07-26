from distutils.core import setup

setup(
    name='pyiface',
    version='0.0.9',
    author='Sergey Kostov',
    author_email='bat.serjo@gmail.com',
    packages=['pyiface'],
    scripts=[],
    url='http://pypi.python.org/pypi/pyiface/',
    python_requires='>=2',
    license='LICENSE.txt',
    description='View and control network interfaces. Linux only currently! Join us lets make it available for other OSes',
    long_description=open('README.rst').read(),
    install_requires=[],
)
