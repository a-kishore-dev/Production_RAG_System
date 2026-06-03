import os
import uuid
import tempfile
import streamlit as st
from dotenv import load_dotenv
from src.pipeline.rag_pipeline import RAGPipeline
from streamlit import session_state as ss


def config_rag(collection_name, gemini_model_name, gemini_api_key, groq_model_name, groq_api_key):
    with st.container(horizontal=True, horizontal_alignment="right"):
        if st.button("Upload Document"):
            load_document(collection_name, gemini_model_name, gemini_api_key, groq_model_name, groq_api_key)

@st.dialog("Add document")
def load_document(collection_name, gemini_model_name, gemini_api_key, groq_model_name, groq_api_key):
    uploaded_files = st.file_uploader("Upload the pdf files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        with tempfile.TemporaryDirectory() as temp_dir:
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(dir=temp_dir,delete=False, suffix=".pdf") as temp_file:
                    temp_file.write(uploaded_file.read())
            try:
                with st.spinner("Processing documents"):
                    ss.rag = RAGPipeline(
                            dir_path=temp_dir,
                            collection_name=collection_name,
                            gemini_model_name=gemini_model_name,
                            gemini_api_key=gemini_api_key,
                            groq_model_name=groq_model_name,
                            groq_api_key=groq_api_key
                        )
                    chat = get_current_chat()
                    chat["uploaded_documents"] = True
                st.success("File uploaded successfully", icon="✅")
            except Exception as e:
                st.warning("The Upload Failed", icon="❌") 

def page():
    with st.container(horizontal=True, horizontal_alignment="right"):
        delete_current_chat()

    chat = get_current_chat()

    for message in chat["messages"]:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"], text_alignment="right")
            else:
                st.markdown(message["content"])
    
    if input_msg := st.chat_input("What is up?"):
        if chat["uploaded_documents"] == True:
            with st.chat_message("user"):
                st.markdown(input_msg, text_alignment="right")
            chat["messages"].append({"role":"user", "content": input_msg})
            
            ai_response, nodes_with_score = ss.rag.predict(query=input_msg)
            with st.chat_message("assistant"):
                st.markdown(ai_response)
            chat["messages"].append({"role":"assistant", "content": ai_response})
        else:
            st.warning("Please Upload a Document", icon="‼️")

def init_state():
    if "store" not in ss:
        ss.store = {}
    
    if "chats" not in ss:
        first_chat_id = str(uuid.uuid4())
        
        ss.chats = {
            first_chat_id:{
                "session_id": first_chat_id,
                "messages": [],
                "uploaded_documents": False
            }
        }

        ss.current_chat = first_chat_id

def get_current_chat():
    return ss.chats[ss.current_chat]

def create_new_chat():
    chat_id = str(uuid.uuid4())
    ss.chats[chat_id] = {
        "session_id": chat_id,
        "messages": [],
        "uploaded_documents": False
    }
    ss.current_chat = chat_id

def delete_current_chat():
    if st.button("Delete"):
        current_chat_id = ss.current_chat
        del ss.chats[current_chat_id]
        if ss.chats:
            ss.current_chat = next(iter(ss.chats))
        else:
            create_new_chat()
        st.rerun()

def draw_sidebar():
    with st.sidebar:
        if st.button("+ New Page"):
            create_new_chat()
            st.rerun()
        
        st.divider()

        for chat_id, chat_data in ss.chats.items():
            first_msg = (
                chat_data["messages"][0]["content"][:10]
                if chat_data["messages"]
                else "New Chat"
            )
            if st.button(first_msg, key=chat_id):
                ss.current_chat = chat_id
                st.rerun()

def main():
    load_dotenv()

    gemini_api_key = os.getenv("GOOGLE_API_KEY")
    groq_api_key = os.getenv("GROQ_API_KEY")
    st.set_page_config(page_title="Production RAG System", page_icon="images/icon.png", layout="wide")
    init_state()
    config_rag(collection_name="knowledge_base",
               gemini_model_name="gemini-2.5-flash",
               gemini_api_key=gemini_api_key,
               groq_model_name="llama-3.1-8b-instant",
               groq_api_key=groq_api_key)
    page()
    
    draw_sidebar()
    
if __name__ == "__main__":
    main()