# DSA + AI Roadmap

**A step-by-step plan to learn Data Structures and Algorithms, and to use that skill in the age of AI.** Follow it from the top if you are
new, or jump to the stage you are at. Every DSA stage links to the matching **handbook chapters**, the **video**, the **code and notes** in this
repository, and the **practice notebooks**.

[Back to the course home](../README.md) · [The handbook](../handbook/README.md)

## Why DSA still matters when AI can write code

As the video explains, AI tools can now produce a large share of the code. What they cannot replace is a person who can
**read that code, find the bug, and make it faster or cheaper**. That is exactly what data structures, algorithms and
complexity analysis train you to do.

- **You can judge a solution.** Is it correct for the edge cases? Is it O(n) or O(n^2)? Will it still work with a million inputs?
- **You can debug.** Recursion, loops and data structures are where most real bugs hide.
- **You can talk about trade-offs** in interviews and on the job.
- **You build better AI products.** Search, caching, queues and trees sit underneath retrieval, agents and pipelines ([handbook chapter 28](../handbook/28-dsa-behind-ai.md)).

## The two paths at a glance

| Path | Goal | You will finish with |
|---|---|---|
| **DSA path** (stages 0 to 11) | Think and code like a problem solver | Recursion, complexity, every core structure, sorting, DP, greedy, patterns |
| **AI path** (stages A to F) | Understand and build with AI | The AI vocabulary, prompting, and small AI projects |

Do them side by side if you like: a few DSA problems a day plus one AI idea a week.

## DSA path

