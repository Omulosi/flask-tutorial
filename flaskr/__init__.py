import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
            )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure instance folder exists
    try:
        # raises error if directory already exists
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from .db import db
    db.init_app(app)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    app.add_url_rule('/', endpoint='index')

    return app
