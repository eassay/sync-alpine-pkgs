set url="http://nl.alpinelinux.org/alpine/v3.3/main/x86_64/"
set threadnum=80
set timeout=120
set downloadroot=G:\work_chenping\alpine-pkgs\3.3\main

python main.py --pkgurl %url% --threadnum %threadnum% --timeout %timeout% --downloadroot %downloadroot%