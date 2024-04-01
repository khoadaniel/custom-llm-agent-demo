from langchain_openai import ChatOpenAI
from langchain.agents import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor
import requests
import streamlit as st
from dotenv import load_dotenv


class LangChainCustomAgent():
    def __init__(self):
        load_dotenv()

    def color_text(self, text: str, color: str = "#95ed96"):
        return f"""
                    <div style="
                        border-radius: 10px;
                        padding: 10px;
                        color: black;
                        background-color: {color};
                    ">
                        {text}
                    </div>
                """

    def make_requests(self, conversation: str):
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

        @tool
        def add_orders(order_data):
            """Add items to an order by making a POST request with the order_data argument strictly following this format:
            order_data = [
            {'quantity': 2, 'item': 'apple'},
            {'quantity': 1, 'item': 'banana'},
            {'quantity': 3, 'item': 'cherry'}
                    ]
            """

            # Make a POST request to the FastAPI endpoint
            url = "http://localhost:8889/add"

            st.markdown(self.color_text(f"""🔌 Add items to the order by making a POST request to: {url}""",
                                        color="#95ed96"),
                        unsafe_allow_html=True)

            # Adhere to the expected format of the FastAPI endpoint
            request_json = {"list_items": order_data}

            response = requests.post(url,
                                     headers={
                                         "Content-Type": "application/json"},
                                     json=request_json)
            st.write(order_data)

            # Check if the request was successful
            if response.status_code == 200:
                st.markdown(f"""Request successful to . Status code: {
                            response.status_code}""")
            else:
                st.markdown(
                    f"""Failed to make request. Status code: {response.status_code}""")

        @tool
        def remove_orders(order_data):
            """Remove items from an order by making a POST request with the order_data argument strictly following this format:
            order_data = [
            {'quantity': 2, 'item': 'apple'},
            {'quantity': 1, 'item': 'banana'},
            {'quantity': 3, 'item': 'cherry'}
                    ]
            """

            # Make a POST request to the FastAPI endpoint
            url = "http://localhost:8889/remove"

            st.markdown(self.color_text(f"""🔌 Remove items from the order by making a POST request to: {url}""",
                                        color="#ffaaa8"),
                        unsafe_allow_html=True)

            # Adhere to the expected format of the FastAPI endpoint
            request_json = {"list_items": order_data}

            response = requests.post(url,
                                     headers={
                                         "Content-Type": "application/json"},
                                     json=request_json)
            st.write(order_data)

            # Check if the request was successful
            if response.status_code == 200:
                st.markdown(f"""Request successful to . Status code: {
                            response.status_code}""")
            else:
                st.markdown(
                    f"""Failed to make request. Status code: {response.status_code}""")

        @tool
        def pay_orders(payment_method: str):
            """Proceed to pay for the order by making a POST request with the payment_method argument strictly following this format:
            payment_method = 'cash' or 'card'
            """

            # Make a POST request to the FastAPI endpoint
            url = "http://localhost:8889/pay"

            st.markdown(self.color_text(f"""🔌 Proceed to payment by making a POST request to: {url}""",
                                        color="#95ed96"),
                        unsafe_allow_html=True)

            # Adhere to the expected format of the FastAPI endpoint
            request_json = {"payment_method": payment_method}

            # We can use this response for logging purposes
            response = requests.post(url,
                                     headers={
                                         "Content-Type": "application/json"},
                                     json=request_json)
            st.write(request_json)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "You are a helpful assistant, you extract user's food orders from a conversation and add or remove them to POS system by making POST request with the extracted order data.\
                 User can also request to pay with a preferred payment method.\
                    The real order information starts from a signpost word 'agent' and ends with a signpost word 'please'.\
                        The rest of the conversation is not important, you must strictly ignore it. The extracted order should contain the items and their quantity,\
                            and it is in the format of a python list of multiple dictionaries."),
                ("user",
                 "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        # Bind the tools to the LLM, the result is an LLM with tools
        tools = [add_orders, remove_orders, pay_orders]
        llm_with_tools = llm.bind_tools(tools)

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
            }
            | prompt
            | llm_with_tools
            | OpenAIToolsAgentOutputParser()
        )

        # And we need to create an agent executor, we cannot just call the agent directly
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

        agent_output = agent_executor.invoke(
            {"input": conversation}
        )

        st.markdown(self.color_text(f"""🤖 {agent_output["output"]}""",
                                    color="#fcf89d"),
                    unsafe_allow_html=True)
