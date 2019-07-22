# this file is only used for the deployed website
activate_this = 'PATH'
with open(activate_this) as f:
	exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/flaskproject/")

from app import app as application
