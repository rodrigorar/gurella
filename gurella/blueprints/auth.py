from flask import Blueprint, render_template, request, session, g, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from gurella.extensions import Transaction, hashing
from gurella.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.before_app_request
def load_session():
    user_id = session.get('user_id')

    if user_id is None:
        g.user_id = None
        redirect(url_for('auth.login'))
    else:
        g.user_id = user_id


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashedPassword = hashing.hash_value(password)

        tx = Transaction()
        with tx:
            user = tx.execute(function=lambda db_session: db_session.query(User).filter_by(username=username).first())
            if user is not None and user.password == hashedPassword:
                session['user_id'] = user.id
                return redirect(url_for('views.dashboard'))
            else:
                abort(403)
        tx = Transaction()
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        hashedPassword = hashing.hash_value(password)

        tx = Transaction()
        with tx:
            user = tx.execute(lambda db_session: db_session.add(User(username=username, email=email, password=hashedPassword)))

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
