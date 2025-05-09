from groq import Groq
import os


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
        return parsed_data
    except Exception as e:
        print(f"Error parsing resume: {e}")
        return None


resume_text = """Email: emily.johnson@example.com
LinkedIn: linkedin.com/in/emilyjohnson
Skills
- Python
- Flask
- AWS
- MongoDB
Education
M.Sc. in Software Engineering, University B (2018-2022)
Projects
- Mobile App: Built a cross-platform app using React Native.
- Web Portal: Designed and implemented a user management portal.
Experience
- Backend Developer at Startup Z (2020-Present): Implemented microservices with Docker and Kubernetes."""
print(parse_resume_llm(resume_text))
