import numpy as np
import torch, torch.nn as nn
from torch.autograd import Variable

from agym.models import (
    IQValuesModel,
)

from typing import (
    List,
)


class GlobalMaxPooling(nn.Module):
    def __init__(self, dims=[-1]):
        super(self.__class__, self).__init__()
        self.dims = dims

    def forward(self, x):
        for dim in reversed(self.dims):
            x = x.max(dim=dim)[0]
        return x


class ConvQValuesModel(IQValuesModel):
    def __init__(self, n_actions: int,
                 filters_list: List[int],
                 hidden_units_list: List[int]):
        layers: List[nn.Module] = []

        prev_filters = filters_list[0]
        for filters in filters_list[1:-1]:
            layers.append(nn.Conv2d(prev_filters, filters,
                                    kernel_size=3, padding=1))
            layers.append(nn.ReLU())
            layers.append(nn.MaxPool2d(2))
            prev_filters = filters

        if len(filters_list) >= 2:
            filters = filters_list[-1]
            layers.append(nn.Conv2d(prev_filters, filters,
                                    kernel_size=3, padding=1))
            layers.append(nn.ReLU())

        layers.append(GlobalMaxPooling([2, 3]))

        prev_units = filters_list[-1]
        for units in hidden_units_list:
            layers.append(nn.Linear(prev_units, units))
            layers.append(nn.ReLU())
            prev_units = units

        layers.append(nn.Linear(prev_units, n_actions))

        self.model = nn.Sequential(*layers)

    def get_t_qvalues(self, t_states):
        t_qvalues = self.model(t_states)

        return t_qvalues

    def get_qvalues(self, states: np.ndarray):
        t_states = torch.from_numpy(states)
        t_qvalues = self.get_t_qvalues(t_states)
        qvalues = t_qvalues.data.numpy()

        return qvalues

    def get_action(self, state: np.ndarray) -> int:
        qvalues = self.get_qvalues(state[None, ...])[0, :]

        action = np.argmax(qvalues, axis=-1)
        return action

    def parameters(self):
        return self.model.parameters()

    def try_event(self, state) -> bool:
        return False
