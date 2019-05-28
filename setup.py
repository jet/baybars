from setuptools import setup, find_packages

packages = find_packages()

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(name='baybars',
      version='0.0.25',
      setup_requires=['pbr==5.1.1'],
      copyright='Copyright 2019 Jet.com',
      url='http://pypi.org/project/baybars/',
      packages=packages,
      install_requires=[
        'python-consul==1.1.0',
        'azure-storage-blob==1.4.0',
        'azure-storage-queue==1.4.0',
        'confluent-kafka==0.11.6',
        'azure-cosmos==3.0.2',
        'pysftp==0.2.9',
        'requests==2.20.1',
        'numpy==1.15.4',
        'pandas==0.23.4',
        'python-consul==1.1.0',
        'PyHive==0.6.1',
        'elasticsearch==6.3.1',
        'azure-cosmosdb-table==1.0.5'
      ],
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='azure kafka blob documentdb cosmosdb queue tar',
      python_requires='>=3.5',
      zip_safe=False,
      pbr=True)
