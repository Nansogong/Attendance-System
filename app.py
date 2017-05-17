from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
import os
import config

deploy = os.getenv('DEPLOY', 'local').title()
app = Flask(__name__)
app.config.from_object('config.{}Config'.format(deploy))
app.app_context().push()

from views import website

app.register_blueprint(website.mod)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# Default port:
if __name__ == '__main__':
    app.run()
