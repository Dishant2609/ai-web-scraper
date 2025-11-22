from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)



template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. Extract Information: Only extract the information that directly matches the provided description: {parse_description}. "
    "2. No Extra Content: Do not include any additional text, comments, or explanations in your response. "
    "3. Empty Response: If no information matches the description, return an empty string ('')."
    "4. Direct Data Only: Your output should contain only the data that is explicitly requested, with no other text."
)


model = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)



def parse_with_openai(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_result = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_result.append(response.content)

    return "\n".join(parsed_result)
