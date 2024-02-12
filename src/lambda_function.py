import base64
import io
import json
import os

from openai import OpenAI
from streaming_form_data import StreamingFormDataParser
from streaming_form_data.targets import ValueTarget


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def transcribe_audio(file_name, audio_data):
    with io.BytesIO(audio_data) as audio_file:
        audio_file.name = file_name.lower()
        print(f'Starting request to OpenAI: audio_file.name={audio_file.name}')
        transcript = client.audio.transcriptions.create(model='whisper-1', file=audio_file)
        print(f'Finished request to OpenAI: text={transcript.text}')
        return transcript.text


def lambda_handler(event, context):
    try:
        if 'body' in event:
            parser = StreamingFormDataParser(headers=event['headers'])
            audio_data = ValueTarget()
            parser.register("audio", audio_data)
            parser.data_received(base64.b64decode(event["body"]))
            text = transcribe_audio(audio_data.multipart_filename, audio_data.value)
            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "text": text
            }
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "text": "No audio!"
        }
    except ValueError as ve:
        import traceback
        print(traceback.format_exc())
        print(f"ValueError: {str(ve)}")
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": str(ve)}),
        }
        return response
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(f"Error: {str(e)}")
        response = {
            "statusCode": 500,
            "body": json.dumps({"message": f"An error occurred while processing the request. {str(e)}"}),
        }
        return response
        