import json
import os
from multiprocessing import Pool, Lock

class Checkpoint:
    def __init__(self, checkpoint_path, numbers, iteration_numbers, init=False,):
        self.checkpoint_path = checkpoint_path
        self.init = init
        self.numbers = numbers
        self.iteration_numbers = iteration_numbers
        self._numbers = []
        self._iteration_numbers = []
        self.checkpoints = self.load_checkpoint()

    def load_checkpoint(self):
        checkpoint_key = [f"{n}_{i}" for n, i in zip(self.numbers, self.iteration_numbers)]

        if os.path.exists('checkpoint.json') and not self.init:
            with open('checkpoint.json', 'r') as f:
                checkpoints = json.load(f)
            self.make_newlist(checkpoints)

        else:
            with open('checkpoint.json', 'w') as f:
                checkpoint_dic = {'checkpoint': {str(key): False for key in checkpoint_key}}
                json.dump(checkpoint_dic, f)

            checkpoints = checkpoint_dic
            self.make_newlist(checkpoints)

    #ロードしたチャックポイントをもとに未完部を確認し、リストを作成
    def make_newlist(self, checkpoints):
        for item in checkpoints.get('checkpoint'):
            first, second = item.split('_')
            self._numbers.append(int(first))
            self._iteration_numbers.append(int(second))


    def update(self, id, idx, global_lock):
        with global_lock:
            with open(self.checkpoint_path, 'r+') as f:
                checkpoints = json.load(f)
                checkpoint_key = f'{str(idx)}_{str(id)}'
                checkpoints['checkpoint'][checkpoint_key] = True
                f.seek(0)
                f.truncate()
                json.dump(checkpoints, f)
