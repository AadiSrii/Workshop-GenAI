import streamlit as st
from google import genai

st.set_page_config(page_title="MERN & Java Study Buddy", page_icon="🎓", layout="wide")

# ---------- Knowledge base: the "library" the assistant is allowed to read ----------
NOTES = [
    {"topic": "MongoDB", "text": "MongoDB is a NoSQL database that stores data as flexible JSON-like documents (BSON) inside collections instead of rows and tables."},
    {"topic": "Express", "text": "Express is a minimal Node.js web framework. Middleware functions run in order for each request and can modify the request, the response, or end the cycle."},
    {"topic": "React", "text": "React builds UIs from reusable components. State changes trigger a re-render, and hooks like useState and useEffect let function components manage state and side effects."},
    {"topic": "Node.js", "text": "Node.js runs JavaScript outside the browser using the V8 engine. Its event loop handles many I/O operations without blocking by using callbacks, promises and async/await."},
    {"topic": "REST API", "text": "A REST API exposes resources through URLs and uses HTTP methods: GET reads, POST creates, PUT or PATCH updates, DELETE removes. Responses carry status codes like 200, 201, 404 and 500."},
    {"topic": "JWT", "text": "A JSON Web Token has a header, payload and signature. The server signs it after login, and the client sends it with later requests so the server can verify identity without storing a session."},
    {"topic": "Java OOP", "text": "Java's four OOP pillars are encapsulation, inheritance, polymorphism and abstraction. They help organise code into reusable objects with clear responsibilities."},
    {"topic": "Java Collections", "text": "Java Collections include List (ordered, allows duplicates), Set (unique items) and Map (key-value pairs). ArrayList and HashMap are the most commonly used implementations."},
    {"topic": "Git", "text": "Git tracks changes in snapshots called commits. Branches let you work on features separately, and a pull request proposes merging one branch into another."},
]


# ---------- Heavy imports happen here (not at the top) so the page opens instantly ----------
@st.cache_resource(show_spinner="Loading the embedding model (first time only)...")
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource(show_spinner="Indexing notes...")
def embed_notes(_model):
    return _model.encode([n["text"] for n in NOTES], convert_to_tensor=True)


def retrieve(question, model, note_vectors, top_k):
    """Find the notes whose meaning is closest to the question."""
    from sentence_transformers import util
    q_vec = model.encode(question, convert_to_tensor=True)
    hits = util.semantic_search(q_vec, note_vectors, top_k=top_k)[0]
    return [(NOTES[h["corpus_id"]], float(h["score"])) for h in hits]


def ask_gemini(api_key, question, context_notes):
    client = genai.Client(api_key=api_key)
    context = "\n".join(f"- ({n['topic']}) {n['text']}" for n, _ in context_notes)
    prompt = (
        "You are a friendly tutor. Answer the student's question using ONLY the notes below. "
        "If the notes do not contain the answer, say so honestly.\n\n"
        f"NOTES:\n{context}\n\nQUESTION: {question}\n\nAnswer in simple words with a short everyday analogy."
    )
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text


# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API key", type="password", help="Get one free at aistudio.google.com/apikey")
    top_k = st.slider("Notes to retrieve", 1, 5, 2)
    st.divider()
    st.subheader("Topics I know")
    for topic in sorted({n["topic"] for n in NOTES}):
        st.write(f"• {topic}")

# ---------- Main page ----------
st.title("🎓 MERN & Java Study Buddy")
st.write("Ask a question. I first search my notes, then explain the answer in simple words.")

question = st.text_input("Your question", placeholder="e.g. How does JWT authentication work?")

if st.button("Ask", type="primary"):
    if not api_key:
        st.warning("Please add your Gemini API key in the sidebar.")
    elif not question.strip():
        st.warning("Type a question first.")
    else:
        try:
            model = load_model()
            vectors = embed_notes(model)
            found = retrieve(question, model, vectors, top_k)
            with st.spinner("Thinking..."):
                answer = ask_gemini(api_key, question, found)

            st.subheader("Answer")
            st.write(answer)

            with st.expander("📚 Notes I used"):
                for note, score in found:
                    st.markdown(f"**{note['topic']}** (match: {score:.2f})")
                    st.write(note["text"])
        except Exception as err:
            st.error(f"Something went wrong: {err}")