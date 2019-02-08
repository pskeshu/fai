from setuptools import setup

setup(name='fai',
      version='0.2',
      description='Analysis for Fluorescence Anisotropy Imaging',
      url='https://github.com/pskeshu/fai',
      author='Kesavan Subburam',
      author_email='pskesavan@tifrh.res.in',
      packages=['fai'],
      install_requires=['numpy>=1.16.1',
                        'scikit-image>=0.14.2',
                        'matplotlib>=3.0.2',
                        'tqdm>=4.30.0',
                        'scipy>=1.2.0',
                        'matplotlib-scalebar>=0.5.1',
                        'matplotlib-colorbar>=0.3.7'],
      zip_safe=False)
