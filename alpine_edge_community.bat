set url="http://nl.alpinelinux.org/alpine/edge/community/x86_64/"
set threadnum=80
set timeout=120
set downloadroot=G:\work_chenping\alpine-pkgs\edge\community

python main.py --pkgurl %url% --threadnum %threadnum% --timeout %timeout% --downloadroot %downloadroot%