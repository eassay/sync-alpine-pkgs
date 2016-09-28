set url="http://nl.alpinelinux.org/alpine/edge/main/x86_64/"
set threadnum=50
set timeout=120
set downloadroot=G:\work_chenping\alpine-pkgs\edge\main

python main.py --pkgurl %url% --threadnum %threadnum% --timeout %timeout% --downloadroot %downloadroot%