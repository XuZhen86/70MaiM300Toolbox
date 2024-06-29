import setuptools

setuptools.setup(
    name='70mai-m300-toolbox',
    version='0.1',
    author='XuZhen86',
    url='https://github.com/XuZhen86/70MaiM300Toolbox',
    packages=setuptools.find_packages(),
    python_requires='>=3.12',
    install_requires=[
        'absl-py==2.0.0',
        'requests==2.31.0',
        'jsonschema==4.19.1',
    ],
    entry_points={
        'console_scripts': ['70mai-m300-toolbox = m300_toolbox.main:app_run_main',],
    },
)
