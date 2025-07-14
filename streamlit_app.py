import streamlit as st

main_page = st.Page("app.py", title="Cost Calculator", icon="🧮")
page_2 = st.Page("past_data_page.py", title="Past Data", icon="🕰️")

# nav setup 
pg = st.navigation([main_page, page_2])

pg.run()