import unicodecsv
import pandas as pd
import os

class PromptGenerate:
    def __init__(self, csv_file, prompt_file, hashtag_files, hometown_files):
        self.csv_file = csv_file
        self.prompt_file = prompt_file
        self.hashtag_files = hashtag_files
        self.hometown_files = hometown_files
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
        full_prompt = new_prompt.replace("〇〇", hashtag).replace("△△", hometown)
        #print(full_prompt)
        return full_prompt, _type, type_id


    #def generate_full_prompt(self, prompt_path):

"""
    #promptの空白に、ビックファイブチャートの結果を入れてファイルに読み込む
    def generate_prompt_files(self):
        template = self.read_prompt()
        f, reader = self.read_bigfive()
        for i, row in enumerate(reader):
            score = row[2:]
            new_prompt = template.format(*score)
            file_name = f'{self.output_folder}/{row[0]}_{row[1]}_prompt.txt'
            print(new_prompt)
            #ファイルに書き込む
            with open(file_name, 'w') as outfile:
                outfile.write(new_prompt)
        f.close()
#ビックファイブチャートを入れたプロンプトに、ハッシュタグと出身を入れる
    """




