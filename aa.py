import os
import shutil
import time


def process_files(directory, checker, trash_dir, filtered_dir):
    # trash_output ディレクトリが存在しない場合は作成
    if not os.path.exists(trash_dir):
        os.makedirs(trash_dir)

    if not os.path.exists(filtered_dir):
        os.makedirs(filtered_dir)

    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            file_path = os.path.join(directory, filename)
            start_time = time.time()
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_content = file.read()
                end_time = time.time()
                timeee = end_time - start_time
                print('time_load;', timeee)

            # NGワードのチェック
            if not checker.detect_ng_word(xml_content):

                new_filename = f"including_ng_word_{filename}"
                new_file_path = os.path.join(directory, new_filename)
                os.rename(file_path, new_file_path)
                print(f"Renamed '{filename}' to '{new_filename}'")

                # 新しいファイルをtrash_outputに移動
                trash_file_path = os.path.join(trash_dir, new_filename)

                shutil.move(new_file_path, trash_file_path)
                print(f"Moved '{new_filename}' to '{trash_dir}'")
            else:
                filtered_file_path = filtered_dir
                print(filtered_file_path)
                shutil.move(file_path, filtered_file_path)



checker = Checker('assets/input/ngword_list.csv')
# ディレクトリ内のファイルを処理
process_files('old_output/A_output', checker, 'old_output/A_trash_output/', 'old_output/A_filtered_output/')