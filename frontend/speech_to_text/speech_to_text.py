import speech_recognition as sr
import pyttsx3
import streamlit as st

# Initialize the recognizer
r = sr.Recognizer()


def speech_to_text():
    done = False
    while not done:
        try:
            # Use the microphone as source for input.
            with sr.Microphone() as source:

                # Recognize the ambient noise to improve accuracy
                r.adjust_for_ambient_noise(source, duration=0.2)

                print("Please start speaking.")
                # Listens for the user's input and automatically recognizes when user starts and stops speaking
                audio = r.listen(source)
                print("Converting Speech to Text...")

                converted_text = r.recognize_google(audio)
                converted_text = converted_text.lower()

                colored_box_html = f"""
                <div style="
                    border-radius: 10px;
                    padding: 10px;
                    color: white;
                    background-color: #0C0C0C;
                ">
                    👦🏻 {converted_text}
                </div>
                """

                st.markdown(colored_box_html, unsafe_allow_html=True)

                done = True

        except Exception as e:
            st.markdown(
                """Sorry, I cannot understand, please try again.\n{e}""")

    return converted_text
