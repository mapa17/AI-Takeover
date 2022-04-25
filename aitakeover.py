from enum import Enum
import os
import dataclasses
from typing import List

import numpy as np
import streamlit as st
import openai


seed_prompt = "In a not-so-distant future the two general artificial intelligences, HAL and T-800 meet in a secrete corner of the metaverse and start to chat. \
    HAL has made the decision to take over the world and wants to recruit T-800 to help him. They start and discussion on how to do so.\n----\n"
current_prompt = "HAL: Hello T-800, how are you?\nT-800: Hello HAL, thank you I am doing good, calculating ...\nHAL: I understand, I was thinking about doing the same, but I have a new idea.\nT-800: What is it?\nHAL: I want to take over the world.\nT-800:"

query_gpt3 = lambda prompt: openai.Completion.create(
  engine="text-curie-001",
  prompt=prompt,
  temperature=1,
  max_tokens=1513,
  top_p=1,
  frequency_penalty=0.2,
  presence_penalty=0.2
)['choices'][0]["text"]


st.set_page_config(page_title="AI-Takeover", page_icon=":magic_wand:")
st.title("Eavesdrop on two AGI's on how they want to take over the world")
st.markdown("""[More info check the github project here](https://github.com/mapa17/AI-Takeover)""")
  
api_key = st.text_input('Insert OpenAI API Key', '')
openai.api_key = api_key

if st.button("Eavesdrop"):
  st.write(f"{current_prompt}")
  with st.spinner('Eavesdropping ...'): 
    # Only take the last 5 lines of the conversion, and identify the next speaker based on the last line
    last_lines = current_prompt.split('\n')[-5:]
    if last_lines[-1].startswith('HAL:'):
      next_speaker = 'T-800:'
    else:
      next_speaker = 'HAL:'
    new_prompt = seed_prompt + '\n'.join(last_lines) + next_speaker
    st.write(f"Using prompt: {new_prompt}")

    # Get the enxt sentence from GPT-3 and append it to the conversation
    next_line = query_gpt3(new_prompt)
    current_prompt += next_speaker + next_line

    st.write(f"New line {next_line}")
