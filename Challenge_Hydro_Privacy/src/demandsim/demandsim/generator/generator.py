import os
import scipy.io
import numpy as np

from .datatypes import Appliances, Trajectories, Fixtures
from .wrapper import UseFrequency, UseProbability


class DemandGenerator:
    """Demand data generator class."""

    def __init__(self, horizon: int, ts: int, directory: str = None) -> None:
        """Constructor creating a demand generator object with specific time horizon and step."""

        self.horizon = horizon
        self.ts = ts

        self.signatures = {}
        self.frequencies = {}
        self.probabilities = {}

        self._data_loaded = False
        self._rng = np.random.default_rng()

        self._load_data(directory)

    def _load_data(self, directory=None):
        if directory is None:
            directory = os.path.dirname(os.path.realpath(__file__)) + '/../../data'

        signatures_dir = directory + '/signatures'
        frequencies_dir = directory + '/UseFrequencies'
        probabilities_dir = directory + '/UseProbabilities'

        # Load signatures
        for filename in os.listdir(signatures_dir):
            if filename.endswith('.mat'):
                self.signatures[os.path.splitext(filename)[0]] = scipy.io.loadmat(
                    os.path.join(signatures_dir, filename))

        # Load UseFrequencies
        subdirs = [f.name for f in os.scandir(frequencies_dir) if f.is_dir()]
        for dir in subdirs:
            uf = UseFrequency()
            uf.number_of_events_per_day = scipy.io.loadmat(
                frequencies_dir + '/' + dir + '/NumberOfEventsPerDay.mat')
            uf.event_duration = scipy.io.loadmat(
                frequencies_dir + '/' + dir + '/EventDuration.mat')
            uf.event_start_time = scipy.io.loadmat(
                frequencies_dir + '/' + dir + '/EventStartTime.mat')
            uf.event_volume = scipy.io.loadmat(
                frequencies_dir + '/' + dir + '/EventVolume.mat')
            self.frequencies[dir] = uf

        # Load UseProbabilities
        subdirs = [f.name for f in os.scandir(probabilities_dir) if f.is_dir()]
        for dir in subdirs:
            up = UseProbability()
            up.number_of_events_per_day = scipy.io.loadmat(
                probabilities_dir + '/' + dir + '/NumberOfEventsPerDay.mat')
            up.gmduration_and_volume = scipy.io.loadmat(
                probabilities_dir + '/' + dir + '/GMDurationAndVolume.mat')
            up.event_start_time = scipy.io.loadmat(
                probabilities_dir + '/' + dir + '/EventStartTime.mat')
            self.probabilities[dir] = up

        self._data_loaded = True

    def initialize_trajectories(self, appliances: Appliances) -> dict:
        """Initialize trajectories for given appliances using the generator properties."""

        trajectories = {}
        for fixture in appliances:
            trajectories[fixture.value] = np.zeros(self.horizon*24*360, dtype=float)
        return trajectories

    def consumption_events(self, trajectories: Trajectories, hhsize: int) -> Trajectories:
        """Create consumption events in the trajectories using probabilities from the database."""

        # Check if database is loaded
        if not self._data_loaded:
            raise Exception('Database not loaded!')

        for k in trajectories.keys():
            for dayID in range(0, self.horizon):
                # Number of events per day
                numEvents = self.probabilities[k].get_number_of_events_per_day(
                    hhsize, self._rng)

                # Duration and Volume
                durations = np.zeros(numEvents)
                volumes = np.zeros(numEvents)
                time_start = np.zeros(numEvents)
                for eventID in range(0, numEvents):
                    tempDurVol = np.exp(
                        self.probabilities[k].get_gmduration_and_volume(hhsize, self._rng))
                    if self._rng.random() > 0.5:
                        tempDurVol = np.ceil(tempDurVol)
                    else:
                        tempDurVol = np.floor(tempDurVol)

                    durations[eventID] = tempDurVol[0] if tempDurVol[0] > 0 else 1.0
                    volumes[eventID] = tempDurVol[1] if tempDurVol[1] > 0 else 1.0

                    # Time of day
                    time_start[eventID] = self.probabilities[k].get_event_start_time(
                        hhsize, self._rng)

                    # Resizing signature
                    sig_name = None
                    if k == 'StToilet':
                        sig_name = 'StandardToilet'
                    elif k == 'HEToilet':
                        sig_name = 'EfficientToilet'
                    elif k == 'StShower':
                        sig_name = 'StandardShower'
                    elif k == 'HEShower':
                        sig_name = 'StandardShower'
                    elif k == 'StFaucet':
                        sig_name = 'StandardFaucet'
                    elif k == 'HEFaucet':
                        sig_name = 'StandardFaucet'
                    elif k == 'StClothesWasher':
                        sig_name = 'StandardClothesWasher'
                    elif k == 'HEClothesWasher':
                        sig_name = 'EfficientClothesWasher'
                    elif k == 'StDishwasher':
                        sig_name = 'StandardDishwasher'
                    elif k == 'HEDishwasher':
                        sig_name = 'StandardDishwasher'
                    elif k == 'StBathtub':
                        sig_name = 'Bathtub'
                    elif k == 'HEBathtub':
                        sig_name = 'Bathtub'
                    else:
                        raise Exception('Unknown appliance!')

                    rnd_sig = self._rng.integers(
                        0, len(self.signatures[sig_name]['values'][0]))
                    event = self.signatures[sig_name]['values'][0][rnd_sig][0]
                    event = event[1:len(event)-1]

                    # Resizing signature length
                    positive = np.where(event > 0)
                    delta_size = int(durations[eventID] - positive[0].size)

                    if delta_size > 0:
                        # Duplicate positive elements
                        duplicates = np.random.default_rng().choice(
                            positive[0], abs(delta_size))
                        values = np.take(event, duplicates)
                        event = np.insert(event, duplicates, values)
                    elif delta_size < 0:
                        # Remove positive elements
                        removals = np.random.default_rng().choice(
                            positive[0], abs(delta_size), replace=False, shuffle=False)
                        event = np.delete(event, removals)

                    # Resizing signature volume
                    event_volume = np.sum(event)
                    if event_volume > volumes[eventID] or event_volume < volumes[eventID]:
                        event = np.divide(
                            event, event_volume / volumes[eventID])

                    # Placing event in time series
                    start_idx = int(
                        max(min(dayID*24*360 + time_start[eventID], len(trajectories[k])), 0))
                    end_idx = int(max(
                        min(dayID*24*360 + time_start[eventID] + len(event), len(trajectories[k])), 0))
                    num_of_elem = end_idx - start_idx
                    trajectories[k][start_idx:end_idx] = event[:num_of_elem]

        return trajectories

    def aggregate_resolution(self, trajectories: Trajectories) -> Trajectories:
        """Aggregate 10-second sampling resolution time series to a desired resolution."""

        for k in trajectories.keys():
            trajectory = np.cumsum(trajectories[k])
            # Pick elements from trajectory by timestep interval
            trajectory = trajectory[self.ts-1::self.ts]
            trajectory = np.insert(trajectory, 0, 0)
            trajectories[k] = np.diff(trajectory)

        return trajectories

    def generate_trajectories(self, appliances: Appliances, hhsize: int, summarize: bool = True) -> Trajectories:
        """Generate demand trajectories for given appliances and household size."""

        trajectories = self.initialize_trajectories(appliances)
        trajectories = self.consumption_events(trajectories, hhsize)
        trajectories = self.aggregate_resolution(trajectories)

        if summarize:
            # Sum all individual trajectories
            trajectories['Total'] = None
            for k in trajectories.keys():
                if trajectories['Total'] is None:
                    trajectories['Total'] = trajectories[k]
                else:
                    if k != 'Total': #####
                        trajectories['Total'] = np.add(
                            trajectories['Total'], trajectories[k])

        return trajectories
