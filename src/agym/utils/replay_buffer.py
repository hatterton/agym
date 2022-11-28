# This code is shamelessly stolen from https://github.com/openai/baselines/blob/master/baselines/deepq/replay_buffer.py
import random
from itertools import chain

import numpy as np


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

        if self._maxsize > len(self._storage):
            self._storage.append(data)
            self._order.append(self._next_idx)
            self._next_idx = (self._next_idx + 1) % self._maxsize
        else:
            new_id = random.randint(0, self._maxsize - 1)
            self._order.append(new_id)
            self._storage[new_id] = data
            if len(self._order) > 2 * self._maxsize:
                self._order = self._order[-self._maxsize :]

    def _extract_batch(self, idxes):
        states, actions, rewards, next_states, dones = [], [], [], [], []

        for i in idxes:
            data = self._storage[i]
            state, action, reward, next_state, done = data

            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            dones.append(done)

        return (
            np.stack(states, axis=0),
            np.array(actions),
            np.array(rewards),
            np.stack(next_states, axis=0),
            np.array(dones),
        )

    def sample(self, batch_size):
        last_size = batch_size // 2
        random_size = batch_size - last_size

        storage_size = len(self._storage)
        order_size = len(self._order)

        lower_bound = max(0, order_size - last_size)
        last_idxes = [self._order[i] for i in range(lower_bound, order_size)]
        random_idxes = [
            random.randint(0, storage_size - 1) for _ in range(random_size)
        ]

        idxes = chain(last_idxes, random_idxes)
        batch = self._extract_batch(idxes)
        # print(batch)

        return batch
