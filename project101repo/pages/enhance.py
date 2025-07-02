import os
import requests
import streamlit as st
from textblob import TextBlob
from dotenv import load_dotenv
from pages.navbar import render_navbar
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import warnings

def enhance_func():
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")
    together_api_key = os.getenv("TOGETHER_API_KEY")

    if not hf_token or not together_api_key:
        st.error("Missing API keys in environment. Please check .env file.")
        return

    # Load FAISS vector index
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

    # Suppress the pickle warning temporarily
    warnings.filterwarnings('ignore', category=UserWarning)

    # Set environment variable (some versions check this)
    os.environ['LANGCHAIN_ALLOW_DANGEROUS_DESERIALIZATION'] = 'true'


    # Check if index exists
    index_path = r"C:\Users\shrey\OneDrive\Desktop\Projects\Marketing MLOps\project101repo\llm\faiss_index"

    if os.path.exists(index_path):
        try:
            # Try loading with the safety parameter
            db = FAISS.load_local(
                folder_path=index_path,
                embeddings=embedding,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            print(f"Error loading FAISS index: {e}")
            # Handle the error - maybe recreate the index or use alternative approach
    else:
        print("FAISS index not found. Please create it first.")


    # Navbar
    render_navbar()

    # API Setup
    HF_EMOTION_MODEL_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/bert-base-go-emotion"
    HF_HEADERS = {"Authorization": f"Bearer {hf_token}"}

    TOGETHER_API_URL = "https://api.together.xyz/v1/completions"
    TOGETHER_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
    TOGETHER_HEADERS = {
        "Authorization": f"Bearer {together_api_key}",
        "Content-Type": "application/json"
    }

    # RAG-enhanced LLM generation
    def improve_campaign_text(original_text, tone):
        relevant_docs = db.similarity_search(original_text, k=3)
        context = "\n".join([doc.page_content for doc in relevant_docs])

        prompt = f"""
You are a top-tier social media marketing expert who has all the knowledge to do their job, understands trends using context, audience psychology, and engagement strategies with respect to product the user wants to market.
Based on the context below from past campaigns and trends improve the following marketing text in a *{tone.lower()}* tone to make it more engaging and persuasive. Make a sense of urgency and excitement in the text, and make it more likely to convert. Use the context to add relevant details, statistics, or examples that enhance the message.
If you give a good output, you will be rewarded with a bonus. If you give a bad output, you will be fired. So do your best.

Context:
{context}

Original Text:
\"{original_text}\"

Improved Version:
        """

        payload = {
            "model": TOGETHER_MODEL,
            "prompt": prompt,
            "max_tokens": 300,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9,
            "repetition_penalty": 1.1
        }

        response = requests.post(TOGETHER_API_URL, headers=TOGETHER_HEADERS, json=payload)
        if response.status_code == 200:
            return response.json().get("choices", [{}])[0].get("text", "").strip() or "[No output returned]"
        else:
            return f"[ERROR] {response.status_code}: {response.text}"

    def get_sentiment(text):
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            return "Positive"
        elif polarity < -0.2:
            return "Negative"
        else:
            return "Neutral"

    def predict_success(text):
        sentiment = TextBlob(text).sentiment.polarity
        return "Likely to Succeed" if (len(text) > 60 and sentiment > 0.2) else "Unlikely to Succeed"

    def get_emotion_scores(text):
        response = requests.post(HF_EMOTION_MODEL_URL, headers=HF_HEADERS, json={"inputs": text})
        if response.status_code == 200:
            results = response.json()[0]
            top_emotions = sorted(results, key=lambda x: x['score'], reverse=True)[:3]
            return ", ".join([f"{e['label']} ({e['score']:.2f})" for e in top_emotions])
        else:
            return f"[ERROR] Emotion API: {response.status_code} - {response.text}"

    # UI
    user_input = st.text_area("Enter your campaign text", height=100)
    tone = st.selectbox("Choose the tone", ["Exciting", "Professional", "Funny", "Friendly", "Urgent"])

    if st.button("Improve and Analyze"):
        if not user_input.strip():
            st.warning("Please enter your campaign text.")
        else:
            with st.spinner("Working on it..."):
                improved = improve_campaign_text(user_input, tone)
                sentiment = get_sentiment(improved)
                prediction = predict_success(improved)
                emotion_scores = get_emotion_scores(improved)

                st.markdown("### Improved Campaign Text")
                st.success(improved)

                st.markdown("### Sentiment")
                st.info(sentiment)

                st.markdown("### Predicted Success")
                st.warning(prediction)

                st.markdown("### Top Emotions")
                st.info(emotion_scores)
