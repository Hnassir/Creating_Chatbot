import nltk

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import string

import streamlit as st



# Load the text file and preprocess the data
with open('Korea Information - Culture.txt', 'r', encoding='utf-8') as f:
    data = f.read()
    

# Tokenize the text into sentences
sentences = sent_tokenize(data)

# Define a function to preprocess each sentence
def preprocess(sentence):

    # Tokenize the sentence into words
    words = word_tokenize(sentence)

    # Remove stopwords and punctuation
    words = [word.lower() for word in words if word.lower() not in stopwords.words('english') and word not in string.punctuation and word.isalnum()]
    
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    words = [lemmatizer.lemmatize(word,pos='v') for word in words]
    words = [lemmatizer.lemmatize(word,pos='a') for word in words]
    words = [lemmatizer.lemmatize(word,pos='r') for word in words]

    return words


# Preprocess each sentence in the text
corpus = [preprocess(sentence) for sentence in sentences]


# Define a function to find the most relevant sentence given a query
def get_most_relevant_sentence(query):

    # Preprocess the query
    query = preprocess(query)

    # Compute the similarity between the query and each sentence in the text
    max_similarity = 0

    for sentence in corpus:

        similarity = len(set(query).intersection(sentence)) / len(set(query).union(sentence))
        
        if similarity > max_similarity:
            max_similarity = similarity
            index=corpus.index(sentence)

    try:
        return index
    
    except:
        return st.warning('nothing found while searching')
        


def chatbot(question):
    
    # Return the answer
    return get_most_relevant_sentence(question)



def main():


    with st.sidebar:

        st.header('SideBar')
        with st.container(border=True,width='content'):
            page=st.radio('switch pages',options=['Text','ChatBot'],horizontal=True,index=1)


    if page =='Text' :
        with st.container(border=True):
            st.write(data)

    else:    

        clm1,clm2=st.columns([0.3,0.7])

        with clm2:

            if 'hist' not in st.session_state:
                st.session_state.hist={}

            with st.container(border=True,width=300):
                    
                col1, col2 = st.columns([0.35,0.65],vertical_alignment='center')

                with col2:
                    st.title("Chatbot")

                with col1 :
                    st.image('Image1.png',width=100)


            with st.container(border=True):

                st.write("Hello ! I'm a ChatBot. \n + Ask me anything about the topic in the text **(Use SideBar)**. ")
                # Get the user's question

                question = st.text_input("You: ")
                # Call the chatbot function with the question and display the response           
            
            
            # Create a button to submit the question 
            if st.button("Submit"):

                res=chatbot(question)

                if isinstance(res,int): 

                    st.write('chatbot : ',sentences[res])
                    st.session_state.hist[question]=sentences[res]

                else :

                    st.session_state.hist[question]='nothing found while searching'

                


        with clm1:

            with st.container(border=True):

                st.container(border=True).markdown('chat Histrory :')

                show =st.button('show history')

                val=True

                if show :

                    for key in st.session_state.hist.keys():
                        st.write(key,' : ',st.session_state.hist[key])

                    val=False

                if st.button('clear history',disabled=val) :

                    if 'hist' in st.session_state :

                        st.session_state.hist.clear()
                        st.info('history cleared')
                        
                       



if __name__ == "__main__":
    main()



