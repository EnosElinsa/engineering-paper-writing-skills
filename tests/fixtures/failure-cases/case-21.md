# Case 21: Component gain reported as an overall advantage
Skill: write-experiments
Expected gates: G-EX-offset
Language: en
Snippet:
> When the charging van follows the drones, their return flights become shorter and the drones consume less return energy on every map. The mobile van therefore makes the whole system more energy efficient than a parked van.
Why it fails: the van spends energy driving, which can offset the drones' saving. The result reports one component, not the net system energy.
