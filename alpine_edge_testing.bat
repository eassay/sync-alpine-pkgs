set url="http://nl.alpinelinux.org/alpine/edge/testing/x86_64/"
set threadnum=80
set timeout=120
set downloadroot=G:\work_chenping\alpine-pkgs\edge\testing

python main.py --pkgurl %url% --threadnum %threadnum% --timeout %timeout% --downloadroot %downloadroot%