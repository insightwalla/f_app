'''
To run the script:

streamlit run 🏠_Home.py
'''
import streamlit as st
from login_script import login
from templates.home_template import FeedBackHelper
from templates.section_final_counter_ import final_page
from templates.section_ai_report import final_page_ai
from templates.settings_template import settings_template_doc

from utils import *

import streamlit_antd_components as sac

def create_sidebar_menu(self, with_db = True):
    with st.sidebar:
        menu = sac.menu([
            sac.MenuItem('Feedback', icon='database', children=[
                    sac.MenuItem('Score', icon='brush'),
                    sac.MenuItem('Upload', icon='upload'),
                    sac.MenuItem('Download', icon='download'),
                ]),
            sac.MenuItem('Reporting', icon='link'),
            sac.MenuItem('AI Assistant', icon='robot'),
            sac.MenuItem('Settings', icon='gear')
                
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
    DEBUG = False
    CONFIG_FILE = "config.yaml"

    Menu = create_sidebar_menu(None)
    
    if Menu == 'Score':
        MAIN = main_debug if DEBUG else main_prod
        login(render_func=MAIN,
                config_file=CONFIG_FILE)

    elif Menu == 'Reporting':
        login(render_func=final_page, 
            config_file=CONFIG_FILE, 
            section='')
        

    elif Menu == 'AI Assistant':
        login(render_func=final_page_ai,
                config_file=CONFIG_FILE,
                section='AI Assistant')
        
    elif Menu == 'Settings':
        login(render_func=settings_template_doc,
                config_file=CONFIG_FILE,
                section='Settings')
    
    elif Menu == 'Upload':
        def OnUploaded(name_db: str, section = '', name_user = ''):
            try:
                app = FeedBackHelper(name_db, name_user=name_user).UploadNewDataMenu()
                app.run()
            except:
                st.info('Add some reviews by dragging and dropping the file')
        
        login(render_func=OnUploaded,
                config_file=CONFIG_FILE,
                section='Upload')