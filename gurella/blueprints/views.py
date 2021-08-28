from flask import Blueprint, render_template, session, url_for, g
from werkzeug.utils import redirect

from gurella.extensions import Transaction
from gurella.models import User

views_bp = Blueprint('views', __name__, url_prefix='/')

@views_bp.before_app_request
def load_session():
    user_id = session.get('user_id')

    if user_id is None:
        g.user_id = None
        redirect(url_for('auth.login'))
    else:
        g.user_id = user_id

@views_bp.route('/')
def landing_page():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('views.dashboard'))


@views_bp.route('/dashboard', methods=['GET'])
def dashboard():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))

    return render_template('views/dashboard.html', username='no obtained')


@views_bp.route('/campaigns', methods=['GET'])
def campaigns():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))

    tx = Transaction()
    with tx:
        user = tx.execute(lambda db_session: db_session.query(User).get(user_id))
        return render_template('views/campaigns.html', username=user.username)
