from setuptools import setup, Extension

with open('README.md') as f:
    long_description = f.read()

setup(
    name='get_project_root',  # How you named your package folder (MyLib)
    packages=['get_project_root'],  # Chose the same as "name"
    version='0.2',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='a simple package for resolving project root in most situations',  # Give a short description about your library
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Charles Anderson',  # Type in your name
    author_email='hpcngmoh@gmail.com',  # Type in your E-Mail
    url='https://github.com/bigbizze/py_get_project_root',  # Provide either the link to your github or to your website
    download_url='https://github.com/bigbizze/py_get_project_root/archive/refs/tags/init4.tar.gz',  # I explain this later on
    keywords=['UTILS', 'PROJEC ROOT', 'DIRECTORY'],  # Keywords that define your package best
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
