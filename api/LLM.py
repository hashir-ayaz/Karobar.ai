from groq import Groq
import os
import json


def get_user_query_prompt():
    # this prompt will be used when the user submits a query
    """
    Returns a prompt for user query parsing.
    """
    return (
        "You are a resume parser. Your task is to extract relevant information "
        "from user queries. The output should be a JSON object containing the "
        "following fields: skills. Ensure that each "
        "field contains the most accurate and complete information based on the user query."
        "Example: required_skills = ['Python', 'Flask', 'AWS', 'MongoDB']"
    )


def get_resume_parsing_prompt():
    """
    Returns a prompt for resume parsing.
    """
    return (
        "You are a resume parser. Your task is to extract relevant information "
        "from resumes. The output should be a JSON object containing the following "
        "fields: name, email, education, skills, and experience. Ensure that each "
        "field contains the most accurate and complete information based on the resume."
    )


client = Groq(
    api_key="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",
)


def groq_completion():
    chat_completion = client.chat.completions.create(
        messages=[
            # Set an optional system message. This sets the behavior of the
            # assistant and can be used to provide specific instructions for
            # how it should behave throughout the conversation.
            {"role": "system", "content": "You are a helpful assistant."},
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            },
        ],
        # The language model which will generate the completion.
        model="llama-3.3-70b-versatile",
    )

    # Print the completion returned by the LLM.
    print(chat_completion.choices[0].message.content)


def parse_resume_llm(text):
    """
    Parses the resume text using a language model and returns structured data.
    """
    try:
        prompt = get_resume_parsing_prompt()
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"{prompt}\n\n{text}"},
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        parsed_data = response.choices[0].message.content
        return json.loads(parsed_data)
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return None


def parse_user_query(text):
    """
    Parses the user query using a language model and returns structured data.
    """
    try:
        print(f"Parsing user query: {text}")
        prompt = get_user_query_prompt()
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"{prompt}\n\n{text}"},
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"},
            temperature=0.0,
        )
        parsed_data = response.choices[0].message.content
        print(f"Parsed data: {parsed_data}")
        return json.loads(parsed_data)
    except Exception as e:
        print(f"Error parsing user query: {e}")
        return None


# user_query = (
#     "I am looking for a software engineer with experience in Python, Flask, and AWS."
# )
# parsed_query = parse_user_query(user_query)
# print(parsed_query)
