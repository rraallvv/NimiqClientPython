from setuptools import setup

setup(
    name='nimiqclient',
    version='0.0.1',
    description='A python client for the Nimiq JSON-RPC API',
    url='http://github.com/rraallvv/NimiqClientPython',
    author='Nimiq Community',
    author_email='info@nimiq.com',
    license='MIT',
    packages=['nimiqclient'],
    zip_safe=True,
    install_requires=[
        'requests'
    ],
)
