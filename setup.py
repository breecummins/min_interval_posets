from distutils.core import setup

setup(
    name='min_interval_posets',
    version='0.0.1',
    package_dir={'':'lib'},
    packages = ['min_interval_posets'],
    install_requires=["networkx","numpy"],
    author="Bree Cummins and Riley Nerem",
    url='https://github.com/breecummins/min_interval_posets'
    )