| Stage | Goal | Read | Code, notes and video | Practice | Pace* |
|---|---|---|---|---|---|
| 0 | Python basics | [Hello Python](https://github.com/mayank953/python-ai-crash-course) | Functions, scope and slicing lessons | Its checkpoints | 2 to 4 weeks |
| 1 | The DSA mindset, Python for DSA, arrays | Handbook [1](../handbook/01-what-is-dsa.md), [2](../handbook/02-python-for-dsa.md), [14](../handbook/14-arrays-and-lists.md) | Video [`2:21`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=141s) to [`24:38`](https://www.youtube.com/watch?v=BhaHEnpNujI&t=1478s), [arrays](../dsa-topics/arrays/) | Chapter practice | 1 week |
| 2 | Time and space complexity | Handbook [3](../handbook/03-time-complexity.md), [4](../handbook/04-space-complexity.md) | [Complexity notes and notebooks](../dsa-topics/time-and-space-complexity/) | Count steps yourself | 1 week |
| 3 | **Recursion** (the video) | Handbook [5](../handbook/05-recursion-from-scratch.md), [6](../handbook/06-pmi-and-the-recursion-recipe.md), [7](../handbook/07-fibonacci-and-recursion-trees.md), [8](../handbook/08-head-vs-tail-recursion.md), [9](../handbook/09-recursion-on-arrays.md), [10](../handbook/10-searching-and-sorting-with-recursion.md), [11](../handbook/11-recursion-on-strings.md), [12](../handbook/12-the-choices-tree.md), [13](../handbook/13-backtracking.md) | [Introduction](../recursion/01-introduction-to-recursion/), [arrays](../recursion/02-recursion-and-arrays/), [searching and sorting](../recursion/03-searching-and-sorting/), [strings](../recursion/04-recursion-and-strings/) | [Checkpoints](../assignments/README.md), [Set 1](../assignments/B1-backtracking-and-search.ipynb) | 3 to 4 weeks |
| 4 | Linked lists | Handbook [15](../handbook/15-linked-list.md) | [Linked list](../dsa-topics/linked-list/) | [Set 2](../assignments/B2-lists-stacks-queues.ipynb) | 1 week |
| 5 | Stacks and queues | Handbook [16](../handbook/16-stack.md), [17](../handbook/17-queue-and-deque.md) | [Stack](../dsa-topics/stack/), [queue](../dsa-topics/queue/) | Set 2 | 1 week |
| 6 | Hashmaps | Handbook [18](../handbook/18-hashmaps.md) | [Hashmaps](../dsa-topics/hashmaps/) | [Set 3](../assignments/B3-hashmaps-trees-heaps.ipynb) | 1 week |
| 7 | Trees and binary search trees | Handbook [19](../handbook/19-trees.md), [20](../handbook/20-binary-search-trees.md) | [Trees](../dsa-topics/trees/) | Set 3 | 2 weeks |
| 8 | Heaps and graphs | Handbook [21](../handbook/21-heaps.md), [22](../handbook/22-graphs.md) | The BFS and DFS ideas from stack and queue | Sets 3 and [4](../assignments/B4-graphs-dp-greedy.ipynb) | 2 weeks |
| 9 | Sorting and binary search in depth | Handbook [23](../handbook/23-sorting-compared.md), [24](../handbook/24-binary-search-beyond.md) | [Merge sort and quick sort code](../recursion/03-searching-and-sorting/) | Set 1 | 1 week |
| 10 | Dynamic programming and greedy | Handbook [25](../handbook/25-dynamic-programming.md), [26](../handbook/26-greedy.md) | [DP starter](../dsa-topics/dynamic-programming/) | Set 4 | 3 weeks |
| 11 | Patterns and interviews | Handbook [27](../handbook/27-patterns-and-interview-playbook.md) | The whole repository | Daily problems on a coding site | ongoing |

\*A suggestion for about an hour of study a day. Finishing matters more than speed.

### How to work through each stage

1. **Watch or read** the topic once without coding.
2. **Code it yourself** from a blank file. Peek at the repo code only when stuck.
3. **Do the practice problems** at the end of the chapter, then the auto-checked notebooks.
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
| D | Give a model your own documents (RAG) | Handbook [18](../handbook/18-hashmaps.md), [21](../handbook/21-heaps.md), [28](../handbook/28-dsa-behind-ai.md): hashmaps, heaps, similarity search | 2 weeks |
| E | Give a model tools and let it act (MCP, agents) | Handbook [22](../handbook/22-graphs.md), [28](../handbook/28-dsa-behind-ai.md): graphs and plans; functions from stage 0 | 2 weeks |
| F | Evaluate, optimise and ship | Handbook [3](../handbook/03-time-complexity.md), [28](../handbook/28-dsa-behind-ai.md): complexity and cost thinking | ongoing |

New to AI? The [AI roadmap for beginners](https://github.com/mayank953/python-ai-crash-course/blob/main/roadmap/README.md) in the Hello Python repo is the gentler starting point.

## How DSA shows up in AI work

| DSA idea | Where you meet it in AI work | Built in the handbook |
|---|---|---|
| Time and space complexity | Latency, memory and the cost of every model call and pipeline step | [3](../handbook/03-time-complexity.md), [4](../handbook/04-space-complexity.md), [28](../handbook/28-dsa-behind-ai.md) |
| Hashmaps and tries | Tokenizers, caches, lookups, deduplication | [18](../handbook/18-hashmaps.md), [28](../handbook/28-dsa-behind-ai.md) |
| Heaps and sorting | Ranking results, top-k answers | [21](../handbook/21-heaps.md), [23](../handbook/23-sorting-compared.md), [28](../handbook/28-dsa-behind-ai.md) |
| Queues | Batching requests, rate limits, background jobs | [17](../handbook/17-queue-and-deque.md), [28](../handbook/28-dsa-behind-ai.md) |
| Stacks and recursion | Call stacks, parsing nested JSON, walking folders | [5](../handbook/05-recursion-from-scratch.md), [16](../handbook/16-stack.md) |
| Trees and graphs | Structured outputs, knowledge graphs, workflows and agent plans | [19](../handbook/19-trees.md), [22](../handbook/22-graphs.md), [28](../handbook/28-dsa-behind-ai.md) |
| Dynamic programming | Edit distance, sequence comparison, reusing earlier results | [25](../handbook/25-dynamic-programming.md), [28](../handbook/28-dsa-behind-ai.md) |

## Pick a plan

| You have | Do this |
|---|---|
| **2 weeks** (an interview is close) | Handbook 3, 5, 6, 9 to 12, 14 to 18, 19; Sets 1 to 3; then daily mixed problems |
| **4 weeks** | Stages 1 to 3 and 5 to 7 at a fast pace, then handbook 27 |
| **12 weeks** (one hour a day) | The plan below |
| **Just curious about AI** | Handbook 1, 3, 18, 21, 22, 28, then the AI path |

### A 12-week plan

| Weeks | Focus |
|---|---|
| 1 | Python basics refresh ([Hello Python](https://github.com/mayank953/python-ai-crash-course)), handbook [1](../handbook/01-what-is-dsa.md), [2](../handbook/02-python-for-dsa.md), complexity [3](../handbook/03-time-complexity.md), [4](../handbook/04-space-complexity.md) |
| 2 | Arrays and hashmaps: handbook [14](../handbook/14-arrays-and-lists.md), [18](../handbook/18-hashmaps.md); AI vocabulary (stage A) |
| 3 to 5 | **Recursion**: handbook [5](../handbook/05-recursion-from-scratch.md), [6](../handbook/06-pmi-and-the-recursion-recipe.md), [7](../handbook/07-fibonacci-and-recursion-trees.md), [8](../handbook/08-head-vs-tail-recursion.md), [9](../handbook/09-recursion-on-arrays.md), [10](../handbook/10-searching-and-sorting-with-recursion.md), [11](../handbook/11-recursion-on-strings.md), [12](../handbook/12-the-choices-tree.md), [13](../handbook/13-backtracking.md), the video, checkpoints and Set 1 |
| 6 | Linked lists, stacks, queues: [15](../handbook/15-linked-list.md), [16](../handbook/16-stack.md), [17](../handbook/17-queue-and-deque.md) and Set 2 |
| 7 | Trees and BST: [19](../handbook/19-trees.md), [20](../handbook/20-binary-search-trees.md) and Set 3 |
| 8 | Heaps and graphs: [21](../handbook/21-heaps.md), [22](../handbook/22-graphs.md) |
| 9 | Sorting and binary search: [23](../handbook/23-sorting-compared.md), [24](../handbook/24-binary-search-beyond.md) |
| 10 to 11 | Dynamic programming and greedy: [25](../handbook/25-dynamic-programming.md), [26](../handbook/26-greedy.md) and Set 4 |
| 12 | Patterns ([27](../handbook/27-patterns-and-interview-playbook.md)), then one small project that uses a data structure and a model call ([28](../handbook/28-dsa-behind-ai.md)) |

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
