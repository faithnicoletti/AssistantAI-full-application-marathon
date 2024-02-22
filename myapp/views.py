from django.shortcuts import render
import openai
form dotenv import find_dotenv, load_dotenv

load_dotenv()

client = openai.OpenAI()

