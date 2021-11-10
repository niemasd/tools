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

# prettify
alias pretty_json='python -m json.tool'
alias pretty_js='js-beautify'

# SSH aliases
alias ssh_key_create='ssh-keygen -t rsa -b 4096 -o -a 100'
alias cse='echo "Connecting to CSE (login.eng.ucsd.edu)..." ; ssh a1moshir@login.eng.ucsd.edu'
alias comet='echo "Connecting to Comet..." ; ssh -Y a1moshir@comet.sdsc.edu'
alias cometL1='echo "Connecting to Comet Login Node 1..." ; ssh -Y a1moshir@comet-ln1.sdsc.edu'
alias cometL2='echo "Connecting to Comet Login Node 2..." ; ssh -Y a1moshir@comet-ln2.sdsc.edu'
alias cometL3='echo "Connecting to Comet Login Node 3..." ; ssh -Y a1moshir@comet-ln3.sdsc.edu'
alias cometL4='echo "Connecting to Comet Login Node 4..." ; ssh -Y a1moshir@comet-ln4.sdsc.edu'
alias expanse='echo "Connecting to Expanse..." ; ssh -Y a1moshir@expanse.sdsc.xsede.org'
alias knuron='echo "Connecting to Knuron..." ; ssh -Y root@knuron.calit2.optiputer.net'
alias pi_tv_server='echo "Connecting to Raspberry Pi TV Server..." ; ssh -Y pi@192.168.1.15'
alias tscc='echo "Connecting to TSCC..." ; ssh -Y a1moshir@tscc.sdsc.edu'
alias tsccL1='echo "Connecting to TSCC Login Node 1..." ; ssh -Y a1moshir@tscc-login1.sdsc.edu'
alias tsccL2='echo "Connecting to TSCC Login Node 2..." ; ssh -Y a1moshir@tscc-login2.sdsc.edu'
alias xsede='echo "Connecting to XSEDE Login Hub..." ; ssh -Y niemasd@login.xsede.org'

# aliases for running servers
alias server_jupyter='jupyter notebook --ip 0.0.0.0 --port 1642'
