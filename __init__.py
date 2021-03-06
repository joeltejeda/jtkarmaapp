import os

from flask import Flask, render_template, request


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'jtkarma.co.uk.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'changed'
        print(app.config['DATABASE'] )
        return 'Hello, World the database is set to ' + app.config['DATABASE'] + 'END'

    @app.route("/contact")
    def contact():
        return "please contact us on email at hello@example.com"

    @app.route("/serverconfig")
    def serverconfig():
        return render_template ("forms/serverconfig.html")

    @app.route ("/serverconfig", methods=["POST"])
    def save_serverconfig():
        return render_template("thank-you.html", data=request.form)


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
