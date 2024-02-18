import streamlit as st
from streamlit_extras.stoggle import stoggle
from jar import get_jars_dct_title_key, get_jar_ledger_as_pd, get_jar_ledger_as_pd
from jar import jar_commit, delete_clip_using_page_id, edit_clip_content, edit_clip_title, edit_jar_title
from sync import sync
from analytics import process_df, get_num_entries
import streamlit.components.v1 as components
import time
import gspread
import datetime

#####################################
# FUNCTIONS
#####################################

# Function to generate HTML for a single card with a title and a static statistic number
def generate_card_html(title, statistic, card_id):
    card_html = f"""
    <div style="border: 2px solid #ccc; margin-bottom: 32px; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <h2 style="margin: 0; padding: 0; color: rgba(239, 245, 255, 0.69); font-family: 'Inter', sans-serif;">{title}</h2>
        <p style="margin: 10px 0 0 0; font-size: 36px; font-weight: bold; color: rgba(252, 253, 255, 0.94); font-family: 'Inter', sans-serif;">{statistic}</p>
    </div>
    """
    return card_html

#####################################
# MAIN
#####################################

if __name__ == "__main__":
    st.set_page_config(
        page_title="JAR",
        page_icon="logo.webp",
        layout="centered",
    )

    with st.sidebar:
        left_co, cent_co, last_co = st.columns(3)
        with cent_co:
            st.markdown(
                """
                <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                    <img src="https://i.imgur.com/EKx9qSk.png" style="max-width: 100%; border-radius: 50%;">
                </a>
                """,
                unsafe_allow_html=True,
            )

        st.divider()

        st.button("Neo's JAR", use_container_width=True, type="primary")

        st.button("Ryusei's JAR", use_container_width=True)

        stoggle("About us", f"✨ We are a team of UC Berkeley students who are passionate about AI education: Neo (PhD in Statistics) and Ryusei (Political Science at Berkeley). We built Just Attempt Record (JAR) on February 16, 2024, to help PhD researchers and professors produce knowledge faster by accelerating the inquiry and experimentation cycles!")

    st.write(
        """
        <style>
        h1 {
            text-align: center;
            color: #1B7FB9;
            margin-top: -50px;
            margin-bottom: -15px; 
            font-size: 64px; 
            font-family: 'Inter', sans-serif;
        }
        h2 {
            text-align: center;
            margin-top: -24px; 
            font-size: 16px; 
            margin-bottom: -50px;
            font-family: 'Inter', sans-serif;
        }
        h3 {
            text-align: center;
            color: #4AF8CD;
            margin-top: -20px; 
            font-size: 24px; 
            margin-bottom: -50px;
            font-family: 'Inter', sans-serif;
        }
        h4 {
            text-align: center;
            margin-top: -20px; 
            font-size: 16px; 
            font-family: 'Inter', sans-serif;
        }
        h5 {
            font-size: 24px;
            margin-bottom: -20px;
            font-family: 'Inter', sans-serif;
        }

        h6{
            text-align:left;
            font-size: 24px;
            margin-top:-20px;
            font-family: 'Inter', sans-serif;
        }
        @media only screen and (max-width: 600px) {
            h1 {
                font-size: 32px;
            }
            h5 {
                font-size: 20px;
            }
        }  
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("""
        <style>
        .hover_text:hover .default_text {
            display: none;
        }
        
        .hover_text:hover .hover_text_content {
            display: block;
        }
        
        .hover_text_content {
            display: none;
        }
        </style>
        
        <div class="hover_text">
            <h1 class="default_text">JAR</h1>
            <h1 class="hover_text_content">Just Attempt Record</h1>
        </div>
        """, unsafe_allow_html=True)
    
    add = "Add new entry"
    edit = "Edit entry"
    delete = "Delete entry"

    st.write("<h5>Select JAR</h5>", unsafe_allow_html=True)

    jar_dct = get_jars_dct_title_key()
    # get a tuple of all the keys
    jar_titles = tuple(jar_dct.keys())
    
    option = st.selectbox(
            "",
            jar_titles,
            label_visibility="collapsed",
        )

    st.write("")
    st.write("")

    selected_database_id = jar_dct[option]["database_id"]
    df = get_jar_ledger_as_pd(selected_database_id)
    # df = process_df(get_jar_ledger_as_pd(selected_database_id))
    total_entries = get_num_entries(df)
    average_entries_per_week = "20" # TODO and make sure to fix the process_df function

    first_co, second_co = st.columns(2)
    with first_co:
        def generate_full_html():
            card_1_html = generate_card_html("Total Entries", total_entries, "1")
            card_2_html = generate_card_html("Avg. Entries Per Week", average_entries_per_week, "2")
            
            full_html = f"""
            <html>
            <body>
                {card_1_html}
                {card_2_html}
            </body>
            </html>
            """
            return full_html
        
        components.html(generate_full_html(), height=350)

    with second_co:
        st.markdown(
                """
                <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
                    <img src="https://i.imgur.com/EKx9qSk.png" style="max-width: 100%; border-radius: 5%;">
                </a>
                """,
                unsafe_allow_html=True,
            )

    st.divider()

    st.write("<h5>Select action</h5>", unsafe_allow_html=True)
    option = st.selectbox(
            "",
            (
                add,
                edit,
                delete,
            ),
            label_visibility="collapsed",
        )
    
    st.write("")

    if option == add:
        with st.form(key="form_add"):
            st.write("<h5>New Entry Title</h5>", unsafe_allow_html=True)
            title = st.text_input("Class", label_visibility="collapsed")
            st.write("<h5>Content</h5>", unsafe_allow_html=True)
            content = st.text_input(f"What would you like to know about?", placeholder="Type here ...", label_visibility="collapsed")
            start_co, end_co = st.columns(2)
            with start_co:
                start_date = st.date_input("Start date", datetime.date(2021, 1, 1))
            with end_co:
                end_date = st.date_input("End date", datetime.date(2021, 12, 31))
            submit_button = st.form_submit_button(label="Submit")

    elif option == edit:
        form_delete = st.selectbox(
            "Select entry to edit",
            (
                "Entry 1",
                "Entry 2",
                "Entry 3",
            ),
            label_visibility="collapsed",
        )
         
        st.write("")

        with st.form(key="form_edit"):
            st.write("<h5>Entry Title</h5>", unsafe_allow_html=True)
            title = st.text_input("Class", label_visibility="collapsed")
            st.write("<h5>Content</h5>", unsafe_allow_html=True)
            content = st.text_input(f"What would you like to know about?", placeholder="Type here ...", label_visibility="collapsed")
            start_co, end_co = st.columns(2)
            with start_co:
                start_date = st.date_input("Start date", datetime.date(2021, 1, 1))
            with end_co:
                end_date = st.date_input("End date", datetime.date(2021, 12, 31))
            submit_button = st.form_submit_button(label="Save")

    elif option == delete:
        form_delete = st.selectbox(
            "Select entry to delete",
            (
                "Entry 1",
                "Entry 2",
                "Entry 3",
            ),
            label_visibility="collapsed",
        )
        button_delete = st.button("Delete")