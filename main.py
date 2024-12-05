import json
from pathlib import Path
from dotenv import load_dotenv
import os

import boto3
from botocore.exceptions import ClientError

load_dotenv()

def detect_file_text() -> None:

    """
    Function used to extract the text content from an image.
    """

    # initialise Amazon Textract
    client = boto3.client("textract", region_name = "us-east-1",
                          aws_access_key_id=os.getenv("ACCESS_KEY_ID"),
                          aws_secret_access_key=os.getenv("SECRET_ACCESS_KEY"))

    # get image path
    file_path = str(Path(__file__).parent / "images" / "Lista-de-material-escolar-3-547x640.png")

    # reading file 
    with open(file_path, "rb") as image:
        document = image.read()

    # using Amazon Textract API to get the text from image

    try:
        response = client.detect_document_text(Document={'Bytes': document})
        # saving extracted text as JSON format file
        with open("response.json", "w") as json_file:
            json_file.write(json.dumps(response))
    except ClientError as ce:
        print(f"Error processing document: {ce}")

def get_lines() -> list[str]:

    """
    Returns the extracted text from a JSON file as a list of strings.
    """

    text_blocks = []

    try:
        with open("response.json", "r") as json_file:

            data = json.loads(json_file.read())
            text_blocks = data["Blocks"]
    except IOError:
        detect_file_text() # runs textract if file was not found or is empty

    return [block["Text"] for block in text_blocks if block["BlockType"] == "LINE"]

if __name__ == "__main__":
    for line in get_lines():
        print(line)