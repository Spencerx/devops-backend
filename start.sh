# dependance install
echo "install requirment"
pip install -r dependance
echo "finish install dependance"
echo "start up ..."

source /etc/profile

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
gunicorn -b 0.0.0.0:18888 -w 12 -k gevent --env ads_env=prod --access-logfile logs/access.log --error-logfile logs/error.log --access-logformat='%(h)s %(t)s %(r)s %(s)s %(b)s %(L)s' devops:app --preload
