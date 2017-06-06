FROM u16

RUN cd /root && \
    git clone https://github.com/geopython/pywps.git && \
    cd /root/pywps && \
    python setup.py install && \
    mkdir /var/www/html/wps && \
    mkdir /var/www/html/wps_results && \
    useradd apapywps && \
    mkdir /home/apapywps && \
    chown apapywps /home/apapywps && \
    chgrp apapywps /home/apapywps && \
    chown apapywps /var/www/html/wps_results && \
    chgrp apapywps /var/www/html/wps_results && \
    rm -rf /root/pywps
