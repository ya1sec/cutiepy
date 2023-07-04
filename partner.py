import os
import sys
import openai
import platform
import subprocess
import distro

from termcolor import colored
from colorama import init
from dotenv import load_dotenv

art = """
                    _____
                ___/     \___
               `-._)     (_,-`
                   \O _ O/
                    \ - /
                     `-(
                      ||
                     _||_
                    |-..-|
                    |/. \|
                    |\__/|
                  ._|//\\|_,
                  `-((  ))-'
                   __\\//__ gnv
                   >_ /\ _<,
                     '  '
"""

print(colored(art, "yellow"))

cur_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv()


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

SAFETY_SWITCH = True


class CutiePy:
    def __init__(self, arguments):
        self.safety_switch = True

        self.model = "gpt-3.5-turbo"
        self.openai_api_key = OPENAI_API_KEY

        self.shell = self.get_shell()
        self.os = self.get_os()

        self.user_prompt = self.get_user_prompt(arguments)

        full_prompt = self.get_full_prompt(self.user_prompt)
        self.system_prompt = full_prompt[1]
        self.prompt = full_prompt
        # self.response = self.get_response()
        # self.reply = self.get_reply()

    def get_shell(self):
        shell = os.environ.get("SHELL")
        if shell is None:
            shell = "unknown"
        return shell

    def get_os(self):
        os_name = platform.system()
        if os_name == "Linux":
            return "Linux/" + distro.name(pretty=True)
        elif os_name == "Windows":
            return os_name
        elif os_name == "Darwin":
            return "Darwin/macOS"

    def get_user_prompt(self, arguments):
        user_prompt = " ".join(arguments)
        # return " ".join(sys.argv[1:])
        return user_prompt

    # Construct the prompt
    def get_full_prompt(self, user_prompt, explain=False):
        ## Find the executing directory (e.g. in case an alias is set)
        ## So we can find the prompt.txt file
        yolo_path = os.path.abspath(__file__)
        prompt_path = os.path.dirname(yolo_path)

        prompt_file = os.path.join(prompt_path, "prompts/partner.txt")

        pre_prompt = open(prompt_file, "r").read()
        pre_prompt = pre_prompt.replace("{shell}", self.shell)
        pre_prompt = pre_prompt.replace("{os}", self.os)
        prompt = pre_prompt + user_prompt

        # be nice and make it a question
        if prompt[-1:] != "?" and prompt[-1:] != ".":
            prompt += "?"

        # return prompt
        return pre_prompt

    def get_response(self):
        openai.api_key = self.openai_api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.prompt},
            ],
            temperature=0,
            max_tokens=500,
        )
        print(self.system_prompt)
        print(self.prompt)
        return response

    def get_cmd(self):
        response = self.get_response()
        # reply = response["choices"][0]["message"]["content"]
        cmd = response.choices[0].message.content.strip()
        return cmd
