# Challenge: Resilient Edge

Making edge computing infrastructure resilient to power outages


## Description

The internet of things (IoT) and edge computing are core components of future smart cities. Interconnected computing systems will perform tasks beyond measuring and monitoring, and will also make decisions and take over highly critical tasks. Especially in disaster situations, such as extreme weather events, where for e.g. traffic control can be crucial to guarantee safety, we should therefore not rely on grid power supply to be available at all times.

In this challenge, students will investigate how to manage an edge computing node resilient against power outages by relying on on-site renewable energy generation and a battery. The node will be running a critical service that may never stop and can optionally take over workloads of lower priority if energy availability allows. Within this scenario, students can develop solutions for a variety of problems, such as: How should the edge node be managed in order to accept as many optional workloads as possible without risking power outage? How risky are different solutions to this problem? Can we use weather forecasts to improve our results? Can we maybe delay some non-urgent workloads and compute them when the sun is shining?

The objective of this challenge is to learn to use simulation and datasets to investigate abstract problems. Solutions to this challenge can either be technical and involve some programming, or you can use the simulation to back your conceptual ideas with some experimental data.


## Required/Suggested Tools

You are free to use any libraries or tools that help you researching the problem or supporting your ideas.

- [SimPy](https://simpy.readthedocs.io/): Python discrete-event simulation framework
- [LEAF](https://github.com/dos-group/leaf): Simulator for modeling energy consumption in edge computing based on SimPy
- [PyBaMM](https://github.com/pybamm-team/PyBaMM): Fast and flexible physics-based battery models in Python
- ... whatever you think is interesting


## Data

You are free to use any publicly available datasets in your data analysis or simulations.
Follow, a few suggestions.


### Weather Data

Solar irradiance and other weather time series can be useful to simulate the produced energy at your edge node. The repository includes `data/weather_berlin_2022-06.csv`, which contains minutely measurements of solar irradiance and wind speed in August 2021 in Berlin ([permalink](https://wetter.htw-berlin.de/History/EGH_SMP4,VWI_ANE1/2021-06-01/2021-06-30)). More weather data can be obtained from https://wetter.htw-berlin.de.

To help you get started, you can convert weather data to energy production using different formulas... TODO
Same with wind


### Taxi Data



- Amount of cars over time based on NYC Taxi data (https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)


