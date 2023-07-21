import setuptools

setuptools.setup(name='solarlog_exporter',  # Change to your package name
                 description="Solarlog exporter to influxdb",
                 version='2.0.0',
                 author='Christoph Herb',
                 url='https://github.com/chrishrb/solarlog-exporter',
                 packages=setuptools.find_packages(exclude=('tests', 'docs')))
