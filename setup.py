
from distutils.core import setup

setup(name='minivan',
      packages = ['minivan'],
      version='2.0',
      description='Minifier for vanilla JS and CSS file',
      url='https://github.com/mitesh-raval/Minivan',
      download_url = 'https://github.com/mitesh-raval/Minivan/archive/refs/tags/2.0.tar.gz',
      author='Mitesh Raval',
      author_email='mitesh@nasagram.com',
      keywords = ['minifier', 'minivan', 'minifier js', 'minifier css'],
      license='MIT', #YOUR LICENSE HERE!

      install_requires=[],  #YOUR DEPENDENCIES HERE
  
      classifiers=[
        'Development Status :: 5 - Production/Stable',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License', # Your License Here  
        'Programming Language :: Python :: 3.9',
        ],
)