import pkg_resources
from flask import g

from akk import app

app.config.update(dict(
    DATABASE=pkg_resources.resource_filename("akk", "db_data/database.db")
))
app.config.from_envvar('AKK_SETTINGS', silent=True)

@app.cli.command("initdb")
def initdb_command():
    from akk.db.engine import init_db
    init_db()