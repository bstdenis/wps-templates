# wps-templates
OGC Web Processing Service templates

Installation:

Copy wpstemplates.sample.cfg as wpstemplates.cfg and edit as needed.

    docker build -t wpstemplates .

Or if in development, building images in docker_images prior:

    docker build --no-cache -t wpstemplates -f Df_dev1 .

Running the application:

    docker run --name wpstemplates1 -d -p 8009:80 wpstemplates

The available processes can be obtained at:

    http://localhost:8009/pywps?service=WPS&request=GetCapabilities&version=1.0.0

Note that to run the tests locally, the local ip address must be entered in
wpstemplates.cfg since localhost inside docker is not the same as localhost
on the machine running docker.

The pywps config file (pywps.cfg) is available. However, the outputurl
and outputpath values should not be modified as they are currently
hardcoded in other places.

Development:

1. Name all python files wps_*.py, these are the only files copied by the
   Dockerfile.
