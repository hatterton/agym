import numpy as np
import torch, torch.nn as nn

from agym.model_wrappers.qlearning.replay_buffer import (
    ReplayBuffer,
)
from agym.model_wrappers import (
    IModelWrapper,
)
from agym.models import (
    IQValuesModel,
)

class SarsaWrapper(IModelWrapper):
    def __init__(self, model: IQValuesModel,
                 n_actions: int, eps: float = 0.1, gamma: float = 0.9):
        self.model = model
        self.n_actions = n_actions
        self.eps = eps
        self.gamma = gamma

        self.batch_size = 32
        self.n_iters_per_epoch = 10

        self.last_state: np.ndarray
        self.last_action: int
        self.replay_buffer = ReplayBuffer(1000)

    def get_action(self, state) -> int:
        best_action = self.model.get_action(state)

        action: int
        if np.random.random() < self.eps:
            action = np.random.choice(self.n_actions)
        else:
            action = best_action

        self.last_state = state
        self.last_action = action
        return action

    def post_action(self, next_state, reward: int, is_done: bool) -> None:
        self.replay_buffer.add(
            self.last_state, self.last_action, reward, next_state, is_done)

        if is_done:
            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
            for i in range(self.n_iters_per_epoch):
                batch = self.replay_buffer.sample(self.batch_size)
                # states, actions, rewards, next_states, is_done = batch
                loss = self.td_loss(*batch)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

    def td_loss(self, states, actions, rewards,
               next_states, is_done) -> torch.Tensor:
        states = torch.from_numpy(states)
        print(actions)
        actions = torch.from_numpy(actions[:, None])
        rewards = torch.from_numpy(rewards[:, None])
        next_states = torch.from_numpy(next_states)
        is_done = torch.from_numpy(states.astype("float32")[:, None])

        predicted_qvalues = self.model.get_t_qvalues(states)
        predicted_qvalues_for_actions = torch.gather(
            predicted_qvalues, dim=1, index=actions)

        predicted_next_qvalues = self.model.get_t_qvalues(next_states)
        predicted_next_svalues = torch.max(
            predicted_next_qvalues, dim=1, keepdim=True)[0]

        target_qvalues_for_actions = (
            rewards + self.gamma * predicted_next_svalues)
        target_qvalues_for_actions = (
            is_done * rewards + 
            (1 - is_done) * target_qvalues_for_actions
        )

        diff = (predicted_qvalues_for_actions - 
            target_qvalues_for_actions.detach())
        loss = torch.mean(diff ** 2)

        assert(loss.shape == [])
        return loss

    def try_event(self, event) -> bool:
        return False

