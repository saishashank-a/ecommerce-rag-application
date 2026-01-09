import streamlit as st
import requests

import os

# Configuration
# Default to localhost for local testing, can be overridden by env var
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="E-commerce RAG", layout="wide")

st.title("🤖 E-commerce RAG Assistant")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    mode = st.radio("Choose Mode", ["Search Products", "Chat with AI"])
    
    st.header("Settings")
    k_results = st.slider("Number of Contexts", min_value=1, max_value=5, value=3)

# --- SEARCH MODE ---
if mode == "Search Products":
    st.subheader("🔍 Semantic Product Search")
    query = st.text_input("Enter your search query:", placeholder="e.g., healthy dog food for puppies")

    if query:
        with st.spinner("Searching vector database..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/search",
                    json={"query": query, "k": k_results}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    if not results:
                        st.warning("No results found.")
                    else:
                        st.success(f"Found {len(results)} matches!")
                        for i, res in enumerate(results):
                            with st.expander(f"#{i+1} - {res['summary']} (Score: {res['score']:.2f})", expanded=True):
                                st.write(f"**Product ID:** {res['product_id']}")
                                st.info(res['review_snippet'])
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Backend Error: {e}")

# --- CHAT MODE ---
elif mode == "Chat with AI":
    st.subheader("💬 Chat with your Data")
    st.markdown("Ask questions, and the AI will answer based on the reviews.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! Ask me anything about our products."}]

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("What is the best dog food?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Retrieving products & generating answer..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/chat",
                        json={"query": prompt}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        answer = data.get("answer", "No answer generated.")
                        context = data.get("context", [])
                        
                        st.markdown(answer)
                        
                        # Show sources used
                        if context:
                            with st.expander("📚 Sources (RAG Context)"):
                                for c in context:
                                    st.caption(f"**{c['summary']}**: {c['review_snippet'][:100]}...")
                        
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"Failed to get answer from backend: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
