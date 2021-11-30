from typing import TypedDict, FrozenSet
from enum import Enum
import numpy as np


class Fixtures(Enum):
    """Available fixtures."""

    StToilet = 'StToilet'
    HEToilet = 'HEToilet'
    StShower = 'StShower'
    HEShower = 'HEShower'
    StFaucet = 'StFaucet'
    HEFaucet = 'HEFaucet'
    StClothesWasher = 'StClothesWasher'
    HEClothesWasher = 'HEClothesWasher'
    StDishwasher = 'StDishwasher'
    HEDishwasher = 'HEDishwasher'
    StBathtub = 'StBathtub'
    HEBathtub = 'HEBathtub'


# Set of fixtures
Appliances = FrozenSet[Fixtures]


class Trajectories(TypedDict, total=False):
    """Container class for end-use trajectories."""

    StToilet: np.ndarray
    HEToilet: np.ndarray
    StShower: np.ndarray
    HEShower: np.ndarray
    StFaucet: np.ndarray
    HEFaucet: np.ndarray
    StClothesWasher: np.ndarray
    HEClothesWasher: np.ndarray
    StDishwasher: np.ndarray
    HEDishwasher: np.ndarray
    StBathtub: np.ndarray
    HEBathtub: np.ndarray
