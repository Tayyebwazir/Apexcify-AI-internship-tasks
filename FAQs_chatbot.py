import streamlit as st
import nltk
import string
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datasets import load_dataset

# Streamlit UI Configuration - MUST BE FIRST!
st.set_page_config(
    page_title="E-commerce FAQ Chatbot",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Download NLTK stopwords
nltk.download("stopwords", quiet=True)

# Load E-commerce FAQ dataset
@st.cache_data
def load_faq_dataset():
    """Load and cache the E-commerce FAQ dataset"""
    try:
        # Load the dataset from Hugging Face
        ds = load_dataset("Andyrasika/Ecommerce_FAQ")

        # Convert to pandas DataFrame for easier handling
        df = pd.DataFrame(ds['train'])

        # Extract questions and answers
        faq_questions = df['question'].tolist()
        faq_answers = df['answer'].tolist()

        print(f"Loaded {len(faq_questions)} E-commerce FAQ entries successfully!")
        return faq_questions, faq_answers, df, None

    except Exception as e:
        error_msg = f"❌ Error loading E-commerce FAQ dataset: {str(e)}"
        return [], [], None, error_msg

# Load the dataset
faq_questions, faq_answers, faq_df, error_message = load_faq_dataset()

# Handle loading errors
if error_message:
    st.error(error_message)
    st.error("Please make sure you have internet connection and the 'datasets' library installed.")
    st.stop()

# Preprocessing function
def preprocess(text):
    """Clean and preprocess text for better matching"""
    if not text:
        return ""

    text = text.lower()
    # Remove punctuation and split into tokens
    tokens = text.split()
    # Remove stopwords and punctuation, keep only meaningful words
    tokens = [word.strip(string.punctuation) for word in tokens
              if word.strip(string.punctuation) and word.lower() not in stopwords.words("english")]
    return " ".join(tokens)

# Preprocess all FAQ questions
preprocessed_questions = [preprocess(q) for q in faq_questions]

# TF-IDF Vectorization for similarity matching
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)

# Function to find the best answer
def find_best_answer(user_question, threshold=0.1):
    """Find the best matching answer for user question"""
    if not user_question.strip():
        return None, 0

    user_processed = preprocess(user_question)
    if not user_processed:
        return None, 0

    user_vec = vectorizer.transform([user_processed])
    similarity_scores = cosine_similarity(user_vec, tfidf_matrix)
    best_match_index = similarity_scores.argmax()
    best_score = similarity_scores[0][best_match_index]

    if best_score > threshold:
        return faq_answers[best_match_index], best_score
    else:
        return None, best_score

# Main UI
st.title("🛒 E-commerce FAQ Chatbot")
st.markdown("*Your intelligent shopping assistant for all e-commerce questions!*")
st.markdown("---")

# Sidebar with FAQ list and dataset info
with st.sidebar:
    st.header("�️ E-commerce FAQ Topics")
    st.markdown("**Sample questions you can ask:**")

    # Show first 7 questions as examples
    for i, question in enumerate(faq_questions[:7], 1):
        st.markdown(f"{i}. {question}")
    if len(faq_questions) > 7:
        st.markdown(f"... and {len(faq_questions) - 7} more!")

    st.markdown("---")
    st.markdown(f"**📊 Dataset Info:**")
    st.markdown(f"- Total FAQs: {len(faq_questions)}")
    st.markdown(f"- Source: Andyrasika/Ecommerce_FAQ")
    st.markdown(f"- Topics: Shopping, Orders, Returns, etc.")

# Main chat interface
st.markdown("### 💬 Ask me about shopping, orders, returns, or any e-commerce topic!")
user_input = st.text_input("Type your question here:", placeholder="e.g., How do I return an item?")

col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    ask_button = st.button("🔍 Get Answer", type="primary")
with col2:
    if st.button("🔄 Clear"):
        st.rerun()
with col3:
    if st.button("📊 Show Dataset Info"):
        st.info(f"**Dataset Statistics:**\n\n"
                f"- Total Questions: {len(faq_questions)}\n"
                f"- Average Question Length: {sum(len(q.split()) for q in faq_questions) / len(faq_questions):.1f} words\n"
                f"- Average Answer Length: {sum(len(a.split()) for a in faq_answers) / len(faq_answers):.1f} words")

        # Show some sample categories based on keywords
        categories = {}
        keywords = {
            'Shipping': ['ship', 'delivery', 'shipping', 'deliver'],
            'Returns': ['return', 'refund', 'exchange'],
            'Orders': ['order', 'purchase', 'buy', 'cart'],
            'Payment': ['pay', 'payment', 'card', 'billing'],
            'Account': ['account', 'login', 'profile', 'register']
        }

        for category, words in keywords.items():
            count = sum(1 for q in faq_questions if any(word in q.lower() for word in words))
            if count > 0:
                categories[category] = count

        if categories:
            st.markdown("**Question Categories:**")
            for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                st.markdown(f"- {cat}: {count} questions")

if ask_button:
    if user_input.strip():
        with st.spinner("🔍 Searching for the best answer..."):
            answer, confidence = find_best_answer(user_input)

            if answer:
                st.success("✅ **Answer Found!**")
                st.markdown(f"**Q:** {user_input}")
                st.markdown(f"**A:** {answer}")

                # Show confidence score
                confidence_percentage = confidence * 100
                if confidence_percentage > 70:
                    st.info(f"🎯 Confidence: {confidence_percentage:.1f}% (High)")
                elif confidence_percentage > 40:
                    st.info(f"🎯 Confidence: {confidence_percentage:.1f}% (Medium)")
                else:
                    st.info(f"🎯 Confidence: {confidence_percentage:.1f}% (Low)")
            else:
                st.warning("❓ **Sorry, I couldn't find a good match for your question.**")
                st.markdown("**Suggestions:**")
                st.markdown("- Try rephrasing your question")
                st.markdown("- Check the sidebar for available topics")
                st.markdown("- Use simpler keywords")
    else:
        st.error("❌ Please type a question before clicking the button.")

# Footer
st.markdown("---")
st.markdown("*💡 Tip: Try asking questions about shopping, orders, returns, shipping, payments, or any e-commerce topic!*")
st.markdown("*🛒 Powered by the Andyrasika/Ecommerce_FAQ dataset*")
