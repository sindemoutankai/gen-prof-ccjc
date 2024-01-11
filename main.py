import config
from generate import Generate
from promptgenerate import PromptGenerate
import random
import os
from tqdm import tqdm

def main():
    api_key = config.OPENAI_API_KEY
#set up
    number_of_gen = int(os.getenv("NUMBER_OF_GEN", 200))
    prompt_file = 'prompt.txt'
    personality_list = 'assets/input/personality_list.csv'
    hobbies_list = 'assets/input/hobbies_list.csv'
    hometown_list =  'assets/input/hometown_list.csv'

    #prompt用インスタンス
    generator = PromptGenerate(personality_list, prompt_file, hobbies_list, hometown_list)

    #回数分の飛び出しリストを作る
    numbers = list(range(0, 25))
    repeat_count = number_of_gen // len(numbers)
    remainder = number_of_gen % len(numbers)
    numbers *= repeat_count
    numbers += random.sample(numbers, remainder)
    numbers.sort()

# iteration
    for i, idx in tqdm(enumerate(numbers), total=len(numbers)):
        prompt, _type, type_id = generator.gen_full_prompt(idx)
        chat_gpt = Generate(prompt, gpt_model='gpt-3.5-turbo')
#
        if 0 <= idx <= 4:
            output_folder = "output/A_output"
        elif 5 <= idx <= 10:
            output_folder = "output/B_output"
        elif 11 <= idx <= 15:
            output_folder = "output/C_output"
        elif 16 <= idx <= 20:
            output_folder = "output/D_output"
        elif 21 <= idx <= 24:
            output_folder = "output/E_output"

        output_file_path = f"{output_folder}/{_type}_{type_id:02d}_{i+1:04d}.xml"
        chat_gpt.process_prompt_and_generate_output(output_file_path,output_folder)

if __name__ == "__main__":
    main()