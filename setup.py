from distutils.core import setup

setup(
    name='GatorHoldEm',
    packages=['GatorHoldEm'],
    version='0.2',
    license='MIT',
    description='Poker game made for CIS4390',
    author="Sean O'Reilly, Yaswanth Potluri, Adriel Mohammed, Bharat Samineni, Azharullah Baig",
    author_email='a.baig@ufl.edu',
    url='https://github.com/y0sh12/GatorHoldEm',
    download_url='https://github.com/y0sh12/GatorHoldEm/archive/v0.2.tar.gz',
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
    package_data={'':['res/*.png']},
)
