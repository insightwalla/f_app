'''
To run the script:

streamlit run 🏠_Home.py
'''
import streamlit as st
from login_script import login
from templates.home_template import FeedBackHelper

import streamlit_antd_components as sac

# create menu


def create_sidebar_menu(self, with_db = True):
    with st.sidebar:
        menu = sac.menu([
            sac.MenuItem('Feedback', icon='database', children=[
                    sac.MenuItem('Edit', icon='brush'),
                    sac.MenuItem('Upload', icon='upload'),
                    sac.MenuItem('Download', icon='download'),
                    sac.MenuItem('Delete', icon='trash'),
                ]),

            sac.MenuItem('AI Assistant', icon='robot'),
            sac.MenuItem('Settings', icon='gear', children=[
                sac.MenuItem('AI', icon='robot'),
                sac.MenuItem('Vault', icon='lock'),
                sac.MenuItem('Theme', icon='brush'),
                sac.MenuItem('About', icon='info-circle'),
            ]),
                
        ], open_all=False)
        return menu

st.set_page_config(
   page_title='Feedback Reviewer',
   page_icon=':smile:',
   layout='wide',
   initial_sidebar_state='auto'
   )

def main_debug(name_db: str,section = '', name_user = ''):
    try:
        app = FeedBackHelper(name_db, name_user=name_user)
        app.run()
    except Exception as error:
        st.warning(error)
        raise error

def main_prod(name_db: str, section = '', name_user = ''):
    '''
    Main function to run the app
    This wont display the error message
    '''
    try:
        app = FeedBackHelper(name_db, name_user=name_user)
        app.run()
    except:
        st.info('Add some reviews by dragging and dropping the file')

# Main Loop
if __name__ == "__main__":
    DEBUG = True

    Menu = create_sidebar_menu(None)
    
    if Menu == 'Feedback':
        st.info('Feedback')


        CONFIG_FILE = "config.yaml"
        MAIN = main_debug if DEBUG else main_prod
        login(render_func=MAIN,
                config_file=CONFIG_FILE)