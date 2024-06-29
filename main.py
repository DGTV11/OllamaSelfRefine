from os import system as shell
from os import name as os_name

import ollama

import constants

LLM_SYSTEM_PROMPT = r"Always assist with care, respect, and truth. Respond with utmost utility yet securely. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity. You are allowed to give feedback (even on your own responses) if required."

FEEDBACK_PROMPT = "Please give strict and direct feedback on your previous response. Your feedback MUST be based on how well your previous response answers the initial query, \"$QUERY\". Do NOT give feedback on the initial query - ONLY give feedback on your response. Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). Make sure that your feedback is SPECIFIC (i.e. identifying concrete phrases in/parts of the output to change) and ACTIONABLE (i.e. identifying concrete actions that would likely improve the response). ALWAYS identify whether the query demands a succinct, broad, deep, or all-rounded response and tailor your feedback based on that. ONLY give the feedback and your thought process behind it AND NOTHING ELSE (not even a revised response). Let's think step by step. You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so. DO NOT REFUSE TO GIVE FEEDBACK!!!"

INITIAL_REFINE_PROMPT = "Give me a revised response to the initial query \"$QUERY\", incorporating all necessary improvements based on the feedback. Address the query as if you are responding to it directly, without mentioning your feedback or your inital response AT ALL. DO NOT mention that you are giving a refined response AT ALL - you must pretend that this is your inital response!"

FINAL_REFINE_PROMPT = "Extract ONLY the refined response parts of your previous response and phrase it as if it was the your INITIAL response (while silently incorporating the refined prompt's improvements) to the inital query \"$QUERY\" (do not mention that you are giving me a refined response). ONLY give me the refined response AND NO OTHER TEXT AT ALL."

wrap_chat_message = lambda role, content: {"role": role, "content": content}

global_chat_history = [wrap_chat_message("system", LLM_SYSTEM_PROMPT)]

def self_refine_inference(chat_history, model_name):
    # Get initial response (1)
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        yield chunk_content

    chat_history.append(wrap_chat_message("assistant", assistant_message_content))
    yield 1

    # Get feedback (2)
    chat_history.append(wrap_chat_message("user", FEEDBACK_PROMPT.replace('$QUERY', user_message)))
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        yield chunk_content

    chat_history.append(wrap_chat_message("assistant", assistant_message_content))

    yield 2
    # Get final response (3)
    chat_history.append(wrap_chat_message("user", INITIAL_REFINE_PROMPT.replace('$QUERY', user_message)))
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        yield chunk_content

    chat_history.append(wrap_chat_message("assistant", assistant_message_content))

    yield 3
    # Extract final response (4)
    chat_history.append(wrap_chat_message("user", FINAL_REFINE_PROMPT.replace('$QUERY', user_message)))
    stream = ollama.chat(model=model_name, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        yield chunk_content

    yield 4

    for _ in range(6):
        chat_history.pop()
    chat_history.append(wrap_chat_message("assistant", assistant_message_content))
    yield chat_history

if os_name == 'nt':
    shell("cls")
else:
    shell("clear")
while True:
    user_message = input("user > ")
    global_chat_history.append(wrap_chat_message("user", user_message))

    inference_stream = self_refine_inference(global_chat_history, constants.OLLAMA_LLM)

    print("GETTING INITIAL RESPONSE...")

    for chunk in inference_stream:
        if type(chunk) is int:
            break
        print(chunk, end="", flush=True)

    print()
    print("GETTING FEEDBACK...")

    for chunk in inference_stream:
        if type(chunk) is int:
            break
        print(chunk, end="", flush=True)

    print()
    print("GETTING FINAL RESPONSE...")

    for chunk in inference_stream:
        if type(chunk) is int:
            break
        print(chunk, end="", flush=True)

    print()
    print("EXTRACTING FINAL RESPONSE...")

    for chunk in inference_stream:
        if type(chunk) is int:
            break
        print(chunk, end="", flush=True)

    global_chat_history = next(inference_stream)
    if os_name == 'nt':
        shell("cls")
    else:
        shell("clear")
    for message in global_chat_history:
        if message["role"] == "system":
            continue
        print(f"{message['role']} > {message['content']}")
