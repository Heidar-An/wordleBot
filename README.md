# wordleBot

Inspired by 3b1b, me and my friend decided to make a wordle bot.

## How it works

For every 5 letter word, we compare it to **every** other word and see what pattern is created,
e.g. GGGGG = means that same word, etc. This part would be terribly inefficient, because for the small word file, this would take 9 million
comparions, and for the large word file, this would take 169 million comparisons. Thus, we have already precomputed them, into a file called
data.json, which stores all key-value pairs, the key being "guessWord:correctWord", and the value being the pattern generated e.g. "BYBYY"

After doing this, we find out the probability (p) that each pattern occurs for a single word, e.g. "BBYYG" might be 23/size of words array. We multiply
this by log base 2(1/p) - which calculates the entropy of the probabiility, and sum this up. After summing this up, we find the best word,
and display that.
