BaLaGan
=======

A simple web-based application for tracking who arrived to the kinder-garden each morning.

Configuration
=============
The server's configuration is defined, and can be edited through the *balagan_config.yaml* file (currently the servers domain and port)

Docker commands
===============
The app can be build into a docker image. A pre-build imaged can be found at: [https://hub.docker.com/r/omeryair/balagan/] 


To build the docker use:
``` bash
docker build -t balagan:latest .
```

To run the docker use:
``` bash
docker run --rm -p 80:80 balagan:latest
```

ToDo:
=====
- Store data in DB instead of memory
- Mailing system
- Management page
- Support for entering multiple e-mails
- Upload image
