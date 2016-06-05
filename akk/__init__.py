import pkg_resources
import flask

__version__ = pkg_resources.get_distribution(__name__).version

# Create the flask application only once
app = flask.Flask(__name__)
app.config.from_object(__name__)

# Import all settings
import akk.flask.config

# Import all the routing
import akk.flask.views
