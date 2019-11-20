from flask import Flask
from dice.classes.database import Database
from dice.views import blueprints


def create_app(debug=False):
    app = Flask(__name__)
    app.config['TESTING'] = debug
    """ app.config['LOGIN_DISABLED'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE' """

    db = Database()
    db.initDiceSets("dice/resources")
    db.remove_all_dice_in_set("basic")
    db.remove_all_dice_in_set("halloween")
    db.initDiceCollection("basic")
    db.initDiceCollection("halloween")

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app


if __name__ == '__main__':

    app = create_app()
    app.run(debug=True)
