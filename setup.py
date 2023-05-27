import setuptools

setuptools.setup(
    name='70mai-m300-toolbox',
    version='0.1',
    author='XuZhen86',
    url='https://github.com/XuZhen86/70MaiM300Toolbox',
    packages=setuptools.find_packages(),
    python_requires='==3.11.3',
    install_requires=[
        'absl-py==1.4.0',
        'requests==2.31.0',
    ],
    entry_points={
        'console_scripts': ['70mai-m300-toolbox = m300_toolbox.main:app_run_main',],
    },
)
