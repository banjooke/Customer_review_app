from langchain import OpenAI, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
import streamlit as st
import requests

#Initialize GROQ API KEY

openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]



#Define prompt template

template = """\
For the following text, extract the following \
information:

sentiment: Is the customer happy with the product? 
Answer Positive if yes, Negative if \
not, Neutral if either of them, or Unknown if unknown.

delivery_days: How many days did it take \
for the product to arrive? If this \
information is not found, output No information about this.

price_perception: How does it feel the customer about the price? 
Answer Expensive if the customer feels the product is expensive, 
Cheap if the customer feels the product is cheap,
not, Neutral if either of them, or Unknown if unknown.

Format the output as bullet-points text with the \
following keys:
- Sentiment
- How long took it to deliver?
- How was the price perceived?

Input example:
This dress is pretty amazing. It arrived in two days, just in time for my wife's anniversary present. It is cheaper than the other dresses out there, but I think it is worth it for the extra features.

Output example:
- Sentiment: Positive
- How long took it to deliver? 2 days
- How was the price perceived? Cheap

text: {review}
"""
#set up Langchain components


prompt = PromptTemplate(input_variable = ["review"], template=template,)
llm = OpenAI(api_key = openai_api_key)

#Strealit App Layout
st.title("Customer Feedback Analysis")
st.text("This app analyses customer feedback.")

def get_review():
    review_text = st.text_area(label = "Product review", label_visibility='collapsed', placeholder='Your product review..', key='review-input' )
    return review_text
review_input = get_review()

if len(review_input.split(" ")) > 200:
    st.write("Please enter a shorter product review. The maximum length is 200 words.")
    st.stop()

if st.button("Analyse"):
    #Generate response from the LLM
    with st.spinner("Analysing..."):
        response = prompt.format(review=review_input)
        key_data_extraction = llm(response)
        st.write(key_data_extraction)