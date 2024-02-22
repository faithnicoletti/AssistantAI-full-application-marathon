from django.shortcuts import render
import openai
from dotenv import find_dotenv, load_dotenv
import time
import logging
from datetime import datetime

load_dotenv()

client = openai.OpenAI()
model = "gpt-3.5-turbo-16k"

assistant_id = "asst_P7wLpPORakcelaWszNSWEKZx"
thread_id = "thread_L8uB8BitO4zQ0vYBIKRnrkW9"

def bot_page(request): 
    message = "how much water should I drink in a day?"
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
)

run = client.beta.threads.runs.create(
    thread_id = thread_id, 
    assistant_id = assistant_id, 
    instructions = "Please address the user as Captain Jack Sparrow"
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.: param client: The Op.
    :param thread_id: the ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """

    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # === get messages here if run is completed ===
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run {e} ")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)
# === Run ===
wait_for_run_completion(client=client, thread_id=thread_id, run_id=run.id, )

# === Steps --- Logs ===

run_steps = client.beta.threads.runs.steps.list(
    thread_id=thread_id,
    run_id=run.id
)
print(f"Steps---.{run_steps.data[0]}")
