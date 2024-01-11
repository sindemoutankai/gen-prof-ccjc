from openai import OpenAI
import config
from dotenv import load_dotenv
import os

class Generate:
    def __init__(self, prompt, gpt_model='gpt-3.5-turbo'):
        self.client = OpenAI()
        self.prompt = prompt
        self.gpt_model = gpt_model

    def read_prompt(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.read()

    def write_response(self, output_file, response):
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(response)

    def get_response(self, prompt):
        response = self.client.chat.completions.create(
            model= self.gpt_model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        res = response.choices[0].message.content
        #print(res)
        return res

    def process_prompt_and_generate_output(self, output_file, output_folder):
#output_folderがなかったら作る
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        #prompt = self.read_prompt(self.input_file)
        response = self.get_response(self.prompt)
        self.write_response(output_file, response)


    def overide_api(self):
        load_dotenv(override=True)


