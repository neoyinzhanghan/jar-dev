import streamlit as st
from streamlit_extras.stoggle import stoggle
import time
import gspread
import datetime

#####################################
# FUNCTIONS
#####################################



#####################################
# MAIN
#####################################

if __name__ == "__main__":
    st.set_page_config(
        page_title="JAR",
        page_icon="logo.webp",
        layout="centered",
    )

    st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">', unsafe_allow_html=True)

