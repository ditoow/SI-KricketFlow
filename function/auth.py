
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_users_file_path():
    """Get the path to the users JSON file"""
    ensure_dir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database'))
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'users.json')

def load_users():
    """Load users from the JSON file"""
    users_file = get_users_file_path()
    if not os.path.exists(users_file):
        # Create default admin user if file doesn't exist
        default_users = {
            "admin": {
                "password": "admin123",
                "name": "Administrator",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        with open(users_file, 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users
    
    with open(users_file, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save users to the JSON file"""
    with open(get_users_file_path(), 'w') as f:
        json.dump(users, f, indent=4)

def check_credentials(username, password):
    """Check if the username and password are valid"""
    users = load_users()
    if username in users and users[username]["password"] == password:
        return True, users[username]["name"]
    return False, None

def show_login():
    """Display the login page"""
    # Use a container for the login form
    login_container = st.container()
    
    with login_container:
        st.title("🦗 KricketFlow")
        st.subheader("Login to continue")
        
        # Center the form elements
        col1, col2, col3 = st.columns([1.5, 2, 1.5])
        
        with col2:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_button = st.button("Login")
            
            if login_button:
                if not username or not password:
                    st.error("Please enter both username and password")
                else:
                    is_valid, user_name = check_credentials(username, password)
                    if is_valid:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_name = user_name
                        st.success(f"Login successful. Welcome, {user_name}!")
                        # Replace deprecated experimental_rerun with rerun
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            # Add some information about default credential

def is_logged_in():
    """Check if user is logged in"""
    return 'logged_in' in st.session_state and st.session_state.logged_in

def logout():
    """Log out the user"""
    if 'logged_in' in st.session_state:
        del st.session_state.logged_in
    if 'username' in st.session_state:
        del st.session_state.username
    if 'user_name' in st.session_state:
        del st.session_state.user_name
