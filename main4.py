import config
from generate import Generate
from promptgenerate import PromptGenerate
import random
import os
from tqdm import tqdm
from multiprocessing import Pool, Lock
import json
import time

# global_lockの初期化
global_lock = None

# Lockの初期化関数
def init_lock(lock):
    global global_lock
    global_lock = lock

# 出力プロセスの関数
def process_output(id, idx, generator):
    global global_lock
    try:
        prompt, _type, type_id = generator.gen_full_prompt(idx)
        chat_gpt = Generate(prompt, gpt_model='gpt-3.5-turbo')
        output_folder = f"output/{_type}_output"
        output_file_path = f"{output_folder}/{_type}_{type_id:02d}_{id:07d}.xml"

        if not os.path.exists(output_file_path):
            chat_gpt.process_prompt_and_generate_output(output_file_path, output_folder)

        # チェックポイントの更新
        with global_lock:
            with open('checkpoint.json', 'r+') as f:
                checkpoints = json.load(f)
                checkpoint_key = f'{str(idx)}_{str(id)}'
                checkpoints['checkpoint'][checkpoint_key] = True
                f.seek(0)
                f.truncate()
                json.dump(checkpoints, f)

    except Exception as e:
        print('gen')
        print(f"An error occurred: {e}")

# main3関数の定義
def main3(retry_count=0, max_retries=5):
    start_time = time.time()
    try:
        global iteration_numbers
        start_time = time.time()
        api_key = config.OPENAI_API_KEY
        # set up
        number_of_gen = int(os.getenv("NUMBER_OF_GEN", 15000))
        prompt_file = 'prompt.txt'
        personality_list = 'assets/input/personality_list.csv'
        hobbies_list = 'assets/input/hobbies_list.csv'
        hometown_list = 'assets/input/hometown_list.csv'
        ng_list = 'assets/input/ngword_list'

        # prompt用インスタンス
        generator = PromptGenerate(personality_list, prompt_file, hobbies_list, hometown_list)

        # 回数分のよび出しリストを作る
        numbers = list(range(0, 25))
        iteration_numbers = list(range(1, number_of_gen + 1))
        repeat_count = number_of_gen // len(numbers)
        remainder = number_of_gen % len(numbers)
        numbers *= repeat_count
        numbers += random.sample(numbers, remainder)
        numbers.sort()
        # checkpoint用のタイプIDとIDのキー
        checkpoint_key = [f"{n}_{i}" for n, i in zip(numbers, iteration_numbers)]

        if os.path.exists('checkpoint.json'):
            with open('checkpoint.json', 'r') as f:
                checkpoints = json.load(f)
        else:
            with open('checkpoint.json', 'w') as f:
                checkpoint_dic = {'checkpoint': {str(key): False for key in checkpoint_key}}
                json.dump(checkpoint_dic, f)

        # 未完のpointのみのよび出しリストを作成する
        numbers = []
        iteration_numbers = []

        for item in checkpoints.get('checkpoint'):
            first, second = item.split('_')
            numbers.append(int(first))
            iteration_numbers.append(int(second))
        # print(_totaliteration)
        # print(iteration_numbers)

        # init lock
        lock = Lock()
        # multiprocessing iteration with lock
        with Pool(10, initializer=init_lock, initargs=(lock,)) as pool:
            args = [(iteration_numbers[i], idx, generator) for i, idx in enumerate(numbers)]
            list(tqdm(pool.starmap(process_output, args), total=len(numbers)))

    except Exception as e:  # 一般的な例外処理
        if "rate_limit_exceeded" in str(e) and retry_count < max_retries:
            wait_time = 600  # エラーメッセージで指定された待機時間
            print(f"Rate limit reached, waiting for {wait_time} seconds and retrying... ({retry_count + 1}/{max_retries})")
            time.sleep(wait_time)
            main3(retry_count + 1, max_retries)
        else:
            print(f"An error occurred: {e}")
            if retry_count >= max_retries:
                print("Max retries reached, stopping execution.")

    end_time = time.time()
    print(end_time - start_time)

if __name__ == "__main__":
    main3()
