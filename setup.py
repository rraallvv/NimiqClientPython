from setuptools import setup

setup(
    name='nimiq-client-python',
    version='0.0.1',
    description='A python client for the Nimiq JSON-RPC API',
    url='http://github.com/jgraef/nimiq-client-python',
    author='Janosch Gräf',
    author_email='janosch.graef@cispa.saarland',
    license='MIT',
    packages=['nimiqclient'],
    zip_safe=True,
    install_requires=[
        'requests'
    ],
)
