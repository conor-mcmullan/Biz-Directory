from setuptools import setup, find_packages

setup(
    name='biz_directory',
    version='0.0.1',
    author='Sean McMullan',
    author_email='seanpatrick246@icloud.com',
    description='Ulster University: Flask API with MongoDB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/conor-mcmullan/Biz-Directory',
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.3',
        'pymongo==4.10.1',
        'pydantic==2.9.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
