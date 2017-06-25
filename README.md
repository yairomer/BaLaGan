BaLaGan
=======

A simple web-based application for tracking who arrived to the kinder-garden each morning.

Configuration
=============
The server's configuration is defined, and can be edited through the *balagan_config.yaml* file (currently it's only the port)

Docker commands
===============
The app can be build into a docker image. A pre-build imaged can be found at: [https://hub.docker.com/r/omeryair/balagan/] 


To build the docker use:
``` bash
docker build -t balagan:latest .
```

To run the docker use:
``` bash
docker run --rm -p 80:80 -v {{ path_to_config_file }}:/app/balagn_congi.yaml balagan:latest
```

ToDo:
=====
- Store data in DB instead of memory
- Mailing system
- Support for entering multiple e-mails
- Upload image
- Refresh interval
- Authentication
