# dependance install
echo "install requirment"
pip install -r dependance
echo "finish install dependance"
echo "start up ..."


# start up image
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
    \- ▌                                     ▀ ▀
     - ▌                                         ▀
    /- ▌            Go Go Go !               ▀ ▀
    /  ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ ▀
                  ██
      "

# start command

gunicorn -b 0.0.0.0:8888 -w 4 -k gevent --timeout=30 --access-logfile=- --access-logformat='"%(h)s" "%(t)s" "%(r)s" %(s)s %(b)s" "%(L)s"' devops:app
