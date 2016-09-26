from flask import Blueprint

app = Blueprint('auth', __name__)


@app.route('/here')
def new_route():
    return "HERE!"
