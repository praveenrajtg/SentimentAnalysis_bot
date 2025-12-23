import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sentiment_analyzer import SentimentAnalyzer
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Sentiment Analysis Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Initialize
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = SentimentAnalyzer()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS
st.markdown("""
<style>
.main-header { 
    text-align: center; 
    color: #00D9FF; 
    font-size: 3em; 
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    margin-bottom: 30px; 
}
.chat-message { 
    padding: 15px; 
    margin: 10px 0; 
    border-radius: 15px;
    font-size: 1.1em;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
.user-message { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: 20px;
    border: 2px solid #00D9FF;
}
.bot-message { 
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    margin-right: 20px;
    border: 2px solid #FFD700;
}
.sentiment-positive { color: #00FF00; font-weight: bold; font-size: 1.2em; }
.sentiment-negative { color: #FF4444; font-weight: bold; font-size: 1.2em; }
.sentiment-neutral { color: #FFD700; font-weight: bold; font-size: 1.2em; }
.stApp {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
}
.stTextInput input {
    background-color: #2d3748 !important;
    color: white !important;
    border: 2px solid #00D9FF !important;
    font-size: 1.1em !important;
}
.stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    font-weight: bold !important;
    font-size: 1.1em !important;
    border: 2px solid #00D9FF !important;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🤖 Sentiment Analysis Chatbot</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    
    if st.session_state.chat_history:
        # Simple statistics
        sentiments = [msg['sentiment'] for msg in st.session_state.chat_history]
        pos_count = sentiments.count('positive')
        neg_count = sentiments.count('negative')
        neu_count = sentiments.count('neutral')
        total = len(sentiments)
        
        # Pie chart
        fig_pie = px.pie(
            values=[pos_count, neg_count, neu_count],
            names=['Positive', 'Negative', 'Neutral'],
            title="Sentiment Distribution",
            color_discrete_map={
                'Positive': '#4CAF50',
                'Negative': '#F44336', 
                'Neutral': '#FF9800'
            }
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Statistics
        st.subheader("📈 Statistics")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Messages", total)
            st.metric("Positive %", f"{(pos_count/total*100):.1f}%")
        with col2:
            avg_score = sum(msg['score'] for msg in st.session_state.chat_history) / total
            st.metric("Avg Score", f"{avg_score:.3f}")
            st.metric("Negative %", f"{(neg_count/total*100):.1f}%")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Chat Interface")
    
    # Chat history
    for msg in st.session_state.chat_history:
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You:</strong> {msg['user_message']}
            <br><small>Sentiment: <span class="sentiment-{msg['sentiment']}">{msg['sentiment'].title()}</span> 
            (Score: {msg['score']})</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>Bot:</strong> {msg['bot_response']}
        </div>
        """, unsafe_allow_html=True)
    
    # Input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Type your message:", placeholder="How are you feeling today?")
        if st.form_submit_button("Send 📤"):
            if user_input:
                result = st.session_state.analyzer.process_message(user_input)
                st.session_state.chat_history.append(result)
                st.rerun()

with col2:
    st.subheader("ℹ️ How it Works")
    st.info("""
    **Sentiment Detection:**
    - 😊 **Positive**: Score > 0.1
    - 😐 **Neutral**: Score -0.1 to 0.1  
    - 😞 **Negative**: Score < -0.1
    """)
    
    if st.session_state.chat_history:
        latest = st.session_state.chat_history[-1]
        
        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=latest['score'],
            title={'text': "Latest Sentiment"},
            gauge={
                'axis': {'range': [-1, 1]},
                'steps': [
                    {'range': [-1, -0.1], 'color': "lightcoral"},
                    {'range': [-0.1, 0.1], 'color': "lightyellow"},
                    {'range': [0.1, 1], 'color': "lightgreen"}
                ]
            }
        ))
        fig_gauge.update_layout(height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("---")
st.markdown("**Made by Praveen** | Built with ❤️ using Streamlit | Real-time Sentiment Analysis")