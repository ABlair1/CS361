from flask import Flask

def create_app():
    app = Flask(__name__)

    # Import and register views with application
    from .views import views
    app.register_blueprint(views)

    return app