# from transformers import pipeline
import json
import ollama
import logging

# Load Llama-3.2-1B-Instruct (ensure it's correctly installed and available)
# llama_model = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")

# Function to analyze transcript
def analyze_call(transcript):
    prompt = '''<s>[INST] <<SYS>> You are an AI analyzing a call transcript to prevent Scams.
    Your task is to determine if it was an attempt to OTP scam , Credit Card, Scam remote access softwares.
    
    Output answer in JSON using the following format: {"is_suspicious": true/false, "confidence_percentage": 00, "Reasoning": explanation}
    <</SYS>>
    is this transcript suspicious? [/INST]
    {"is_suspicious": False, "confidence_percentage": 80, "Reasoning": "There was no mention of anything suspicious"}
    </s>
    <s>[INST]  
    is this transcript suspicious?:\n'''+transcript+'''\n[/INST]'''
    
    # response = llama_model(prompt, temperature=0.7)
    # result = response[0]["generated_text"].split("\n[/INST]")[-1].strip()
    response = ollama.chat(model='deepseek-r1:1.5b', messages=[
      {
        'role': 'user',
        'content': prompt,
      },
    ])
    try:
        result=response['message']['content']
        jsonStart=result.find("{")
        jsonEnd=result.find("}")
        jsonres=result[jsonStart:jsonEnd+1]
        jsonRes=json.loads(jsonres)
        print(result)

        is_sus=jsonRes["is_suspicious"]
        if (jsonRes["confidence_percentage"]<=75):is_sus=False
        return is_sus, jsonRes["Reasoning"]
    except:
        logging.error("Invalid Response")
        print("Invalid Response")
        return False,"Error"
        