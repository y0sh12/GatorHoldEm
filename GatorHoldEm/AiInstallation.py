import os

if __name__ == '__main__':
    print("Setting up dependencies")
    print("Compiling ai.cpp")
    os.system('cmake ./; make')
    os.chdir('res')
    os.system('pwd')
    print('Unpacking Handranks.dat')
    os.system('tar -xzvf handranks.tar.gz')
    os.system('rm ._HandRanks.dat')
    os.chdir('..')
    os.system('pwd')