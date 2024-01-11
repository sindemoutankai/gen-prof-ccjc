import config
from generate import Generate

api_key = config.OPENAI_API_KEY
print(api_key)

input_file = 'prompt.txt'
chat_gpt = Generate(input_file)
chat_gpt.process_prompt_and_generate_output('output/res1.xml')



