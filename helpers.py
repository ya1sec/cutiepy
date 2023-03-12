import os
import platform
import openai
import sys
import subprocess
import dotenv 
import distro

def get_os_friendly_name():
  # Get OS Name
  os_name = platform.system()
  
  if os_name == "Linux":
      return "Linux/"+distro.name(pretty=True)
  elif os_name == "Windows":
      return os_name
  elif os_name == "Darwin":
     return "Darwin/macOS"

# Construct the prompt
def get_full_prompt(user_prompt, shell):

  ## Find the executing directory (e.g. in case an alias is set)
  ## So we can find the prompt.txt file
  yolo_path = os.path.abspath(__file__)
  prompt_path = os.path.dirname(yolo_path)

  ## Load the prompt and prep it
  prompt_file = os.path.join(prompt_path, "/prompts/prompt.txt")
  pre_prompt = open(prompt_file,"r").read()
  pre_prompt = pre_prompt.replace("{shell}", shell)
  pre_prompt = pre_prompt.replace("{os}", get_os_friendly_name())
  prompt = pre_prompt + user_prompt
  
  # be nice and make it a question
  if prompt[-1:] != "?" and prompt[-1:] != ".":
    prompt+="?"

  return prompt