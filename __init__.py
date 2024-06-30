from flask import Flask
from datetime import datetime





def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "SECRET!"


    @app.context_processor
    def inject_today_date():
        return {'today_date': datetime.now()}


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)



    return app
