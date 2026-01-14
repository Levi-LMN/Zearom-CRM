# ============================================================================
# app/auth.py
# ============================================================================

from flask import Blueprint, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required
from authlib.integrations.flask_client import OAuth
from app import db
from app.models import User
from config import Config

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=Config.GOOGLE_CLIENT_ID,
        client_secret=Config.GOOGLE_CLIENT_SECRET,
        server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
        client_kwargs={'scope': 'openid email profile'}
    )

@auth_bp.route('/login')
def login():
    redirect_uri = url_for('auth.callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/callback')
def callback():
    token = oauth.google.authorize_access_token()
    user_info = token.get('userinfo')

    if user_info:
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            user = User(
                email=user_info['email'],
                name=user_info.get('name'),
                profile_picture=user_info.get('picture')
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)
        return redirect(url_for('main.dashboard'))

    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
