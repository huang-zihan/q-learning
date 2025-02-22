import numpy as np
import random
from environmentclip import Env
from collections import defaultdict
import dill

class SarsaAgent:
    def __init__(self, actions):
        # actions = [0, 1, 2, 3]
        self.actions = actions
        self.learning_rate = 0.01
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    # 采样 <s, a, r, s'>
    def learn(self, state, action, reward, next_state, next_action):
        current_q = self.q_table[state][action]
        # 贝尔曼方程更新
        new_q = reward + self.discount_factor * self.q_table[next_state][next_action]
        self.q_table[state][action] += self.learning_rate * (new_q - current_q)

    # 从Q-table中选取动作
    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            # 贪婪策略随机探索动作
            action = np.random.choice(self.actions)
        else:
            # 从q表中选择
            state_action = self.q_table[state]
            action = self.arg_max(state_action)
        return action

    def save_model(self, filename):
        dill.dump(self.q_table, open(filename, 'wb'))

    def load_model(self, filename):
        self.q_table = dill.load(open(filename,"rb"))

    @staticmethod
    def arg_max(state_action):
        max_index_list = []
        max_value = state_action[0]
        for index, value in enumerate(state_action):
            if value > max_value:
                max_index_list.clear()
                max_value = value
                max_index_list.append(index)
            elif value == max_value:
                max_index_list.append(index)
        return random.choice(max_index_list)


if __name__ == "__main__":
    #初始化
    env = Env()
    agent = SarsaAgent(actions=list(range(env.n_actions)))
    action = next_action = None
    
    agent.load_model('sarsa450.ckpt')
    
    for episode in range(450,600):
        state = env.reset()
        while True:
            env.render()
            # agent选择已经决定的动作(初始则新选一个)
            action = next_action if next_action is not None else agent.get_action(str(state))
            next_state, reward, done = env.step(action)
            # 选择下一步的动作
            next_action=agent.get_action(str(next_state))
            # 更新Q表
            agent.learn(str(state), action, reward, str(next_state), next_action)
            state = next_state
            env.print_value_all(agent.q_table)
            # 当到达终点就终止游戏开始新一轮训练
            if done:
                if (episode+1) % 50 == 0:
                    agent.save_model(f"sarsa{episode}.ckpt")
                break
