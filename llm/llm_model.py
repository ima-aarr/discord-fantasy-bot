from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

MODEL_NAME = "TheBloke/MPT-7B-Instruct-v0.1"  # CPU版軽量モデル
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, device_map="cpu")

def generate_text(prompt, max_length=200):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_length=max_length)
    return tokenizer.decode(output[0], skip_special_tokens=True)
