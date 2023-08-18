from flask import Flask, render_template
import secrets


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = secrets.token_hex()
    
    @app.route('/')
    def index():
        return render_template("index.html")
    
    from . import pokemon
    app.register_blueprint(pokemon.bp)

    from . import team
    app.register_blueprint(team.bp)
    
    return app

if __name__ == '__main__':
    create_app().run(debug=True)