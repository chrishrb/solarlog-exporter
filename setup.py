import setuptools

with open('README.md') as f:
    readme = f.read()

setuptools.setup(name='solarlog_exporter',  # Change to your package name
                 description="Solarlog exporter to influxdb",
                 version='1.0.0',
                 long_description=readme,
                 author='Christoph Herb',
                 url='https://github.com/chrishrb/solarlog-exporter',
                 packages=setuptools.find_packages(exclude=('tests', 'docs')))
