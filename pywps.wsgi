#!/usr/bin/env python
import sys
from pywps.app import Service

sys.path.append('/var/www/html/wps')

# Must first import the process, then add it to the application.
from wps_simplesttest import SimplestTest

from wps_testall import TestAll

application = Service(processes=[SimplestTest(), TestAll()])
