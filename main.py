from website import create_app
import mariadb
import os.path
from flask import render_template, Blueprint, g
# from website.views import main_views

# main = Blueprint('main', __name__)

app = create_app()

# Register the 'views' blueprint
# app.register_blueprint(main_views)


# @app.teardown_appcontext
# def teardown_db(exception=None):
#     db_connector.close()


if __name__ == '__main__':
    app.run(debug=True)

