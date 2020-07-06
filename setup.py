from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='GatorHoldEm',
    packages=find_packages(),
    version='1.0.2',
    license='MIT',
    description='Poker game made for CIS4390',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sean O'Reilly, Yaswanth Potluri, Adriel Mohammed, Bharat Samineni, Azharullah Baig",
    author_email='a.baig@ufl.edu',
    url='https://github.com/y0sh12/GatorHoldEm',
    download_url='https://github.com/y0sh12/GatorHoldEm/archive/v1.0.2.tar.gz',
    keywords=['poker', 'gatorholdem', 'texas'],
    install_requires=[
        'python-socketio[client]',
        'python-socketio',
        'eventlet',
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'gatorholdem=GatorHoldEm.SocketIOClient:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    package_data={'res':['*.png']},
)
