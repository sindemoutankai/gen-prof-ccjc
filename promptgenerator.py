import csv

class PromptGenerator:
    def __init__(self, csv_file, prompt_file, output_folder):
        self.csv_file = csv_file
        self.prompt_file = prompt_file
        self.output_folder = output_folder

    def read_prompt(self):
        with open(self.prompt_file, 'r', encoding='utf-8') as file:
            return file.read()

    def generate_prompt_files(self):
        template = self.read_prompt()
        with open(self.csv_file, 'r', encoding= "cp932") as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                score = row[2:]
                print(score)
                new_prompt = template.format(*score)
                file_name = f'{self.output_folder}/{row[0]}_{row[1]}_prompt.txt'
                with open(file_name, 'w', encoding= "cp932") as outfile:

                    outfile.write(new_prompt)

generator = PromptGenerator('assets/personality_list.csv', 'prompt.txt', 'assets')
generator.generate_prompt_files()
