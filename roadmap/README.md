# DSA + AI Roadmap

**A step-by-step plan to learn Data Structures and Algorithms and to use that skill in the age of AI.** Follow it from the top
if you are new, or jump to the stage you are at. Every DSA stage links to the code and notes in this repository.

[Back to the course home](../README.md)

## Why DSA still matters when AI can write code

As the video explains, AI tools can now produce a large share of the code. What they cannot replace is a person who can
**read that code, find the bug, and make it faster or cheaper**. That is exactly what data structures, algorithms and
complexity analysis train you to do.

- **You can judge a solution.** Is it correct for the edge cases? Is it O(n) or O(n^2)? Will it still work with a million inputs?
- **You can debug.** Recursion, loops and data structures are where most real bugs hide.
- **You can talk about trade-offs** in interviews and on the job.
- **You build better AI products.** Search, caching, queues and trees sit underneath retrieval, agents and pipelines.

## The two paths at a glance

| Path | Goal | You will finish with |
|---|---|---|
| **DSA path** (stages 0 to 9) | Think and code like a problem solver | Recursion, complexity, core structures, trees and DP |
| **AI path** (stages A to F) | Understand and build with AI | The AI vocabulary, prompting, and small AI projects |

Do them side by side if you like: a few DSA problems a day plus one AI idea a week.

## DSA path

| Stage | Goal | Study | Practice | Suggested pace* |
|---|---|---|---|---|
| 0 | Python basics | [Hello Python](https://github.com/mayank953/python-ai-crash-course) (variables to functions) | The checkpoint assignments there | 2 to 4 weeks |
| 1 | The DSA mindset and arrays | Video `2:21` to `24:38`, [arrays](../dsa-topics/arrays/) | Rebuild a list from scratch | 3 to 5 days |
| 2 | Time and space complexity | [Complexity notes and notebooks](../dsa-topics/time-and-space-complexity/) | Time two sorting functions on growing inputs | 1 week |
| 3 | **Recursion** (the video) | [Introduction](../recursion/01-introduction-to-recursion/), [arrays](../recursion/02-recursion-and-arrays/), [searching and sorting](../recursion/03-searching-and-sorting/), [strings](../recursion/04-recursion-and-strings/) | The four [checkpoints](../assignments/README.md) | 2 to 3 weeks |
| 4 | Linked list | [Linked list](../dsa-topics/linked-list/) | Insert, delete, reverse | 1 week |
| 5 | Stack and queue | [Stack](../dsa-topics/stack/), [queue](../dsa-topics/queue/) | Balanced brackets, queue from two stacks | 1 week |
| 6 | Hashmaps | [Hashmaps](../dsa-topics/hashmaps/) | Count frequencies, two-sum | 1 week |
| 7 | Trees and BST | [Trees](../dsa-topics/trees/) | Traversals, height, search in a BST | 2 weeks |
| 8 | Dynamic programming | [DP starter](../dsa-topics/dynamic-programming/) (needs recursion) | Fibonacci with memoisation, then climbing stairs | 2 to 3 weeks |
| 9 | Keep going | Heaps, graphs, tries (not covered here yet) | Daily problems on a coding site | ongoing |

\*A suggestion for about an hour of study a day. Finishing matters more than speed.

### How to work through each stage

1. **Watch or read** the topic once without coding.
2. **Code it yourself** from a blank file. Peek at the repo code only when stuck.
3. **Do the "Try it yourself" tasks** and the checkpoint.
4. **Explain it aloud** in two minutes, as if to a friend.
5. **Redo one problem a week later** without notes. That is when it really sticks.

### Recursion in four moves (the heart of stage 3)

1. Write the **base case**: the smallest problem you can answer directly.
2. **Assume** the function already works for a smaller input (this is the principle of mathematical induction at work).
3. Use that answer to build the answer for the current input.
4. Draw the **recursion tree** for a small example to confirm it.

## AI path

| Stage | Goal | Start here | Suggested pace* |
|---|---|---|---|
| A | The language of AI (LLM, tokens, RAG, MCP, agents) | [AI concepts](https://github.com/mayank953/python-ai-crash-course/tree/main/ai-concepts) | 3 to 5 days |
| B | Use AI well: prompting and context | The prompting and context sections in the AI concepts guide | ongoing |
| C | Call a model from Python | A provider's official documentation, plus your Python basics | 1 week |
| D | Give a model your own documents (RAG) | Needs hashmaps, lists and search (stages 1 to 6) | 2 weeks |
| E | Give a model tools and let it act (MCP, agents) | Needs functions and loops (stage 0) | 2 weeks |
| F | Evaluate, optimise and ship | Complexity and cost thinking (stage 2) | ongoing |

New to AI? The [AI roadmap for beginners](https://github.com/mayank953/python-ai-crash-course/blob/main/roadmap/README.md) in the Hello Python repo is the gentler starting point.

## How DSA shows up in AI work

| DSA idea | Where you meet it in AI |
|---|---|
| Time and space complexity | Latency, memory and the cost of every model call and pipeline step |
| Hashmaps | Caches, lookups, counting tokens or words, deduplication |
| Lists and sorting | Ranking results, top-k answers, ordering retrieved passages |
| Queues | Batching requests and background jobs |
| Stacks and recursion | Call stacks, parsing nested JSON, walking folders and syntax trees |
| Trees and graphs | Structured outputs, knowledge graphs, workflows and agent plans |
| Dynamic programming | Reusing earlier results instead of recomputing them |

## A sample 12-week plan (one hour a day)

| Weeks | Focus |
|---|---|
| 1 to 2 | Python basics, [Hello Python](https://github.com/mayank953/python-ai-crash-course) lessons on functions and data structures |
| 3 | Arrays, complexity, the AI vocabulary (stage A) |
| 4 to 6 | Recursion: the four topics and checkpoints |
| 7 | Linked list, stack and queue |
| 8 | Hashmaps, plus a small RAG idea on paper (stage D) |
| 9 to 10 | Trees and BST |
| 11 | Dynamic programming starter |
| 12 | Revise, then build one small project that uses a data structure and a model call |

## Habits that make it work

- **Type the code.** Reading is not practising.
- **Draw before you code**: trees, stacks and pointers on paper first.
- **Do a few problems a day** instead of many on one day.
- **Keep an error log**: the bug, the cause, the fix.
- **Use AI as a tutor, not an answer machine**: ask it to quiz you or explain an error before asking for the answer.
- **Share your progress** with the hashtag #HelloDSA.

## Common mistakes

- Memorising solutions instead of the pattern behind them.
- Skipping complexity and then not knowing why a solution is slow.
- Jumping to dynamic programming before recursion feels natural.
- Ignoring edge cases: empty input, one element, duplicates, negative numbers.

[Back to the course home](../README.md)
