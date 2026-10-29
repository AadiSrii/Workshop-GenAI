# Daily Learning Log

A small Streamlit app where I log what I learn each day, hours spent, and how confident I feel. Built for my Day 1 workshop practice.

## What I practiced
- Creating and activating a Python virtual environment
- Building a form-based UI with Streamlit (text input, sliders, buttons)
- Keeping state between reruns with `st.session_state`
- Tracking the project with Git and pushing to GitHub

## Run it locally
```bash
git clone <your-repo-url>
cd <your-repo-folder>
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install streamlit
streamlit run app.py
```

## Files
- `app.py`: the Streamlit app
- `.gitignore`: keeps `venv/` and editor folders out of Git