#!/usr/bin/env bash
# set all languages to English (optional, needed when glibc postinstall complains about language, add to .bash_profile or whatever too)
export LANG=en_US.UTF-8
export LC_CTYPE="en_US.UTF-8"
export LC_NUMERIC="en_US.UTF-8"
export LC_TIME="en_US.UTF-8"
export LC_COLLATE="en_US.UTF-8"
export LC_MONETARY="en_US.UTF-8"
export LC_MESSAGES="en_US.UTF-8"
export LC_PAPER="en_US.UTF-8"
export LC_NAME="en_US.UTF-8"
export LC_ADDRESS="en_US.UTF-8"
export LC_TELEPHONE="en_US.UTF-8"
export LC_MEASUREMENT="en_US.UTF-8"
export LC_IDENTIFICATION="en_US.UTF-8"

# install linuxbrew
git clone https://github.com/Linuxbrew/brew.git ~/.linuxbrew

# set up PATH (don't forget to add these to .bash_profile or whatever)
export PATH="$HOME/.linuxbrew/bin:$HOME/.linuxbrew/sbin:$PATH"
export MANPATH="$HOME/.linuxbrew/share/man:$MANPATH"
export INFOPATH="$HOME/.linuxbrew/share/info:$INFOPATH"

# symlink the system compilers
for f in /usr/bin/gcc*; do ln -s `which $f` $HOME/.linuxbrew/bin/gcc-`$f -dumpversion |cut -d. -f1,2`; done
for f in /usr/bin/g++*; do ln -s `which $f` $HOME/.linuxbrew/bin/g++-`$f -dumpversion |cut -d. -f1,2`; done
for f in /usr/bin/gfortran*; do ln -s `which $f` $HOME/.linuxbrew/bin/gfortran-`$f -dumpversion | grep "GNU Fortran (GCC)" | cut -f4 -d' '`; done
rm $HOME/.linuxbrew/bin/*-

# install important packages
brew install gcc
brew list | grep -v gcc | grep -v glibc | xargs brew reinstall
cd ~/.cache/Homebrew && wget http://niema.net/files/curl-7.54.0.tar.bz2 && cd # only needed if system's certificate is too old. curl source on my server might be out-of-date
brew install curl
brew install perl
brew reinstall openssl
brew reinstall curl
brew install gnu-tar --with-default-names
brew install file-formula bsdmainutils binutils coreutils findutils gawk gnu-sed gnu-which grep libpng libxml2 libxslt make ncurses readline
brew install cmake
brew install ruby
brew install git wget htop gzip unzip
brew install less
brew install python
brew install vim --with-override-system-vi
brew tap linuxbrew/homebrew-science
brew install openblas openmpi

# compile python3 from source
mkdir ~/.python3
wget https://www.python.org/ftp/python/3.2.6/Python-3.2.6.tgz
tar -zxvf Python-3.2.6.tgz && rm Python-3.2.6.tgz
cd Python-3.2.6 && ./configure
make altinstall prefix=$HOME/.python3 exec-prefix=$HOME/.python3
cd .. && rm -rf Python-3.2.6
ln -s ~/.python3/bin/python3.2 ~/bin/python3 # assumes ~/bin is in PATH
curl https://bootstrap.pypa.io/3.2/get-pip.py | ~/bin/python3
ln -s ~/.python3/bin/pip3 ~/bin/pip3
wget https://bitbucket.org/pypa/setuptools/raw/0.7.4/ez_setup.py -O - | python3
pip3 install numpy==1.10.4
wget https://pypi.python.org/packages/4a/da/4bf81ee31f187553fd12381635dc47d14747817c9196e388cf56209f275e/biopython-1.61.tar.gz
tar -zxvf biopython-1.61.tar.gz && rm biopython-1.61.tar.gz
cd biopython-1.61 && python3 setup.py install
cd .. && rm -rf biopython-1.61




#brew install R

# compile python3 from source
#wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
#tar -zxvf Python-3.6.1.tgz
#rm Python-3.6.1.tgz
#cd Python-3.6.1
#./configure
#mkdir -p ~/.python3
#make altinstall prefix=$HOME/.python3 exec-prefix=$HOME/.python3
#ln -s ~/.python3/bin/python3.3 ~/bin/python3


# trying to install python3
#brew install libtool --with-default-names
#brew install bash
#ln -s ~/.linuxbrew/bin/bash ~/bin/sh # assuming ~/bin is in PATH
#brew tap linuxbrew/homebrew-xorg
#brew install xorg
#brew install python3