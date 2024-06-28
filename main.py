from os import system as shell

import ollama

import constants

LLM_SYSTEM_PROMPT = r"Always assist with care, respect, and truth. Respond with utmost utility yet securely. Avoid harmful, unethical, prejudiced, or negative content. Ensure replies promote fairness and positivity."

FEEDBACK_PROMPT = r"Please give strict and direct feedback on your previous response. Your feedback MUST be based on how well your previous response answers the original query. Do NOT give entirely positive feedback - you MUST find AS MANY things that CAN AND MUST be improved as possible (e.g. phrasing, content, factuality). Make sure that your feedback is SPECIFIC (i.e. identifying concrete phrases in/parts of the output to change) and ACTIONABLE (i.e. identifying concrete actions that would likely improve the response). ALWAYS identify whether the query demands a succinct, broad, deep, or all-rounded response and tailor your feedback based on that. ONLY give the feedback and your thought process behind it AND NOTHING ELSE (not even a revised response). Let's think step by step. You are capable of giving strict and direct feedback that is specific and actionable, and therefore MUST do so."

INITIAL_REFINE_PROMPT = "Give me a revised response to the initial query \"$QUERY\", incorporating all necessary improvements based on the feedback. Address the query as if you are responding to it for the first time, without mentioning your feedback or your inital response AT ALL. DO NOT mention that you are giving a refined response AT ALL - you must pretend that this is your inital response!"

FINAL_REFINE_PROMPT = "Repeat ONLY the refined response part of your previous response and phrase it as if it was the ONLY response to the inital query \"$QUERY\". ONLY give me the refined response AND NOTHING ELSE (NO EXTRA TEXT!!!)."

wrap_chat_message = lambda role, content: {"role": role, "content": content}

chat_history = [wrap_chat_message("system", LLM_SYSTEM_PROMPT)]

shell("clear")
while True:
    user_message = input("user > ")
    chat_history.append(wrap_chat_message("user", user_message))

    print("GETTING INITIAL RESPONSE...")
    stream = ollama.chat(model=constants.OLLAMA_LLM, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        print(chunk_content, end="", flush=True)
    chat_history.append(wrap_chat_message("assistant", assistant_message_content))

    print()
    print("GETTING FEEDBACK...")
    chat_history.append(wrap_chat_message("user", FEEDBACK_PROMPT))
    stream = ollama.chat(model=constants.OLLAMA_LLM, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        print(chunk_content, end="", flush=True)
    chat_history.append(wrap_chat_message("assistant", assistant_message_content))

    print()
    print("GETTING FINAL RESPONSE...")
    chat_history.append(wrap_chat_message("user", INITIAL_REFINE_PROMPT.replace('$QUERY', user_message)))
    stream = ollama.chat(model=constants.OLLAMA_LLM, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        print(chunk_content, end="", flush=True)
    chat_history.append(wrap_chat_message("assistant", assistant_message_content))

    print()
    print("EXTRACTING FINAL RESPONSE...")
    chat_history.append(wrap_chat_message("user", FINAL_REFINE_PROMPT.replace('$QUERY', user_message)))
    stream = ollama.chat(model=constants.OLLAMA_LLM, messages=chat_history, stream=True)

    assistant_message_content = ""
    for chunk in stream:
        chunk_content = chunk["message"]["content"]
        assistant_message_content += chunk_content
        print(chunk_content, end="", flush=True)

    for _ in range(6):
        chat_history.pop()
    chat_history.append(wrap_chat_message("assistant", assistant_message_content))

    shell("clear")
    for message in chat_history:
        if message["role"] == "system":
            continue
        print(f"{message['role']}> {message['content']}")
