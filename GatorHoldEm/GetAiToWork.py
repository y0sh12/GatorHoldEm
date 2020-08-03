import os

if __name__ == '__main__':
    os.system('cmake ./; make')
    print('Entering res folder')
    os.chdir('res')
    os.system('pwd')
    print('Entered res folder')
    print('unpacking Handranks.dat')
    os.system('tar -xzvf handranks.tar.gz')
    print('unpacked Handranks.dat')
    print('going back ..')
    os.chdir('..')
    os.system('pwd')
    print('done!')