import json
import os
class Checkpoint:
    def __init__(self, filepath, init=False):
        self.filepath = filepath
        self.checkpoints = self._load_checkpoint()
        self.init = init

    def _load_checkpoint(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        else:
            return {'checkpoint': {}}

    def save_checkpoint(self, checkpoint_key):
        self.checkpoints['checkpoint'][checkpoint_key] = True
        with open(self.filepath, 'w') as f:
            json.dump(self.checkpoints, f)

    def get_incomplete_points(self, numbers, iteration_numbers):
        incomplete_numbers = []
        incomplete_iterations = []
        for key in [f"{n}_{i}" for n, i in zip(numbers, iteration_numbers)]:
            if not self.checkpoints['checkpoint'].get(key, False):
                first, second = map(int, key.split('_'))
                incomplete_numbers.append(first)
                incomplete_iterations.append(second)
        return incomplete_numbers, incomplete_iterations