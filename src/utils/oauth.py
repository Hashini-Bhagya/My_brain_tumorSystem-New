import requests
from flask import redirect, request, url_for, current_app, flash
from flask_login import login_user
from urllib.parse import urlencode
from src.controllers.user_controller import UserController
import json
from config import Config

GOOGLE_CLIENT_ID = Config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = Config.GOOGLE_CLIENT_SECRET

# HARDCODED VALUES - REPLACE WITH YOUR ACTUAL VALUES
GOOGLE_CLIENT_ID = "441128910074-fpqe3k8eo6i8g54rcfp2c12eisrq6ssc.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"  # ← REPLACE THIS

class GoogleOAuth:
    @staticmethod
    def get_google_provider_cfg():
        try:
            response = requests.get(
                "https://accounts.google.com/.well-known/openid-configuration",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"ERROR: Failed to get Google provider config: {e}")
            return None

    @staticmethod
    def login():
        try:
            # Use hardcoded values instead of config
            client_id = GOOGLE_CLIENT_ID
            print(f"DEBUG: Using Client ID: {client_id}")
            
            if not client_id:
             flash("Google authentication is not configured", "error")
             return redirect(url_for("api.login"))

            
            google_provider_cfg = GoogleOAuth.get_google_provider_cfg()
            if not google_provider_cfg:
                flash("Unable to connect to Google authentication service", "error")
                return redirect(url_for("api.login"))
            
            authorization_endpoint = google_provider_cfg["authorization_endpoint"]
            
            # Use _external=True to get full URL
            redirect_uri = url_for("api.google_callback", _external=True)
            print(f"DEBUG: Redirect URI: {redirect_uri}")
            
            params = {
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "response_type": "code",
                "scope": "openid email profile",
                "access_type": "offline",
                "prompt": "consent"
            }
            
            request_uri = f"{authorization_endpoint}?{urlencode(params)}"
            print(f"DEBUG: Google Auth URL: {request_uri}")
            
            return redirect(request_uri)
            
        except Exception as e:
            print(f"ERROR in Google login: {e}")
            flash("Google authentication failed to start", "error")
            return redirect(url_for("api.login"))

    @staticmethod
    def callback():
        try:
            code = request.args.get("code")
            error = request.args.get("error")
            
            print(f"DEBUG: Callback received - code: {code}, error: {error}")
            
            if error:
                flash(f"Google authentication error: {error}", "error")
                return redirect(url_for("api.login"))
            
            if not code:
                flash("Authorization code not received from Google", "error")
                return redirect(url_for("api.login"))
            
            # Get Google provider configuration
            google_provider_cfg = GoogleOAuth.get_google_provider_cfg()
            if not google_provider_cfg:
                flash("Unable to connect to Google authentication service", "error")
                return redirect(url_for("api.login"))
            
            token_endpoint = google_provider_cfg["token_endpoint"]
            
            # Use hardcoded values
            client_secret = GOOGLE_CLIENT_SECRET
            print(f"DEBUG: Client secret exists: {bool(client_secret and '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' not in client_secret)}")
            
            # Prepare token exchange request
            redirect_uri = url_for("api.google_callback", _external=True)
            token_data = {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri,
            }
            
            print(f"DEBUG: Token exchange data: { {k: v for k, v in token_data.items() if k != 'client_secret'} }")
            
            token_headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            # Exchange code for tokens
            token_response = requests.post(
                token_endpoint,
                data=token_data,
                headers=token_headers,
                timeout=10
            )
            
            print(f"DEBUG: Token response status: {token_response.status_code}")
            print(f"DEBUG: Token response text: {token_response.text}")
            
            if token_response.status_code != 200:
                flash("Google authentication failed during token exchange", "error")
                return redirect(url_for("api.login"))
            
            tokens = token_response.json()
            access_token = tokens.get("access_token")
            
            if not access_token:
                flash("No access token received from Google", "error")
                return redirect(url_for("api.login"))
            
            # Get user info
            userinfo_response = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            
            if userinfo_response.status_code != 200:
                flash("Failed to get user information from Google", "error")
                return redirect(url_for("api.login"))
            
            user_info = userinfo_response.json()
            print(f"DEBUG: User info: {user_info}")
            
            # Verify email and get user data
            if user_info.get("email_verified"):
                users_email = user_info["email"]
                users_name = user_info.get("given_name", user_info.get("name", "Google User"))
            else:
                flash("Google email not verified", "error")
                return redirect(url_for("api.login"))

            # Find or create user
            user = UserController.get_user_by_email(users_email)
            
            if not user:
                user_data = {
                    'name': users_name,
                    'email': users_email,
                    'password': None
                }
                user, message = UserController.create_user(user_data)
                
                if not user:
                    flash(f"Error creating user: {message}", "error")
                    return redirect(url_for("api.login"))
            
            # Log the user in
            login_user(user)
            flash("Login successful with Google!", "success")
            return redirect(url_for("api.dashboard"))
            
        except Exception as e:
            print(f"ERROR in Google callback: {e}")
            flash("Google authentication failed unexpectedly", "error")
            return redirect(url_for("api.login"))