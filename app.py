import streamlit as st
from streamlit_extras.stoggle import stoggle
from jar import get_jars_dct_title_key, get_jar_ledger_as_pd, get_jar_ledger_as_pd
from jar import jar_commit, delete_clip_using_page_id, edit_clip_content, edit_clip_title, edit_jar_title
from sync import sync
from analytics import process_df, get_num_entries
from jar_progress import visualize
import streamlit.components.v1 as components
import time
import gspread
import pytz
import datetime

#####################################
# FUNCTIONS
#####################################

BORDER_COLOR = "rgba(239, 245, 255, 0.69)"
BG_COLOR = "rgba(14, 17, 23, 1)"

def calculate_average_entries_per_week(data):
    start_times = data["Start Time"].to_list()
    
    if len(start_times) == 0:
        return 0
    
    # Calculate the number of weeks spanned by entries
    min_date = min(start_times)
    max_date = max(start_times)
    delta = max_date - min_date
    weeks = max(1, delta.days / 7)
    average_entries_per_week = len(start_times) / weeks
    
    return round(average_entries_per_week, 2)

# Function to generate HTML for a single card with a title and a static statistic number
def generate_card_html(title, statistic, card_id):
    card_html = f"""
    <div style="border: 2px solid rgba(239, 245, 255, 0.69); margin-bottom: 32px; padding: 20px; border-radius: 10px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
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

        st.button("Neo's JARs", use_container_width=True, type="primary")

        st.button("Ryusei's JARs", use_container_width=True)

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
    df = process_df(df)

    # with st.spinner('Syncing, please wait...'):
    #     sync(selected_database_id) 

    total_entries = get_num_entries(df)
    average_entries_per_week = calculate_average_entries_per_week(df)

    first_co, second_co = st.columns(2)
    with first_co:
        def generate_full_html():
            card_1_html = generate_card_html("Total Entries", total_entries, "1")
            card_2_html = generate_card_html("Avg. Entries Per Week", average_entries_per_week, "2")
            
            full_html = f"""
            <html>
            <head>
                <style>
                    body {{
                        background-color: rgb(14, 17, 23);
                        font-family: 'Inter', sans-serif;
                    }}
                </style>
            </head>
            <body>
                {card_1_html}
                {card_2_html}
            </body>
            </html>
            """
            return full_html
        
        components.html(generate_full_html(), height=350)

    with second_co:
        plot = visualize(df, theme='basic', starting_jar_dim=4)
        
        # Directly display the plot using the appropriate Streamlit function
        # If visualize(df) returns a Matplotlib figure
        st.pyplot(plot)
        
    st.divider()

    st.write("<h5>Select action</h5>", unsafe_allow_html=True)
    edit_option = st.selectbox(
            "",
            (
                add,
                edit,
                delete,
            ),
            label_visibility="collapsed",
        )
    
    st.write("")

    if edit_option == add:
        with st.form(key="form_add"):
            st.write("<h5>New Entry Title</h5>", unsafe_allow_html=True)
            title = st.text_input("Class", label_visibility="collapsed")
            st.write("<h5>Content</h5>", unsafe_allow_html=True)
            content = st.text_input(f"What would you like to know about?", placeholder="Type here ...", label_visibility="collapsed")
            start_co, end_co = st.columns(2)

            # Get current date and time
            now = datetime.datetime.now()

            # Round down the current time to the nearest hour
            start_time_default = now.replace(minute=0, second=0, microsecond=0)

            # Calculate end date and time (start time + 1 hour)
            end_time_default = start_time_default + datetime.timedelta(hours=1)
            end_date_and_time = end_time_default

            with start_co:
                # Set the start date and time inputs with defaults to today and the current hour
                start_date = st.date_input("Start date", now.date(), format="MM/DD/YYYY", key="start_date")
                start_time = st.time_input("Start time", start_time_default, key="start_time")

                start_date_and_time = datetime.datetime.combine(start_date, start_time)

            with end_co:
                # Set the end date and time inputs with defaults based on the calculated end date and time
                end_date = st.date_input("End date", end_date_and_time.date(), key="end_date", format="MM/DD/YYYY")
                end_time = st.time_input("End time", end_date_and_time.time(), key="end_time")

                end_date_and_time = datetime.datetime.combine(end_date, end_time)

            submit_button = st.form_submit_button(label="Submit")

            # get a json serializable string of the start date and time
            pst_timezone = pytz.timezone('America/Los_Angeles')
            start_date_and_time_pst = start_date_and_time.replace(tzinfo=pst_timezone)
            end_date_and_time_pst = end_date_and_time.replace(tzinfo=pst_timezone)

            start_date_and_time_str = start_date_and_time_pst.isoformat()
            end_date_and_time_str = end_date_and_time_pst.isoformat()

            if submit_button:
                jar_commit(selected_database_id, title, content, start_date_and_time_str, end_date_and_time_str)
                st.success("Entry added successfully!", icon="✅")

    elif edit_option == edit:

        get_jar_ledger_as_pd(selected_database_id)

        # get the tuple of the title column 
        title_tuple = tuple(df["Title"])
        
        form_delete = st.selectbox(
            "Select entry to edit",
            title_tuple,
            label_visibility="collapsed",
        )

        page_id = df[df["Title"] == form_delete]["Page Id"].values[0]

        # get the content of the selected entry
        old_content = df[df["Title"] == form_delete]["Content"].values[0]
        old_title = df[df["Title"] == form_delete]["Title"].values[0]

        with st.form(key="form_edit"):
            st.write("<h5>Editing Entry Title</h5>", unsafe_allow_html=True)
            title = st.text_input("Class", label_visibility="collapsed", value=old_title)
            st.write("<h5>Editing Content</h5>", unsafe_allow_html=True)
            content = st.text_input(f"What would you like to know about?", placeholder="Type here ...", label_visibility="collapsed", value=old_content)
            submit_button = st.form_submit_button(label="Save")

            if submit_button:
                edit_clip_content(page_id, content)
                edit_clip_title(page_id, title)
                st.success("Entry edited successfully!", icon="✅")

    elif edit_option == delete:

        get_jar_ledger_as_pd(selected_database_id)

        # get the tuple of the title column 
        title_tuple = tuple(df["Title"])
        
        form_delete = st.selectbox(
            "Select entry to delete",
            title_tuple,
            label_visibility="collapsed",
        )
        button_delete = st.button("Delete")

        if button_delete:
            page_id = df[df["Title"] == form_delete]["Page Id"].values[0]
            delete_clip_using_page_id(page_id)

            st.success("Entry deleted successfully!", icon="✅")