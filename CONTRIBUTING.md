# Contributing

Thanks for helping learners! The most useful contributions are:

- **Typos and wrong explanations** in READMEs or notebooks.
- **Broken links** (please say which page and which link).
- **New practice questions** for a topic, ideally with a short solution.

## How

1. Open an issue that names the file and the chapter (for example "recursion/02: sum of array").
2. For small fixes, open a pull request that changes only the file concerned.
3. Keep code runnable with the standard library only (the complexity notebooks also use numpy and matplotlib).

## A note on the `scripts/` folder

The topic pages, tables and assignment notebooks are produced by `scripts/build.py` from the original class files, so the text
and links stay consistent. If you change a README by hand, mention it in your pull request and the maintainer will carry the
change into the generator.
