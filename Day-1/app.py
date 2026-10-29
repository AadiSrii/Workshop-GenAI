import streamlit as st
from datetime import date

st.set_page_config(page_title="Daily Learning Log", page_icon="📓")

st.title("📓 Daily Learning Log")
st.caption("Write down what you learned today, like a diary for your brain.")

# session_state is the app's short-term memory: Streamlit re-runs the
# whole script on every click, so without it the list would reset each time.
if "entries" not in st.session_state:
    st.session_state.entries = []

with st.form("log_form", clear_on_submit=True):
    topic = st.text_input("What did you learn?")
    hours = st.slider("Hours spent", 0.5, 8.0, 1.0, step=0.5)
    confidence = st.select_slider(
        "How confident do you feel?", ["Lost", "Shaky", "Okay", "Good", "Nailed it"], value="Okay"
    )
    submitted = st.form_submit_button("Add to log")

if submitted and topic.strip():
    st.session_state.entries.append(
        {"Date": date.today().isoformat(), "Topic": topic.strip(), "Hours": hours, "Confidence": confidence}
    )
    st.success("Saved!")

st.subheader("Your log")
if st.session_state.entries:
    st.table(st.session_state.entries)
    total = sum(e["Hours"] for e in st.session_state.entries)
    st.metric("Total hours studied", f"{total} h")
else:
    st.info("Nothing logged yet. Add your first entry above.")