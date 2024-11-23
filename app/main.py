from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager
from langchain_ollama import OllamaLLM
from typing import Dict, Optional
import json

from pydantic import BaseModel


class FormRequest(BaseModel):
    """
    Pydantic model to define the structure of the request body.
    """

    user_info: str
    json_data: Dict[str, Optional[str]]


# The function get_data goes into the folder personnal_info and get the .txt file my_info.txt and return the content of the file
def get_data():
    with open("personnal_info/my_info.txt") as f:
        return f.read()


def load_model() -> OllamaLLM:
    """
    Load the LLAMA3 model from OLLAMA.
    """

    ollama_client = OllamaLLM(
        base_url="http://ollama:11434", model="llama3.2:1b", format="json"
    )

    return ollama_client


def generate_answer_ollama(
    input_text: str,
    input_dict: Dict[str, Optional[str]],
) -> str:
    """
    Generate a summary for a given text using the OLLAMA model.
    """

    ollama_model = load_model()
    resp = ollama_model.invoke("How are you")
    logger.info(resp)

    values_dict = "\n".join({f'    "{key}": "<value>"' for key in input_dict})

    prompt = f"""You are a system specialized in processing and structuring text-based data. Your task is to analyze the provided text and extract relevant information into a structured format suitable for automated form-filling. Follow the schema provided below and ensure the output is valid JSON:

Schema:
JSON
{{
{values_dict}
}}

Replace <value> with the corresponding information from the text. If any field is not present in the input text, use null or leave it empty please.


Input Text/Document:
{input_text}
"""

    logger.info(prompt)
    resp = ollama_model.invoke(prompt)
    logger.info(resp)
    return resp


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
    form_request: FormRequest,
) -> Dict[str, Optional[str]]:
    user_info = form_request.user_info
    json_data = form_request.json_data
    logger.info(user_info)
    logger.info(json_data)

    response = generate_answer_ollama(user_info, json_data)
    logger.info(response)
    logger.info(type(response))

    json_response = json.loads(response)
    logger.info(json_response)

    return json_response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
