import streamlit as st
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from database import Database_Manager

st.cache_data()
def get_text():
      name_db = 'pages/details.db'
      data = Database_Manager(name_db).get_main_db_from_venue()

      data = data[data['Details'] != '']
      values_list = []
      for c in ['Details', 'Reservation: Venue']:
            values = data[c].tolist()
            # transform in strings
            values = [f'{c}: {i}' for i in values]
            values_list.append(values)

      # values_list = [data['Details'].tolist(), data['Reservation: Venue'].tolist()]
      # need to join the two lists element wise
      data = [' '.join(i) for i in zip(*values_list)]
      data = '      '.join(data)
      return data


def generate_response(query_text, docs):
        documents = docs
        # Split documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.create_documents(documents)
        # Select embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        # Create a vectorstore from documents
        db = Chroma.from_documents(texts, embeddings)
        # Create retriever interface
        retriever = db.as_retriever()
        # Create QA chain
        qa = RetrievalQA.from_chain_type(llm=OpenAI(openai_api_key=openai_api_key), chain_type='stuff', retriever=retriever)
        return qa.run(query_text)


# Page title
openai_api_key = st.secrets["OPENAI_API_KEY"]
prompt = st.chat_input('Ask the Doc App')
docs = get_text()

if prompt:
      response = generate_response(prompt, docs)