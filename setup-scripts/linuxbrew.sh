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
brew install zlib
brew install binutils --with-default-names
brew install glibc --with-current-kernel
# if glibc fails, comment out line 52 of ~/.linuxbrew/Library/Homebrew/os/linux/elf.rb (raise ErrorDuringExecution, command unless $?.success?)
# then also after everything's done do: cd ~/.linuxbrew && git reset --hard origin/master && cd
brew install curl # make sure this works so other stuff can download properly
brew install git
brew install gcc
brew install coreutils --with-default-names
brew install file-formula
brew tap linuxbrew/xorg
brew install xorg
brew install python3 # this needed xorg on debruijn