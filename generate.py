from openai import OpenAI, OpenAIError
import config
from checker import Checker
from dotenv import load_dotenv
import os
import re
from promptgenerate2 import PromptGenerate2
from xml.etree import ElementTree as ET

class Generate:
    def __init__(self, prompt, gpt_model='gpt-3.5-turbo'):
        self.client = OpenAI()
        self.checker = Checker('assets/input/ngword_list.csv')
        self.prompt = prompt
        self.gpt_model = gpt_model
        self.promptgenerate2 = PromptGenerate2("prompt2.txt")
        self.occupation_path = 'assets/input/occupation_list.csv'


    def read_prompt(self, input_file):
        with open(input_file, 'r', encoding='utf-8') as file:
            return file.read()

    def write_response(self, output_file, response):
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(response)

    def get_response(self, prompt):
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        res = response.choices[0].message.content
        is_valid_format = self.checker.xml_checker(res)
        #contains_ng_word = self.checker.detect_ng_word(res)
        if not is_valid_format:
            print("XML error")
            print(res)
            return self.get_response(prompt)

        """
        if not contains_ng_word:
            print('detect ng word')
            return self.get_response(prompt)
        """
        return res

    def get_response2(self, prompt):
        response = self.client.chat.completions.create(
            model=self.gpt_model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}]
        )
        res = response.choices[0].message.content
        is_valid_format2 = self.checker.xml_checker2(res)
        contains_ng_word2 = self.checker.detect_ng_word(res)
        if not is_valid_format2:
            print("XML error")
            print(res)
            return self.get_response2(prompt)
        if not contains_ng_word2:
            print('detect ng word')
            return self.get_response2(prompt)
        return res

    def extract_personality(self, text):
        match = re.search(r"<personality>(.*?)</personality>", text, re.DOTALL)
        if match:
            return match.group(1)
        else:
            return "No personality tag found"



    def process_prompt_and_generate_output(self, output_file, output_folder):
#output_folderがなかったら作る
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        #prompt = self.read_prompt(self.input_file)

        response = self.get_response(self.prompt)
        personality = self.extract_personality(response)
        occupation = self.promptgenerate2.get_oneword(self.occupation_path)
        final_prompt = self.promptgenerate2.gen_final_prompt(personality, occupation)
        response2 = self.get_response2(final_prompt)
        #merge two response
        merge_response = self.merge_response(response, response2, occupation)

        self.write_response(output_file, merge_response)

    def merge_response(self,response1, response2, occupation):
        root1 = ET.fromstring(response1)
        root2 = ET.fromstring(response2)

        # root2の要素をroot1に追加する
        for element in list(root2):
            root1.append(element)

        # 両方のXMLから<occupation>タグを削除
        for elem in root1.findall('occupation'):
            root1.remove(elem)

        # 新しい<occupation>タグを追加
        occupation_elem = ET.Element('occupation')
        occupation_elem.text = occupation
        root1.insert(5, occupation_elem)  # <occupation>を2番目の要素として挿入

        # 更新されたXMLを文字列として取得
        combined_xml = ET.tostring(root1, encoding='unicode')

        combined_xml_str = '\n'.join([line.strip() for line in combined_xml.splitlines()])
        return combined_xml_str

    """
        #二つのレスポンスをまーじ
        def merge_response(self, response1, response2, occupation):
            root1 = ET.fromstring(response1)
            root2 = ET.fromstring(response2)

            # root2の要素をroot1に追加する
            for element in root2:
                root1.append(element)

            # 更新されたXMLを文字列として取得
            combined_xml = ET.tostring(root1, encoding='unicode')

            combined_xml_str = '\n'.join([line.strip() for line in combined_xml.splitlines()])
            #print(combined_xml_str)

            return combined_xml_str
    """


    def overide_api(self):
        load_dotenv(override=True)


