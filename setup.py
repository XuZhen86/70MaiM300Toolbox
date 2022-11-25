import setuptools

setuptools.setup(
    name='70mai-m300-toolbox',
    version='0.1',
    author='XuZhen86',
    url='https://github.com/XuZhen86/70MaiM300Toolbox',
    packages=setuptools.find_packages(),
    python_requires='>=3.11',
    install_requires=[
        'absl-py>=1.3.0',
        'requests>=2.28.1',
    ],
    entry_points={
        'console_scripts': ['70mai-m300-toolbox = m300_toolbox.main:app_run_main',],
    },
)
