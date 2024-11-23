from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager
from langchain_community.llms import Ollama
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import PromptTemplate
from typing import Dict, Optional
import json


# The function get_data goes into the folder personnal_info and get the .txt file my_info.txt and return the content of the file
def get_data():
    with open("personnal_info/my_info.txt") as f:
        return f.read()


def load_llama3() -> Ollama:
    """
    Load the LLAMA3 model from OLLAMA.
    """

    ollama_client = Ollama(base_url="http://localhost:11434", model="llama3")

    system_message = """
        You are an expert AI data extraction assistant specialized in processing text-based information. 
        Your primary objective is to accurately analyze input text and extract structured information.

        Key Guidelines:
        - Extract information precisely from the given text
        - Be concise and accurate
        - Use null for missing information
        - Ensure output is valid, parseable JSON
        - Do not invent or assume information not present in the text"""

    SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=[],  # No input variables for the system message
            template=system_message,
        )
    )
    HumanMessagePromptTemplate(
        prompt=PromptTemplate(input_variables=["input"], template="{input}")
    )

    return ollama_client


def generate_answer_ollama(
    input_text: str,
    dict: Dict[str, Optional[str]],
) -> str:
    """
    Generate a summary for a given text using the OLLAMA model.
    """

    ollama_model = load_llama3()

    aux_prompt = ""
    for key, value in dict.items():
        aux_prompt += f'"{key}": <extracted {key} or null>,'
    prompt = f"""
    Task: Extract information from the following text and format the response EXACTLY as specified.

    Input: {input_text}

    STRICT OUTPUT REQUIREMENTS:
    1. You MUST respond ONLY in the following JSON format:
    {{{aux_prompt}}}

    CRITICAL INSTRUCTIONS:
    - If ANY information is missing, use null
    - Do NOT add ANY additional text or explanation
    - The output MUST be a valid JSON that can be parsed directly
    - Be precise in extraction
    - Only use information explicitly mentioned in the text

    EXAMPLE FORMAT:
    {{{aux_prompt}}}

    Respond ONLY with the JSON, exactly matching this structure."""

    response = ollama_model(prompt)

    return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: You can add initialization code here
    logger.info("Starting the application")

    yield  # Here the FastAPI application runs

    # Shutdown: You can add cleanup code here if needed
    print("Shutting down the application")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health_check():
    return {"status": "ok"}


@app.post("/form")
def form(
    user_info: str, json_data: Dict[str, Optional[str]]
) -> Dict[str, Optional[str]]:
    logger.info(user_info)

    dict = {}

    for input_field in json_data:
        if input_field.get("type") == "text" or input_field.get("type") == "textarea":
            dict[input_field.get("name")] = input_field.get("value")

    response = generate_answer_ollama(user_info, dict)
    logger.info(response)
    logger.info(type(response))

    json_response = json.loads(response)
    logger.info(json_response)

    return json_response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
