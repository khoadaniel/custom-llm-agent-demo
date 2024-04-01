import os
import streamlit as st
from speech_to_text import speech_to_text
from my_langchain.agent import LangChainCustomAgent

custom_agent = LangChainCustomAgent()

st.set_page_config(
    page_title="Custom LLM Agent",
    page_icon="🤖",
    layout="wide"
)


st.title("LLM-powered Hands-free POS Demo")

st.sidebar.markdown("**About this project**")

st.sidebar.image(
    "./img/zeit-fur-brot.png",
    caption="Zeit für Brot Eberswalder | Photo: by detureprojects.com"
)

st.sidebar.write(
    """
## 🧀 The Inspiration
 am a fan of the tasty Käsedings at Zeit für Brot and I've spent quite a bit of time hanging out at their busy Eberswalder spot. It's where my interest in the tasty breads collides with the reality of waiting in line..
I noticed and hypothesized that, to maintain hygiene, cashiers don't directly handle the food. There would be one cashier and one other staff working in a pair to deal with customers. The cashiers only manage orders and payments, leaving food handling to their peers.
\n➡️ This observation sparked an idea: What if we could make the ordering and payment process more efficient, enhancing customer satisfaction, streamlining staff workflow, and ultimately boosting Zeit für Brot's revenue (sorry for the buzzwords)?

## 💡 The Solution: The Integration of the LLM-agent
This solution proposes integrating a custom LLM agent into the Point of Sale (POS) system. The agent will translate the staff's orders into API requests, registering items in the POS system without manual entry.

\nThis is an open-source project and you can find the codes on [GitHub](https://github.com/khoadaniel/home-assist).
""")


st.sidebar.write(
    """
    ## 👋 About me:
    
    I am Daniel Le. I currently work as a Data Engineer - with great passion for Machine Learning.
    I am based in Berlin, Germany and I am interested in new technologies and how they can be implemented to solve real-world problems.
    If you have any questions, feel free to reach out to me on [LinkedIn](https://www.linkedin.com/in/khoadaniel/).""")


HOST = os.getenv("HOST", "local")
if HOST == "local":
    if st.button("Wake up the Agent"):
        st.write("🎤️ Please speak now, the agent will know when you are done.")
        converted_text = speech_to_text()
        # Feed the conversation to the agent to make POST requests
        custom_agent.make_requests(converted_text)
else:
    st.markdown(
        "*No audio device detected. Please use the type-in box below to enter your order instead ⤵️*")
    manual_input_text = st.chat_input("Enter the input here:")

    if manual_input_text is not None:
        st.markdown("👨🏻‍💻 You entered: " + manual_input_text)
        custom_agent.make_requests(manual_input_text)
