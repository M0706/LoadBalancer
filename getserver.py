import random
from abc import ABC, abstractmethod

class LoadBalancerStrategy(ABC):
    def __init__(self, server_list):
        self.server_list = server_list

    @abstractmethod
    def get_next_server(self):
        pass


class RandomStrategy(LoadBalancerStrategy):
    def __init__(self, server_list):
        super().__init__(server_list)

    def get_next_server(self):
        return random.choice(self.server_list)

class LoadBalancer:
    def __init__(self, strategy: str, server_list: list):
        self.server_list = server_list
        self.strategy = self._create_strategy(strategy)

    def _create_strategy(self, strategy: str):
        if strategy == "random":
            return RandomStrategy(self.server_list)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def get_next_server(self):
        return self.strategy.get_next_server()

server_list = ['http://127.0.0.1:8001', 'http://127.0.0.1:8002', 'http://127.0.0.1:8003']

load_balancer = LoadBalancer(strategy="random", server_list=server_list)



