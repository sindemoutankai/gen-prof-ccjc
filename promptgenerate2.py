import unicodecsv
import pandas as pd
import os

class PromptGenerate2:
    def __init__(self, prompt_file2):
        self.prompt_file2 = prompt_file2
        #self.number_of_gen = int(os.getenv("NUMBER_OF_GEN", 200))

        #それぞれの性格タイプのファイルを先に作っておく。
        #self.generate_prompt_files()

#promptの読み込み
    def read_prompt(self):
        with open(self.prompt_file, 'r') as file:
            return file.read()

#ビックファイブチャートの読み込み
    def read_bigfive(self):
        f = open(self.csv_file, 'rb')
        reader = unicodecsv.reader(f,encoding='shift-jis')
        return f, reader

#ハッシュタグと出身地のcsvから一つとる用
    def get_oneword(self, file_path):
        tag_df = pd.read_csv(file_path, encoding="shift_jis")
        sample_hash = tag_df.sample(1)
        word = sample_hash.iloc[0,0]
        return(word)

#指定したindexのビックファイブチャートを読み込んで、埋める。同時に、IDを返す。
    def fill_bigfive(self, p_type):
        with open(self.prompt_file, 'r') as file:
            df = pd.read_csv(self.csv_file, encoding="shift_jis", header=None)
            df = df.reset_index(drop=True)
            row = df.loc[p_type, :]
            template = file.read()
            score = row[2:8]
            _type = row[0]
            type_id = row[1]
            new_prompt = template.format(*score)
            #print(new_prompt)
            return new_prompt, _type, type_id

    def gen_full_prompt(self, _id):
        hashtag = self.get_oneword(self.hashtag_files)
        hometown = self.get_oneword(self.hometown_files)
        new_prompt, _type, type_id = self.fill_bigfive(_id)
        full_prompt = new_prompt.replace("△△", hometown)
        #print(full_prompt)
        return full_prompt, _type, type_id

    def gen_final_prompt(self, personality, occupation):
        with open(self.prompt_file2, 'r') as file:
            template = file.read()
            final_prompt = template.replace("〇〇",personality).replace("XX", occupation)
            return final_prompt

