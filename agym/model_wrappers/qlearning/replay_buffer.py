# This code is shamelessly stolen from https://github.com/openai/baselines/blob/master/baselines/deepq/replay_buffer.py
import numpy as np
import random
from itertools import chain

class ReplayBuffer(object):
    def __init__(self, size):
        self._storage = []
        self._order = []
        self._maxsize = size
        self._next_idx = 0

    def __len__(self):
        return len(self._storage)

    def add(self, obs_t, action, reward, obs_tp1, done):
        data = (obs_t, action, reward, obs_tp1, done)

        if self._next_idx >= len(self._storage):
            self._storage.append(data)
            self._order.append(self._next_idx)
            self._next_idx = (self._next_idx + 1) % self._maxsize
        else:
            new_id = random.randint(0, self._maxsize-1)
            self._order.append(new_id)
            self._storage[new_id] = data
            if len(self._order) > 2 * self._maxsize:
                self._order = self._order[-self._maxsize:]
            

    def _encode_sample(self, idxes):
        obses_t, actions, rewards, obses_tp1, dones = [], [], [], [], []
        for i in idxes:
            data = self._storage[i]
            obs_t, action, reward, obs_tp1, done = data
            obses_t.append(np.array(obs_t, copy=False))
            actions.append(np.array(action, copy=False))
            rewards.append(reward)
            obses_tp1.append(np.array(obs_tp1, copy=False))
            dones.append(done)
        return np.array(obses_t), np.array(actions), np.array(rewards), np.array(obses_tp1), np.array(dones)

    def sample(self, batch_size):
        last_size = batch_size // 2
        random_size = batch_size - last_size
        
        storage_size = len(self._storage)
        order_size = len(self._order)
        
        lower_bound = max(0, order_size - last_size)
        last_idxes = [self._order[i] for i in range(lower_bound, order_size)]
        random_idxes = [random.randint(0, storage_size-1) for _ in range(random_size)]
        
        idxes = chain(last_idxes, random_idxes)
                                      
        return self._encode_sample(idxes)
