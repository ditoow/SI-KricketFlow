
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_users_file_path():
  
    ensure_dir(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database'))
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'users.json')

def load_users():
 
    users_file = get_users_file_path()
    if not os.path.exists(users_file):
        
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

    with open(get_users_file_path(), 'w') as f:
        json.dump(users, f, indent=4)

def check_credentials(username, password):

    users = load_users()
    if username in users and users[username]["password"] == password:
        return True, users[username]["name"]
    return False, None

def show_login():

    
    login_container = st.container()
    
    with login_container:
        st.title("🦗 KricketFlow")
        st.subheader("Login to continue")
        
        
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
                        
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
            
            

def is_logged_in():

    return 'logged_in' in st.session_state and st.session_state.logged_in

def logout():

    if 'logged_in' in st.session_state:
        del st.session_state.logged_in
    if 'username' in st.session_state:
        del st.session_state.username
    if 'user_name' in st.session_state:
        del st.session_state.user_name
