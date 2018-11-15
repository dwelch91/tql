from setuptools import setup


with open('README.md') as f:
    long_desc = f.read()

setup(name='qq',
      version='0.1.0',
      description='Run SQL against CSV or TSV file(s).',
      long_description=long_desc,
      long_description_content_type='text/markdown',
      author='Don Welch',
      author_email='dwelch91 [at] gmail.com',
      url='https://github.com/dwelch91/qq',
      license='MIT license',
      platforms=['unix', 'linux', 'macosx'],
      packages=['qq'],
      entry_points={
          'console_scripts': ['qq=qq.__main__:main']
      },
      install_requires=['prettytable',
                        'pendulum'],
      python_requires='~=3.5',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Operating System :: POSIX',
          'Environment :: MacOS X',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3 :: Only',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
      ]
)
