# ls aliases
alias l='ls'
alias ll='ls -l'
alias lla='ll -a'
alias llh='ll -h'
alias llt='ll -t'

# update
alias update='sudo apt-get -y update ; sudo apt-get -y upgrade ; sudo apt-get -y autoremove; sudo apt-get autoclean ; sudo apt-get clean'

# android box keyboard alias
alias keyboard='telnet 192.168.1.4 2323'

# SSH aliases
alias cse='echo "Connecting to CSE (login.eng.ucsd.edu)..." ; ssh a1moshir@login.eng.ucsd.edu'
alias comet='echo "Connecting to Comet..." ; ssh -Y a1moshir@comet.sdsc.edu'
alias cometL1='echo "Connecting to Comet Login Node 1..." ; ssh -Y a1moshir@comet-ln1.sdsc.edu'
alias cometL2='echo "Connecting to Comet Login Node 2..." ; ssh -Y a1moshir@comet-ln2.sdsc.edu'
alias cometL3='echo "Connecting to Comet Login Node 3..." ; ssh -Y a1moshir@comet-ln3.sdsc.edu'
alias cometL4='echo "Connecting to Comet Login Node 4..." ; ssh -Y a1moshir@comet-ln4.sdsc.edu'
alias tscc='echo "Connecting to TSCC..." ; ssh -Y a1moshir@tscc.sdsc.edu'
alias tsccL1='echo "Connecting to TSCC Login Node 1..." ; ssh -Y a1moshir@tscc-login1.sdsc.edu'
alias tsccL2='echo "Connecting to TSCC Login Node 2..." ; ssh -Y a1moshir@tscc-login2.sdsc.edu'
