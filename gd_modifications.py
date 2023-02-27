from gd import LearningRate, BaseDescent, LossFunction
from typing import Dict
from typing import Type

import numpy as np


def get_descent(descent_config: dict) -> BaseDescent:
    descent_name = descent_config.get('descent_name', 'full')
    regularized = descent_config.get('regularized', False)

    descent_mapping: Dict[str, Type[BaseDescent]] = {
        'full': VanillaGradientDescent #if not regularized else VanillaGradientDescentReg,
        #'stochastic': StochasticDescent if not regularized else StochasticDescentReg,
        #'momentum': MomentumDescent if not regularized else MomentumDescentReg,
        #'adam': Adam if not regularized else AdamReg,
        #'adamax': Adamax
    }

    if descent_name not in descent_mapping:
        raise ValueError(f'Incorrect descent name, use one of these: {descent_mapping.keys()}')

    descent_class = descent_mapping[descent_name]

    return descent_class(**descent_config.get('kwargs', {}))


class VanillaGradientDescent(BaseDescent):
    def update_weights(self, gradient: np.ndarray) -> np.ndarray:
        weight_difference = -self.lr() * gradient
        self.w += weight_difference
        return weight_difference

    def calc_gradient(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        if self.loss is LossFunction.MSE:
            return -2 / y.shape[0] * (x.T @ y - x.T @ (self.predict(x)))
        elif self.loss is LossFunction.MAE:
            return 1 / y.shape[0] * x.T @ np.sign(self.predict(x) - y)
        elif self.loss is LossFunction.LogCosh:
            return 1 / y.shape[0] * x.T @ np.tanh(self.predict(x) - y)
        elif self.loss is LossFunction.Huber:
            difference = self.predict(x) - y
            mask = (np.abs(difference) <= 1)
            less_delta = x[mask].T @ difference[mask]
            more_delta = x[~mask].T @ np.sign(difference[~mask])
            return 1 / y.shape[0] * (less_delta - more_delta)
