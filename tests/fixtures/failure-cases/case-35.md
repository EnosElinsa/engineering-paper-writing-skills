# Case 35: Abstract and contribution list disagree after a rerun
Skill: write-abstracts-and-conclusions
Expected gates: G-AC-sync
Language: en
Snippet:
> Abstract: improving mean hypervolume by 3.1%–95.0% over the best-performing baseline. Last contribution item: a higher mean hypervolume than four baselines on two instances. Results table after the rerun: 4.4%–120.7% over five baselines on three instances.
Why it fails: the summary parts report different ranges, baseline counts, and instance scopes, and neither matches the regenerated table.
