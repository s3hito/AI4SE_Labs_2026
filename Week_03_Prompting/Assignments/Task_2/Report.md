## ICIO
ValueError: No matching label question for prediction on line 103: 'give me a restaurant in the bay area for greek food with a rating above 4.5 (excellent or better)?'
## RTF
Accuracy: 0.2774 (27.74%)
Correct: 43/155
## CRISP
Accuracy: 0.2516 (25.16%)
Correct: 39/155

Most of the time the agents acted rather silly and tried to find workarounds or cut corners simply writing python parsers that achieved questionable results. Copilot setting was set to "Efficiency" and most of the time was routed to gpt-5.6-luna model.
Some prompts tried explicitly restricting the execution of scripts in hopes to get a result of more quality but it merely helped to mitigate the evaluation issues since at some point the .csv formatting would break therefore making such restrictions practically useless.
There was a total of 30+ tries of different prompt formats.