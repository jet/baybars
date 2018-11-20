from setuptools import setup, find_packages

packages = find_packages()

setup(name='baybars',
      version='0.0.10',
      description='Python Common Packages',
      copyright='Copyright 2018 Jet.com',
      url='http://pypi.org/project/baybars/',
      author='Bugra Akyildiz',
      author_email='bugra.akyildiz@jet.com',
      license='Apache 2.0',
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
        'elasticsearch==6.3.1'
      ],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
      ],
      keywords='azure kafka blob documentdb cosmosdb queue tar',
      python_requires='>=3.5',
      zip_safe=False)
