# Case 31: Abstract without numbers, claiming the highest value, over the word limit
Skill: write-abstracts-and-conclusions
Expected gates: G-AC-abs, G-AC-num, G-STY-front
Language: en
Snippet:
> (An abstract of 310 words in two paragraphs, citing two papers.) ... Experimental results show that the proposed algorithm achieves the highest hypervolume and superior performance compared with existing methods.
Why it fails: the abstract must be one paragraph without citations and inside the word limit, and its result move must give the metric value and the improvement range over the best-performing baseline with the instance scope.
