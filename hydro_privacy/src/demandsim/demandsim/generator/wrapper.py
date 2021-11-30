import numpy as np


Rng = np.random._generator.Generator


class UseFrequency:
    """Use frequency wrapper class."""

    def __init__(self):
        self.number_of_events_per_day = dict()
        self.event_duration = dict()
        self.event_start_time = dict()
        self.event_volume = dict()


class UseProbability:
    """Use probability wrapper class."""

    def __init__(self):
        self.number_of_events_per_day = dict()
        self.event_start_time = dict()
        self.gmduration_and_volume = dict()

    def get_number_of_events_per_day(self, hhsize: int, rng: Rng) -> int:
        dist_type = self.number_of_events_per_day['distributions'][hhsize-1][0][0][0]

        if dist_type == 'PoissonDistribution':
            lam = self.number_of_events_per_day['distributions'][hhsize-1][0][3][0][0]
            return rng.poisson(lam)

        elif dist_type == 'NegativeBinomialDistribution':
            n = self.number_of_events_per_day['distributions'][hhsize-1][0][1][0][0]
            p = self.number_of_events_per_day['distributions'][hhsize-1][0][2][0][0]
            return rng.negative_binomial(n, p)

        raise Exception('Unsupported distribution type!')

    def get_gmduration_and_volume(self, hhsize: int, rng: Rng) -> np.ndarray:
        mu = self.gmduration_and_volume['gm'][0][hhsize-1][0]
        p = self.gmduration_and_volume['gm'][0][hhsize-1][1][0]
        sigma = self.gmduration_and_volume['gm'][0][hhsize-1][2]
        which = 0 if rng.random() < p[0] else 1
        return rng.multivariate_normal(mu[which], sigma)

    def get_event_start_time(self, hhsize: int, rng: Rng) -> int:
        bandwidth = self.event_start_time['kd'][0][hhsize-1][1]
        input_data = self.event_start_time['kd'][0][hhsize-1][3]
        sample = rng.choice(input_data)
        t = rng.normal(sample, bandwidth)[0][0]
        # t == 1 -> 24 hours
        return round(abs(t)*24*60*6)
