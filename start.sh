echo "install requirment"
pip install -r dependance
echo "finish install dependance"
echo "start up ..."
echo  "
             ▄▄▄▄▄
               ▀▀▀██████▄▄▄       _______________
             ▄▄▄▄▄  █████████▄  /                 \
            ▀▀▀▀█████▌ ▀▐▄ ▀▐█ |      devops!      |
          ▀▀█████▄▄ ▀██████▄██ | _________________/
          ▀▄▄▄▄▄  ▀▀█▄▀█════█▀ |/
               ▀▀▀▄  ▀▀███ ▀       ▄▄
            ▄███▀▀██▄████████▄ ▄▀▀▀▀▀▀█▌   ______________________________
          ██▀▄▄▄██▀▄███▀ ▀▀████      ▄██  █                              \\
       ▄▀▀▀▄██▄▀▀▌████▒▒▒▒▒▒███     ▌▄▄▀▀▀▀█_____________________________ //
       ▌    ▐▀████▐███▒▒▒▒▒▐██▌
       ▀▄▄▄▄▀   ▀▀████▒▒▒▒▄██▀
                 ▀▀█████████▀
               ▄▄██▀██████▀█
             ▄██▀     ▀▀▀  █
            ▄█             ▐▌
        ▄▄▄▄█▌              ▀█▄▄▄▄▀▀▄
       ▌     ▐                ▀▀▄▄▄▀
        ▀▀▄▄▀     ██
    \  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀
    \- ▌   Vue2 axios elment-ui flask        ▀ ▀
     - ▌                                         ▀
    /- ▌            Go Go Go !               ▀ ▀
    /  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀
                  ██
      "

gunicorn -b 0.0.0.0:8888 -w 12 -k gevent --access-logfile=- --access-logformat=%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" devops:app
