FROM ubuntu:16.04

RUN apt-get -yqq update && \
    apt-get -yqq install python python-pip python-requests apache2 \
                         libapache2-mod-wsgi python-setuptools python-lxml \
                         git-core

RUN cd /root && \
    git clone https://github.com/geopython/pywps.git && \
    cd /root/PyWPS && \
    python setup.py install && \
    mkdir /var/www/html/wps && \
    mkdir /var/www/html/wps_results && \
    useradd apapywps && \
    mkdir /home/apapywps && \
    chown apapywps /home/apapywps && \
    chgrp apapywps /home/apapywps && \
    chown apapywps /var/www/html/wps_results && \
    chgrp apapywps /var/www/html/wps_results && \
    rm -rf /root/PyWPS

COPY pywps.wsgi /var/www/html/wps/
COPY wps_*.py /var/www/html/wps/
COPY apache2.conf /etc/apache2/
COPY pywps.cfg /etc/
COPY wpstemplates.cfg /home/

CMD export WPS_HOST=$(grep --only-matching --perl-regex "(?<=WPS_HOST\=).*" /home/wpstemplates.cfg) && \
    printf "\nexport WPS_HOST=$WPS_HOST\n" >> /etc/apache2/envvars && \
    sed -i '/outputurl=/c\outputurl=http://'"$WPS_HOST"'/wps_results/' /etc/pywps.cfg && \
    /etc/init.d/apache2 start && tail -f /dev/null

EXPOSE 80
