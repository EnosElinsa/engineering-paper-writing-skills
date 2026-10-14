# Negative control 04: scenario-like paragraph of the terrain-aware paper

Skill: write-introductions
Expected: no hard failure on G-INT-15 to G-INT-18; the system description lives in a contribution item, so this paragraph is not a scenario benchmark.

Functional structure, described in our own words (seven sentences, about 220 words in the reference):

1. Answers two stated issues, path-loss estimation on complex terrain and flight safety, with a proposed channel model.
2. Says what the model estimates: signal strength under blockage by terrain and buildings, using elevation data.
3. Describes the core idea: split space into a visible region and a blocked region around each ground device.
4. Explains how the blocked region is represented, with vectors from the device to surrounding terrain points.
5. Says that signal conditions follow from the distance between the aerial unit and the blocked region.
6. Introduces the optimization problem over trajectory, destination, and resource allocation, aiming at service quality while keeping flight safe.
7. In the extracted text this last sentence appears twice; the duplicate is an extraction artifact and must not be copied.

The paragraph mixes the channel model with the problem statement, which is why the scenario is carried by a contribution item instead.
