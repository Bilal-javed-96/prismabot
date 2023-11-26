import os
from openai import OpenAI
import streamlit as st
import time
from dotenv import load_dotenv

load_dotenv()

# Initialize Streamlit app
st.set_page_config(page_title="PrismaDocsBot", page_icon="💡")
st.title("💡 Prisma Docs Bot")

# Initialize OpenAI client
client = OpenAI()

@st.cache_resource
def create_prisma_cloud_assistant():
    try:
        OpenAI.api_key = os.getenv('OPENAI_API_KEY')

        # Retrieve an existing Assistant
        my_assistant = client.beta.assistants.retrieve(assistant_id='asst_g5RCLyfQi5o6mHqbdiUrHse8')
        st.success(f"Assistant retrieved: {my_assistant.name}")

        # Step 1: Create an Assistant
        # my_assistant = client.beta.assistants.create(
        #     model="gpt-4-1106-preview",
        #     instructions="You are a helpful Prisma Cloud Consultant. You have been provided with the prisma cloud docs as a knowledgebase inside the retrieval tool. Always use that to get the most authentic and up-to-date information for it.",
        #     name="Prisma Cloud Consultant",
        #     tools=[{"type": "code_interpreter"}, {"type":"retrieval"}],
        #     file_ids=['file-1l4rQB1l1AiSizuZzvjOfBj6']
        # )

        # st.write(f"Assistant created: {my_assistant}\n")

        return my_assistant

    except Exception as e:
        st.error(f"Error creating assistant: {e}")
        raise

def create_thread():
    try:
        # Step 2: Create a Thread
        my_thread = client.beta.threads.create()
        # st.write(f"Thread created: {my_thread}\n")

        return my_thread

    except Exception as e:
        st.error(f"Error creating thread: {e}")
        raise

def add_user_message_to_thread(thread_id, content):
    try:
        # Step 3: Add a Message to a Thread
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content,
        )
        # st.write(f"User message added to thread: {my_thread_message}\n")

        return my_thread_message

    except Exception as e:
        # st.error(f"Error adding user message to thread: {e}")
        raise

def run_assistant(thread_id, assistant_id, user_question):
    try:
        # Step 4: Run the Assistant
        my_run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            # instructions=f"Please address the user as Rok Benko. User question: {user_question}"
        )
        # st.write(f"Assistant run started: {my_run}\n")

        return my_run

    except Exception as e:
        st.error(f"Error running assistant: {e}")
        raise

def retrieve_run_status(thread_id, run_id):
    try:
        # Step 5: Periodically retrieve the Run to check on its status to see if it has moved to completed
        while True:
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )
            # st.write(f"Run status: {keep_retrieving_run.status}")

            if keep_retrieving_run.status == "completed":
                st.write("\n")
                break
            time.sleep(1)

    except Exception as e:
        st.error(f"Error retrieving run status: {e}")
        raise

def retrieve_messages(thread_id):
    try:
        # Step 6: Retrieve the Messages added by the Assistant to the Thread
        all_messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )

        st.write("------------------------------------------------------------\n")

        st.markdown(f"User: {all_messages.data[-1].content[0].text.value}")
        st.markdown(f"Assistant: {all_messages.data[-2].content[0].text.value}")

    except Exception as e:
        st.error(f"Error retrieving messages: {e}")
        raise

if __name__ == "__main__":
    try:
        my_assistant = create_prisma_cloud_assistant()
        my_thread = create_thread()

        # Get user question
        user_question = st.text_input("Ask a question to the Prisma Docs Bot:")

        if st.button("Ask") and user_question:
            my_thread_message = add_user_message_to_thread(my_thread.id, user_question)
            my_run = run_assistant(my_thread.id, my_assistant.id, user_question)
            retrieve_run_status(my_thread.id, my_run.id)
            retrieve_messages(my_thread.id)

    except Exception as e:
        st.error(f"Error: {e}")