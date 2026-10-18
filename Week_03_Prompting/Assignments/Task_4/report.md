| Framework    | Prompt time execution |Default score|Alt. score|
| -------- | ------- |-------|-------|
| ICIO  | 2 min.     |FAIL|FAIL|
| RTF | 2 min. 41 sec.|0.2774|0.2185|
| CRISP    | 23 sec.|0.2516|0.2075|

The results were different across multiple instances and partially random as sometimes the agent could choose to verify the integrity of the queries and at some instances they could decide not to. CRIPS provided the quickest result but of the poorest quality. I had personally huge hopes for ICIO due to the iterative approach and strict rules that had been prompted to it but it failed at multiple instances. Agents were viewing the repeated information multiple times for no obvious reason therefore large portion of tokens were simply wasted. The results could have been better if I were to choose slightly different setup other than "Efficient" within the copilot settings as it seems that it was one of the main factors (paried with my poor prompting skill). In the result over 30% of the monthly token limit were spent which is quite a number. Each prompt was run a number of times iteratively improving leading to such waste.