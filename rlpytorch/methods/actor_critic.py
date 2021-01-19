# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import torch
import torch.nn as nn
from torch.autograd import Variable
import math

from ..args_provider import ArgsProvider
from .policy_gradient import PolicyGradient
from .discounted_reward import DiscountedReward
from .value_matcher import ValueMatcher
from .utils import add_err

# Actor critic model.
class ActorCritic:
    ''' An actor critic model '''
    def __init__(self):
        ''' Initialization of `PolicyGradient`, `DiscountedReward` and `ValueMatcher`.
        Initialize the arguments needed (num_games, batchsize, value_node) and in child_providers.
        '''
        self.pg = PolicyGradient()
        self.discounted_reward = DiscountedReward()
        self.value_matcher = ValueMatcher()

        self.args = ArgsProvider(
            call_from = self,
            define_args = [
            ],
            more_args = ["num_games", "batchsize", "value_node"],
            child_providers = [ self.pg.args, self.discounted_reward.args, self.value_matcher.args ],
        )

    def update(self, mi, batch, stats):
        ''' Actor critic model update.
        Feed stats for later summarization.

        Args:
            mi(`ModelInterface`): mode interface used
            batch(dict): batch of data. Keys in a batch:
                ``s``: state,
                ``r``: immediate reward,
                ``terminal``: if game is terminated
            stats(`Stats`): Feed stats for later summarization.
        '''
        m = mi["model"]
        args = self.args
        value_node = self.args.value_node

        T = batch["s"].size(0)

        state_curr = m(batch.hist(T - 1)) # T步迭代计算价值
        self.discounted_reward.setR(state_curr[value_node].squeeze().data, stats) #设置 init_reward

        err = None
        # import pdb
        # pdb.set_trace()
        for t in range(T - 2, -1, -1):
            bht = batch.hist(t)
            state_curr = m.forward(bht)

            # go through the sample and get the rewards.
            V = state_curr[value_node].squeeze() # 前向传播计算价值

            R = self.discounted_reward.feed(
                dict(r=batch["r"][t], terminal=batch["terminal"][t]),
                stats=stats)  # 累计奖励(衰减)

            
            policy_err = self.pg.feed(R-V.data, state_curr, bht, stats, old_pi_s=bht) # 计算策略函数误差
            err = add_err(err, policy_err)
            err = add_err(err, self.value_matcher.feed({ value_node: V, "target" : R}, stats))

        # pdb.set_trace()

        stats["cost"].feed(err.data[0] / (T - 1))
        err.backward()
