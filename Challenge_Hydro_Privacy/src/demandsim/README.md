# Water demand simulation

This Python package combines a water network simulation using [Water Network Tool for Resilience (WNTR)](https://github.com/USEPA/WNTR) with a residential water end-use model. The demand data generation is based on [STREaM (STochastic Residential water End-use Model)](https://github.com/acominola/STREaM), which is a Matlab tool recreated as Python code here.

### Preliminaries

Install [SciPy](https://www.scipy.org/), [NumPy](https://numpy.org/) and [WNTR](https://github.com/USEPA/WNTR). This package can be either used directly, or installed locally invoking `pip install PACKAGE-DIRECTORY`.

The original STREaM tool is using data from a MAT-file, which is only readable with restrictions in Python. The Matlab script `data/export.m` can be used to convert the original data into a readable structure.

### Demand data generation

To generate a single end-use trajectory you have to specify the household size (1-6), present applicances, the time horizon (days) and the resolution (10 second steps). Each datapoint in the resulting trajectory represents the amount of water in litres consumed since the last datapoint. Possibly you also have to specify the path to the database files, when initializing the generator object.

```
gen = DemandGenerator(horizon, ts)
trajectories = gen.generate_trajectories(appliances, hhsize)
```

A detailed example can be found in `examples/generate.py`.

### Network simulation

You can use demand trajectories directly in an WNTR simulation, by coupling end-use patterns to specific junction nodes.

```
sim = DemandSimulation(horizon, ts, inp_file)
sim.add_end_usages('junction_name', households)
result = sim.run()
```

A detailed example can be found in `examples/simulate.py`.