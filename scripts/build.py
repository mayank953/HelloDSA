#!/usr/bin/env python3
"""Generate the Hello DSA repository from the original class folders.

    python scripts/build.py \
        --src "/path/to/Hello DSA" \
        --repo /path/to/hello-dsa \
        [--video-url https://www.youtube.com/watch?v=VIDEO_ID]

Requires: pip install -r scripts/requirements.txt
Only generated files are rewritten. `.git` and `scripts/` are never touched.
At the end everything is verified: every source file exists, every shipped code file runs, assignment
solutions pass their checks (and blank starters fail them), notebooks validate, every relative link
and anchor resolves, and chapter timestamps are in order.
"""
import argparse
import contextlib
import hashlib
import io
import linecache
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

import nbformat
import pymupdf
from nbformat import v4

sys.path.insert(0, str(Path(__file__).parent))
import assignments as asg  # noqa: E402
import handbook as hb  # noqa: E402
import handbook_meta as hbm  # noqa: E402
import curriculum as cur  # noqa: E402

REPO_NAME = "HelloDSA"
REPO_URL = f"https://github.com/mayank953/{REPO_NAME}"
PY_REPO = "https://github.com/mayank953/python-ai-crash-course"
HASHTAG = "#HelloDSA"
VIDEO_URL = ""          # set from --video-url (default below)
DEFAULT_VIDEO_URL = "https://www.youtube.com/watch?v=BhaHEnpNujI"
MAX_OUTPUT_CHARS = 20_000
GENERATED = ["recursion", "dsa-topics", "assignments", "roadmap", "handbook", "README.md", "INDEX.md",
             "LICENSE", "CONTRIBUTING.md", ".gitignore", "requirements.txt"]
ICON = {cur.CODE: "💻", cur.TEMPLATE: "🧩", cur.NOTEBOOK: "📓", cur.NOTES: "📄", cur.SOLUTION: "✅"}
LABEL = {cur.CODE: "Code", cur.TEMPLATE: "Starter / assignment", cur.NOTEBOOK: "Notebook",
         cur.NOTES: "Notes (PDF)", cur.SOLUTION: "Solution"}
KERNEL = {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"}
FIXES = {
    "01-introduction-to-recursion/code/01-intro-to-recursion.py": [("def printNumthree(num):1", "def printNumthree(num):")],
    "04-recursion-and-strings/code/09-words-from-a-phone-number.py": [("'6':'ghi'", "'6':'mno'")],
}
PRINT_AS_TEXT = {"trees/code/types-of-binary-tree.py"}
EXPECTED_FAIL = {"01-intro-to-recursion.py"}   # prints until RecursionError on purpose
PDF_INFO = {}


# ------------------------------------------------------------------ helpers
def seconds(ts):
    parts = [int(p) for p in ts.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def vid(ts):
    """Markdown for a timestamp: a link to the video when the URL is known."""
    if not VIDEO_URL:
        return f"`{ts}`"
    sep = "&" if "?" in VIDEO_URL else "?"
    return f"[`{ts}`]({VIDEO_URL}{sep}t={seconds(ts)}s)"


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def gh_slug(title):
    return re.sub(r"[^\w\s-]", "", title.lower()).strip().replace(" ", "-")


def rel(from_dir, to):
    return os.path.relpath(to, from_dir).replace(os.sep, "/")


def clean_dir(root):
    for name in GENERATED:
        p = root / name
        if p.is_dir():
            shutil.rmtree(p)
        elif p.exists():
            p.unlink()


def finalize_nb(nb, seed):
    nb.nbformat, nb.nbformat_minor = 4, 5
    for i, c in enumerate(nb.cells):
        c["id"] = hashlib.md5(f"{seed}:{i}".encode()).hexdigest()[:8]
    nbformat.validate(nb)


def scrub(text):
    return re.sub(r"/Users/[^/\s'\"]+/", "~/", text)


def pdf_meta(path):
    if path not in PDF_INFO:
        d = pymupdf.open(path)
        PDF_INFO[path] = (len(d), os.path.getsize(path) / 1e6)
    return PDF_INFO[path]


def topic_first_ts(topic_key):
    return next(c[0] for c in cur.CHAPTERS if c[2] == topic_key)


# ------------------------------------------------------------------ copying
def copy_notebook(src, dst, banner, notes):
    nb = nbformat.read(src, as_version=4)
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        for out in cell.get("outputs", []):
            if out.get("output_type") == "stream":
                text = "".join(out["text"]) if isinstance(out["text"], list) else out["text"]
                if len(text) > MAX_OUTPUT_CHARS:
                    first = text.splitlines()[0] if text.strip() else ""
                    out["text"] = f"{first}\n... (output shortened: {len(text.splitlines()):,} lines)\n"
                    notes.append(f"shortened an oversized output in {src.name}")
                else:
                    out["text"] = scrub(text)
            elif out.get("output_type") == "error":
                out["traceback"] = [scrub(t) for t in out.get("traceback", [])]
    nb.cells.insert(0, v4.new_markdown_cell(banner))
    dst.parent.mkdir(parents=True, exist_ok=True)
    finalize_nb(nb, str(dst))
    nbformat.write(nb, dst)


def copy_files(owner_folder, files, src_root, out_dir, banner, notes, is_topic=True):
    for f in files:
        src = src_root / f.src
        if not src.exists():
            raise FileNotFoundError(f"missing source: {src}")
        dst = out_dir / f.dest
        dst.parent.mkdir(parents=True, exist_ok=True)
        if f.kind == cur.NOTEBOOK:
            copy_notebook(src, dst, banner(dst), notes)
        elif f.dest.endswith(".py"):
            text = src.read_text(encoding="utf-8")
            for old, new in FIXES.get(f"{owner_folder}/{f.dest}", []):
                assert old in text, f"fix target not found in {src.name}: {old}"
                text = text.replace(old, new)
            if f"{owner_folder}/{f.dest}" in PRINT_AS_TEXT:    # a plain-text diagram saved as .py
                assert '"""' not in text
                text = 'print(r"""' + text.rstrip("\n") + '\n""")\n'
            dst.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(src, dst)
            if dst.suffix == ".pdf":
                pdf_meta(dst)


def topic_banner(topic, topic_dir, home):
    def make(dst):
        lines = []
        if VIDEO_URL:
            lines.append(f"> 📺 **Watch:** {vid(topic_first_ts(topic.key))} {topic.title} (the video chapters start here)")
        lines.append(f"> 📂 **{topic.title}** · [topic page]({rel(dst.parent, topic_dir / 'README.md')}) · "
                     f"[course home]({rel(dst.parent, home / 'README.md')})")
        return "\n".join(lines)
    return make


def subject_banner(subj, subj_dir, home):
    def make(dst):
        return (f"> 📂 **{subj.title}** · [topic page]({rel(dst.parent, subj_dir / 'README.md')}) · "
                f"[course home]({rel(dst.parent, home / 'README.md')})")
    return make


# ------------------------------------------------------------------ tables
def resolve(topic, ref):
    kind, name = ref.split(":", 1)
    for f in topic.files:
        if f.dest.endswith("/" + name) and f.kind in ((cur.CODE, cur.TEMPLATE) if kind == "code" else (cur.NOTES,)):
            return f
    raise KeyError(f"{topic.key}: cannot resolve {ref}")


def file_link(f, base, label=None):
    name = Path(f.dest).name
    return f"[{ICON[f.kind]} `{label or name}`]({base}{f.dest})"


def chapter_table(topics_by_key, base_for):
    rows = ["| Time | Chapter | Code and notes |", "|------|---------|----------------|"]
    for ts, title, key, refs in cur.CHAPTERS:
        t = topics_by_key[key]
        links = " · ".join(file_link(resolve(t, r), base_for(t)) for r in refs) or "—"
        rows.append(f"| {vid(ts)} | {title} | {links} |")
    return "\n".join(rows)


def file_tables(topic, owner_dir, base=""):
    out = []
    code = [f for f in topic.files if f.kind in (cur.CODE, cur.TEMPLATE, cur.SOLUTION)]
    if code:
        out += ["### Code", "", "| File | What it shows |", "|---|---|"]
        out += [f"| {file_link(f, base)} | {f.desc} |" for f in code]
        out.append("")
    notes = [f for f in topic.files if f.kind == cur.NOTES]
    if notes:
        out += ["### Notes (PDF)", "", "| File | Pages | Size | What it is |", "|---|---|---|---|"]
        for f in notes:
            pages, mb = PDF_INFO[owner_dir / f.dest]
            out.append(f"| {file_link(f, base)} | {pages} | {mb:.1f} MB | {f.desc} |")
        out.append("")
    nbs = [f for f in topic.files if f.kind == cur.NOTEBOOK]
    if nbs:
        out += ["### Notebooks", "", "| File | What it is |", "|---|---|"]
        out += [f"| {file_link(f, base)} | {f.desc} |" for f in nbs]
        out.append("")
    return "\n".join(out)


OUT_ROOT = ""


# ------------------------------------------------------------------ topic and subject pages
def topic_page(topic, idx, topics, topics_by_key):
    prev_t = topics[idx - 1] if idx else None
    next_t = topics[idx + 1] if idx + 1 < len(topics) else None
    chs = [c for c in cur.CHAPTERS if c[2] == topic.key]
    L = [f"# {idx + 1}. {topic.title}", "", topic.blurb, ""]
    if VIDEO_URL:
        L += [f"**Video:** starts at {vid(chs[0][0])}", ""]
    L += ["## Chapters", "", "| Time | Chapter | Code and notes |", "|------|---------|----------------|"]
    for ts, title, _k, refs in chs:
        links = " · ".join(file_link(resolve(topic, r), "") for r in refs) or "—"
        L.append(f"| {vid(ts)} | {title} | {links} |")
    L += ["", "## Files", "", file_tables(topic, Path(OUT_ROOT) / "recursion" / topic.folder)]
    L += ["## Try it yourself", ""] + [f"{i}. {t}" for i, t in enumerate(topic.tasks, 1)] + [""]
    a = next(a for a in asg.ASSIGNMENTS if a["after"] == topic.key)
    L += [f"🎯 **Checkpoint:** [{a['title']}](../../assignments/{a['id']}.ipynb) "
          f"(solutions: [here](../../assignments/solutions/{a['id']}.ipynb)).", ""]
    nav = []
    if prev_t:
        nav.append(f"[← {prev_t.title}](../{prev_t.folder}/)")
    nav.append("[Recursion home](../README.md)")
    if next_t:
        nav.append(f"[{next_t.title} →](../{next_t.folder}/)")
    return "\n".join(L + ["---", " · ".join(nav), ""])


def subject_page(subj):
    L = [f"# {subj.title}", "", subj.blurb, ""]
    if subj.prereq:
        L += [f"**Before you start:** {subj.prereq}", ""]
    fake = cur.Topic("x", subj.folder, subj.title, "", subj.files)
    L += [file_tables(fake, Path(OUT_ROOT) / "dsa-topics" / subj.folder)]
    if subj.links:
        L += ["### Useful links", "", "| Link | What it is |", "|---|---|"]
        L += [f"| [{a}]({b}) | {c} |" for a, b, c in subj.links]
        L.append("")
    return "\n".join(L + ["[All DSA topics](../README.md) · [Course home](../../README.md)", ""])


def dsa_topics_readme(counts):
    L = ["# More DSA Topics", "",
         "Code, notebooks and whiteboard notes for the data structures and ideas that sit around recursion. "
         "Each folder has its own page that explains what is inside.", "",
         "| Topic | What's inside | Notebooks and code | PDFs |", "|---|---|---|---|"]
    for s in cur.SUBJECTS:
        n_code = sum(1 for f in s.files if f.kind in (cur.CODE, cur.NOTEBOOK))
        n_pdf = sum(1 for f in s.files if f.kind == cur.NOTES)
        L.append(f"| [{s.title}]({s.folder}/) | {s.blurb} | {n_code} | {n_pdf} |")
    L += ["", "Suggested order: [arrays](arrays/) → [time and space complexity](time-and-space-complexity/) → "
          "[recursion](../recursion/README.md) → [linked list](linked-list/) → [stack](stack/) and [queue](queue/) → "
          "[hashmaps](hashmaps/) → [trees](trees/) → [dynamic programming](dynamic-programming/). "
          "The full plan is in the [roadmap](../roadmap/README.md).", "", "[Course home](../README.md)", ""]
    return "\n".join(L)


# ------------------------------------------------------------------ recursion home
def recursion_readme(topics, topics_by_key, master_pdfs):
    L = ["# Recursion: Complete Code and Notes", "",
         "Everything for the Hello DSA video on recursion: every code file that is shown, the whiteboard notes, "
         "the class notebooks, practice tasks and four checkpoint assignments.", ""]
    if VIDEO_URL:
        L += [f"[Watch the video]({VIDEO_URL}) · jump to any chapter with the timestamp links below.", ""]
    L += ["## The four topics", "", "| # | Topic | Starts at | Code | Notes | Practice |", "|---|---|---|---|---|---|"]
    for i, t in enumerate(topics, 1):
        chs = [c for c in cur.CHAPTERS if c[2] == t.key]
        n_code = sum(1 for f in t.files if f.kind in (cur.CODE, cur.TEMPLATE))
        n_nb = sum(1 for f in t.files if f.kind == cur.NOTEBOOK)
        n_pdf = sum(1 for f in t.files if f.kind == cur.NOTES)
        a = next(a for a in asg.ASSIGNMENTS if a["after"] == t.key)
        L.append(f"| {i} | [{t.title}]({t.folder}/) | {vid(chs[0][0])} | {plural(n_code, 'file')} | "
                 f"{plural(n_pdf, 'PDF')}, {plural(n_nb, 'notebook')} | [checkpoint](../assignments/{a['id']}.ipynb) |")
    L += ["", "## All chapters", "",
          chapter_table(topics_by_key, lambda t: f"{t.folder}/"), "",
          "## Notes that cover the whole series", "",
          "These PDFs are longer sets of recursion notes that run across several topics.", "",
          "| File | Pages | Size | What it is |", "|---|---|---|---|"]
    for f in master_pdfs:
        pages, mb = PDF_INFO[Path(OUT_ROOT) / "recursion" / "notes" / Path(f.dest).name]
        L.append(f"| [📄 `{Path(f.dest).name}`](notes/{Path(f.dest).name}) | {pages} | {mb:.1f} MB | {f.desc} |")
    L += ["", "## Chapter list for the video description", "",
          "[`youtube-chapters.txt`](youtube-chapters.txt) has the same chapters in the format YouTube expects, ready to paste.", "",
          "[Course home](../README.md)", ""]
    return "\n".join(L)


# ------------------------------------------------------------------ assignments
def run_cells(ns, cells, tag="cell"):
    """Run code strings in a shared namespace and register their source so inspect.getsource works."""
    outs = []
    for i, src in enumerate(cells):
        fname = f"<{tag}-{hashlib.md5(src.encode()).hexdigest()[:8]}-{i}>"
        linecache.cache[fname] = (len(src), None, src.splitlines(True), fname)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            exec(compile(src, fname, "exec"), ns)
        outs.append(buf.getvalue())
    return outs


def verify_assignments():
    count = 0
    for a in asg.ASSIGNMENTS + asg.PRACTICE_SETS:
        ns = {}
        run_cells(ns, [a.get("setup", asg.SETUP)], "setup")
        for n, p in enumerate(a["problems"], 1):
            count += 1
            try:
                run_cells(dict(ns), [p["starter"], p["check"]], "starter")
            except BaseException:
                pass
            else:
                raise SystemExit(f"{a['id']} problem {n}: blank starter unexpectedly PASSES its check")
            try:
                run_cells(ns, [p["solution"], p["check"]], "solution")
            except BaseException as exc:
                raise SystemExit(f"{a['id']} problem {n}: solution FAILS its check: {exc!r}")
    return count


def build_assignments(repo):
    a_dir = repo / "assignments"
    s_dir = a_dir / "solutions"
    s_dir.mkdir(parents=True, exist_ok=True)
    for a in asg.ASSIGNMENTS + asg.PRACTICE_SETS:
        setup_code = a.get("setup", asg.SETUP)
        covers = a.get("topic") or a["chapters"]
        for solved in (False, True):
            nb = v4.new_notebook()
            nb.metadata["kernelspec"] = KERNEL
            nb.metadata["language_info"] = {"name": "python"}
            up = "../../" if solved else "../"
            nb.cells.append(v4.new_markdown_cell(
                f"> 📂 **{a['title']}** · [assignments]({'../' if solved else ''}README.md) · [course home]({up}README.md)"))
            body = ("Compare with your own attempt. Try each problem yourself first!" if solved else
                    "Run the setup cell first. Then replace each `...` with your code, run the cell, and run the check cell below it. "
                    "A green tick means you passed. Reference solutions are in the `solutions` folder, but try first.")
            nb.cells.append(v4.new_markdown_cell(
                f"# {a['title']}{' (Solutions)' if solved else ''}\n\n**Covers:** {covers}\n\n{a['intro']}\n\n{body}"))
            ns, counter = {}, 1
            setup = v4.new_code_cell(setup_code)
            if solved:
                run_cells(ns, [setup_code], "setup")
                setup.execution_count = counter
                counter += 1
            nb.cells += [v4.new_markdown_cell("## Setup\n\nRun this cell once. It prepares what the problems and their checks need (for example the `check_recursive` helper or a `Node` class)."), setup]
            for n, p in enumerate(a["problems"], 1):
                nb.cells.append(v4.new_markdown_cell(f"## Problem {n}: {p['title']}\n\n{p['prompt']}"))
                code = p["solution"] if solved else p["starter"]
                check = p["check"] + f"\nprint('✅ Problem {n} passed')"
                cell, chk = v4.new_code_cell(code), v4.new_code_cell(check)
                if solved:
                    for c, out in zip((cell, chk), run_cells(ns, [code, check], "solution")):
                        c.execution_count = counter
                        counter += 1
                        if out:
                            c.outputs = [v4.new_output("stream", name="stdout", text=out)]
                nb.cells += [cell, chk]
            finalize_nb(nb, f"{a['id']}:{solved}")
            nbformat.write(nb, (s_dir if solved else a_dir) / f"{a['id']}.ipynb")
    rows = ["| Checkpoint | After | Problems | Starter | Solutions |", "|---|---|---|---|---|"]
    for a in asg.ASSIGNMENTS:
        rows.append(f"| {a['title'].split(': ', 1)[1]} | [{a['topic']}](../recursion/{next(t.folder for t in cur.TOPICS if t.key == a['after'])}/) | "
                    f"{len(a['problems'])} | [notebook]({a['id']}.ipynb) | [solutions](solutions/{a['id']}.ipynb) |")
    sets = ["| Practice set | Covers | Problems | Starter | Solutions |", "|---|---|---|---|---|"]
    for a in asg.PRACTICE_SETS:
        sets.append(f"| {a['title'].split(': ', 1)[1]} | {a['chapters']} | {len(a['problems'])} | "
                    f"[notebook]({a['id']}.ipynb) | [solutions](solutions/{a['id']}.ipynb) |")
    (a_dir / "README.md").write_text(
        "# Assignments\n\nEvery problem gives you a blank to fill, a check cell that tells you instantly whether you got it right, "
        "and a reference solution in the `solutions` folder. Try first, then compare.\n\n"
        "## Checkpoints: one per recursion topic\n\nThese also check that you really used recursion.\n\n"
        + "\n".join(rows) + "\n\n## Practice sets: the rest of the handbook\n\n"
        + "\n".join(sets) + "\n\n**How to use:** finish the topic or chapter, open the notebook, run the setup cell, solve the problems in order, "
        "and only then look at the solutions.\n\n[Course home](../README.md)\n", encoding="utf-8")


def build_template_solutions(repo, src_root):
    """Fill in the two assignment templates from the video and save them as solutions."""
    topic = cur.TOPICS[0]
    out_dir = repo / "recursion" / topic.folder / "solutions"
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for dest_name, (stub, solution) in asg.TEMPLATE_SOLUTIONS.items():
        f = next(x for x in topic.files if x.dest == f"code/{dest_name}")
        text = (src_root / f.src).read_text(encoding="utf-8")
        assert stub in text, f"stub not found in {f.src}"
        solved = text.replace(stub, solution)
        out = out_dir / dest_name.replace(".py", "-solution.py")
        out.write_text(solved, encoding="utf-8")
        desc = f.desc.replace("Assignment template with test cases. Implement", "A worked solution that implements").replace(" recursively.", " recursively, with the same tests.")
        topic.files.append(cur.F(f.src, f"solutions/{out.name}", cur.SOLUTION, desc))
        made.append(out)
    return made


# ------------------------------------------------------------------ resources
def resources():
    t = {c[1]: c[0] for c in cur.CHAPTERS}
    return [
        ("Hello Python: the Python course", PY_REPO,
         "The free Python course this DSA series builds on. Use it if functions, scope or slicing feel shaky.",
         "Prerequisite", vid("26:19")),
        ("Hello Python: functions", f"{PY_REPO}/tree/main/python/37-intro-to-functions",
         "Lessons 37 to 44 cover defining functions, arguments, scope, lambda, map, filter and reduce.", "Chapters on functions and the call stack", vid("26:19")),
        ("Hello Python: variable scope", f"{PY_REPO}/tree/main/python/41-variable-scope",
         "Local versus global variables. It matters for the global-list approach.", "Collecting answers in a global list", vid("4:58:30")),
        ("Hello Python: slicing", f"{PY_REPO}/tree/main/python/09-concatenation-slicing",
         "Slicing with start, stop and step, used all through the arrays and strings topics.", "Recursion with arrays and strings", vid("2:50:40")),
        ("Python docs: sys.setrecursionlimit", "https://docs.python.org/3/library/sys.html#sys.setrecursionlimit",
         "Why Python stops a runaway recursion and how the limit can be changed.", "Stack memory and stack overflow", vid("1:04:00")),
        ("Tower of Hanoi animation", "https://yongdanielliang.github.io/animation/web/TowerOfHanoi.html",
         "An interactive animation. Pick the number of disks and watch the moves.", "Tower of Hanoi", vid("10:49:58")),
        ("LeetCode: Pow(x, n)", "https://leetcode.com/problems/powx-n/",
         "A harder version of the power assignment (negative exponents, very large inputs).", "Assignments: sum of digits and power", vid("2:43:48")),
        ("LeetCode: Add Digits", "https://leetcode.com/problems/add-digits/",
         "A related digit problem: keep adding the digits until one digit is left.", "Assignments: sum of digits and power", vid("2:43:48")),
        ("Desmos graph of growth rates", "https://www.desmos.com/calculator/l99rykuzx8",
         "Plot O(1), O(log n), O(n), O(n log n) and O(n^2) to see how quickly each one grows.", "Time and space complexity", ""),
        ("Big-O Cheat Sheet", "https://www.bigocheatsheet.com",
         "One-page summary of the complexity of common algorithms and data structures.", "Time and space complexity", ""),
        ("BST animation", "https://yongdanielliang.github.io/animation/web/BST.html",
         "Watch inserts, searches and deletes on a binary search tree step by step.", "Trees", ""),
    ]


def resource_rows():
    rows = ["| Resource | What it is | Use it for | Video |", "|---|---|---|---|"]
    for label, url, what, where, v in resources():
        rows.append(f"| [{label}]({url}) | {what} | {where} | {v} |")
    return "\n".join(rows)



# ------------------------------------------------------------------ the handbook
def build_handbook(repo):
    src_dir = Path(__file__).parent / "handbook_src"
    out = repo / "handbook"
    (out / "code").mkdir(parents=True, exist_ok=True)
    chapters = hbm.HANDBOOK
    stats = {}
    for i, ch in enumerate(chapters):
        text = (src_dir / ch.filename).read_text(encoding="utf-8")
        body, code, st = hb.render_chapter(ch, text)
        stats[ch.num] = st
        head = [f"# {int(ch.num)}. {ch.title}", "",
                f"**{ch.part}** · {ch.level} · about {st['minutes']} minutes to read", "", f"> {ch.blurb}", ""]
        extras = []
        if ch.video and VIDEO_URL:
            extras.append("**In the video:** " + " · ".join(f"{vid(t)} {label}" for t, label in ch.video))
        if ch.related:
            extras.append("**In this repo:** " + " · ".join(f"[{label}](../{path})" for label, path in ch.related))
        extras.append(f"**Run the code from this chapter:** [`code/{ch.num}-{ch.slug}.py`](code/{ch.num}-{ch.slug}.py)")
        nav = []
        if i:
            nav.append(f"[← {int(chapters[i - 1].num)}. {chapters[i - 1].title}]({chapters[i - 1].filename})")
        nav.append("[Handbook contents](README.md)")
        if i + 1 < len(chapters):
            nav.append(f"[{int(chapters[i + 1].num)}. {chapters[i + 1].title} →]({chapters[i + 1].filename})")
        page = "\n".join(head) + "\n".join(f"{e}  " for e in extras) + "\n\n---\n\n" + body.strip() + "\n\n---\n\n" + " · ".join(nav) + "\n"
        (out / ch.filename).write_text(page, encoding="utf-8")
        (out / "code" / f"{ch.num}-{ch.slug}.py").write_text(code, encoding="utf-8")
    (out / "README.md").write_text(handbook_readme(stats), encoding="utf-8")
    return stats


def handbook_table(stats, prefix="handbook/"):
    rows = []
    part = None
    for ch in hbm.HANDBOOK:
        if ch.part != part:
            part = ch.part
            rows += ["", f"### {part}", "", "| # | Chapter | Level | Read | What you will learn |", "|---|---|---|---|---|"]
        rows.append(f"| {int(ch.num)} | [{ch.title}]({prefix}{ch.filename}) | {ch.level} | {stats[ch.num]['minutes']} min | {ch.blurb} |")
    return "\n".join(rows).lstrip("\n")


def handbook_readme(stats):
    total = sum(st["minutes"] for st in stats.values())
    return f"""# The Hello DSA Handbook

**{len(hbm.HANDBOOK)} chapters that take you from "what is a data structure?" to dynamic programming, graphs and the DSA behind AI systems**, written in the style of the video: a story first, then the idea, then the code you can run, then the cost.

About {total // 60} hours of reading, plus the time you spend running and changing the code. Every chapter is self-contained enough to read on its own, but they build on each other in order.

## How every problem is explained

The video's habit is: *do not run after the answer; build the understanding first.* So each worked problem follows the same path:

1. **The question**, in plain words, with examples.
2. **A story** you can picture (a mirror, a teacher's diary, a wedding buffet, a pile of plates).
3. **The smaller problem**, then **assume it works**, then **do your part** (the Hello DSA Method, [chapter 1](01-what-is-dsa.md)).
4. **The base case** and the edge cases.
5. **A trace or a drawn tree**, so you can see it run.
6. **The code**, which you can run: its **output is generated by really running it** when this repo is built, so nothing here is hand-typed or out of date.
7. **The cost**: time and space, counted rather than guessed.
8. **Common mistakes** and **practice problems** with hints.

## Contents

{handbook_table(stats, prefix="")}

## Choose your path

| If you are... | Read |
|---|---|
| **Following the video** | Chapters 5 to 13 (each lists the matching timestamps), then 3 and 4 |
| **New to DSA** | In order: 1 to 4, then 5 to 11, then 14 to 18 |
| **Preparing for interviews** | 3, 5 to 7, 9 to 13, 14 to 22, then 23 to 27 |
| **Struggling with recursion** | 2, 5, 6, 7, 8, then 9 and 11; draw every trace on paper |
| **Heading into dynamic programming** | 7, 12, 13, then 25 (and 26 to compare with greedy) |
| **Curious about AI** | 3, 18, 21, 22, then 28 |

## Run the code yourself

Every chapter has a runnable file in [`code/`](code/). It contains all the code of that chapter, in order:

```bash
python3 handbook/code/07-fibonacci-and-recursion-trees.py
```

The code uses only the Python standard library (3.9 or newer).

## Test yourself

After a chapter, try its practice problems, then the auto-checked notebooks in [`../assignments/`](../assignments/README.md): four recursion checkpoints and four practice sets covering backtracking, search, linked lists, stacks, queues, trees, heaps, graphs, dynamic programming and greedy algorithms.

[Course home](../README.md) · [Roadmap](../roadmap/README.md)
"""


# ------------------------------------------------------------------ roadmap
def roadmap_readme():
    def hl(*nums):
        return ", ".join(f"[{int(n)}](../handbook/{hbm.BY_NUM[n].filename})" for n in nums)

    ac = f"{PY_REPO}/tree/main/ai-concepts"
    return f"""# DSA + AI Roadmap

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
- **You build better AI products.** Search, caching, queues and trees sit underneath retrieval, agents and pipelines ([handbook chapter 28](../handbook/{hbm.BY_NUM["28"].filename})).

## The two paths at a glance

| Path | Goal | You will finish with |
|---|---|---|
| **DSA path** (stages 0 to 11) | Think and code like a problem solver | Recursion, complexity, every core structure, sorting, DP, greedy, patterns |
| **AI path** (stages A to F) | Understand and build with AI | The AI vocabulary, prompting, and small AI projects |

Do them side by side if you like: a few DSA problems a day plus one AI idea a week.

## DSA path

| Stage | Goal | Read | Code, notes and video | Practice | Pace* |
|---|---|---|---|---|---|
| 0 | Python basics | [Hello Python]({PY_REPO}) | Functions, scope and slicing lessons | Its checkpoints | 2 to 4 weeks |
| 1 | The DSA mindset, Python for DSA, arrays | Handbook {hl("01", "02", "14")} | Video {vid('2:21')} to {vid('24:38')}, [arrays](../dsa-topics/arrays/) | Chapter practice | 1 week |
| 2 | Time and space complexity | Handbook {hl("03", "04")} | [Complexity notes and notebooks](../dsa-topics/time-and-space-complexity/) | Count steps yourself | 1 week |
| 3 | **Recursion** (the video) | Handbook {hl("05", "06", "07", "08", "09", "10", "11", "12", "13")} | [Introduction](../recursion/01-introduction-to-recursion/), [arrays](../recursion/02-recursion-and-arrays/), [searching and sorting](../recursion/03-searching-and-sorting/), [strings](../recursion/04-recursion-and-strings/) | [Checkpoints](../assignments/README.md), [Set 1](../assignments/B1-backtracking-and-search.ipynb) | 3 to 4 weeks |
| 4 | Linked lists | Handbook {hl("15")} | [Linked list](../dsa-topics/linked-list/) | [Set 2](../assignments/B2-lists-stacks-queues.ipynb) | 1 week |
| 5 | Stacks and queues | Handbook {hl("16", "17")} | [Stack](../dsa-topics/stack/), [queue](../dsa-topics/queue/) | Set 2 | 1 week |
| 6 | Hashmaps | Handbook {hl("18")} | [Hashmaps](../dsa-topics/hashmaps/) | [Set 3](../assignments/B3-hashmaps-trees-heaps.ipynb) | 1 week |
| 7 | Trees and binary search trees | Handbook {hl("19", "20")} | [Trees](../dsa-topics/trees/) | Set 3 | 2 weeks |
| 8 | Heaps and graphs | Handbook {hl("21", "22")} | The BFS and DFS ideas from stack and queue | Sets 3 and [4](../assignments/B4-graphs-dp-greedy.ipynb) | 2 weeks |
| 9 | Sorting and binary search in depth | Handbook {hl("23", "24")} | [Merge sort and quick sort code](../recursion/03-searching-and-sorting/) | Set 1 | 1 week |
| 10 | Dynamic programming and greedy | Handbook {hl("25", "26")} | [DP starter](../dsa-topics/dynamic-programming/) | Set 4 | 3 weeks |
| 11 | Patterns and interviews | Handbook {hl("27")} | The whole repository | Daily problems on a coding site | ongoing |

\\*A suggestion for about an hour of study a day. Finishing matters more than speed.

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
| A | The language of AI (LLM, tokens, RAG, MCP, agents) | [AI concepts]({ac}) | 3 to 5 days |
| B | Use AI well: prompting and context | The prompting and context sections in the AI concepts guide | ongoing |
| C | Call a model from Python | A provider's official documentation, plus your Python basics | 1 week |
| D | Give a model your own documents (RAG) | Handbook {hl("18", "21", "28")}: hashmaps, heaps, similarity search | 2 weeks |
| E | Give a model tools and let it act (MCP, agents) | Handbook {hl("22", "28")}: graphs and plans; functions from stage 0 | 2 weeks |
| F | Evaluate, optimise and ship | Handbook {hl("03", "28")}: complexity and cost thinking | ongoing |

New to AI? The [AI roadmap for beginners]({PY_REPO}/blob/main/roadmap/README.md) in the Hello Python repo is the gentler starting point.

## How DSA shows up in AI work

| DSA idea | Where you meet it in AI work | Built in the handbook |
|---|---|---|
| Time and space complexity | Latency, memory and the cost of every model call and pipeline step | {hl("03", "04", "28")} |
| Hashmaps and tries | Tokenizers, caches, lookups, deduplication | {hl("18", "28")} |
| Heaps and sorting | Ranking results, top-k answers | {hl("21", "23", "28")} |
| Queues | Batching requests, rate limits, background jobs | {hl("17", "28")} |
| Stacks and recursion | Call stacks, parsing nested JSON, walking folders | {hl("05", "16")} |
| Trees and graphs | Structured outputs, knowledge graphs, workflows and agent plans | {hl("19", "22", "28")} |
| Dynamic programming | Edit distance, sequence comparison, reusing earlier results | {hl("25", "28")} |

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
| 1 | Python basics refresh ([Hello Python]({PY_REPO})), handbook {hl("01", "02")}, complexity {hl("03", "04")} |
| 2 | Arrays and hashmaps: handbook {hl("14", "18")}; AI vocabulary (stage A) |
| 3 to 5 | **Recursion**: handbook {hl("05", "06", "07", "08", "09", "10", "11", "12", "13")}, the video, checkpoints and Set 1 |
| 6 | Linked lists, stacks, queues: {hl("15", "16", "17")} and Set 2 |
| 7 | Trees and BST: {hl("19", "20")} and Set 3 |
| 8 | Heaps and graphs: {hl("21", "22")} |
| 9 | Sorting and binary search: {hl("23", "24")} |
| 10 to 11 | Dynamic programming and greedy: {hl("25", "26")} and Set 4 |
| 12 | Patterns ({hl("27")}), then one small project that uses a data structure and a model call ({hl("28")}) |

## Habits that make it work

- **Type the code.** Reading is not practising.
- **Draw before you code**: trees, stacks and pointers on paper first.
- **Do a few problems a day** instead of many on one day.
- **Keep an error log**: the bug, the cause, the fix.
- **Use AI as a tutor, not an answer machine**: ask it to quiz you or explain an error before asking for the answer.
- **Share your progress** with the hashtag {HASHTAG}.

## Common mistakes

- Memorising solutions instead of the pattern behind them.
- Skipping complexity and then not knowing why a solution is slow.
- Jumping to dynamic programming before recursion feels natural.
- Ignoring edge cases: empty input, one element, duplicates, negative numbers.

[Back to the course home](../README.md)
"""


# ------------------------------------------------------------------ main README, index, misc
def topic_rows():
    rows = ["| # | Topic | Starts at | What you get |", "|---|---|---|---|"]
    for i, t in enumerate(cur.TOPICS, 1):
        chs = [c for c in cur.CHAPTERS if c[2] == t.key]
        n_code = sum(1 for f in t.files if f.kind in (cur.CODE, cur.TEMPLATE))
        n_pdf = sum(1 for f in t.files if f.kind == cur.NOTES)
        n_nb = sum(1 for f in t.files if f.kind == cur.NOTEBOOK)
        rows.append(f"| {i} | [{t.title}](recursion/{t.folder}/) | {vid(chs[0][0])} | "
                    f"{plural(n_code, 'code file')}, {plural(n_pdf, 'PDF')}, {plural(n_nb, 'notebook')}, a checkpoint |")
    return "\n".join(rows)


def assignment_rows():
    rows = ["| Checkpoint | After | Problems | Starter | Solutions |", "|---|---|---|---|---|"]
    for a in asg.ASSIGNMENTS:
        rows.append(f"| {a['title'].split(': ', 1)[1]} | {a['topic']} | {len(a['problems'])} | "
                    f"[notebook](assignments/{a['id']}.ipynb) | [solutions](assignments/solutions/{a['id']}.ipynb) |")
    return "\n".join(rows)


def subject_rows():
    rows = ["| Topic | What's inside | Files |", "|---|---|---|"]
    for s in cur.SUBJECTS:
        n = sum(1 for f in s.files if f.kind != cur.NOTES)
        p = sum(1 for f in s.files if f.kind == cur.NOTES)
        rows.append(f"| [{s.title}](dsa-topics/{s.folder}/) | {s.blurb} | {plural(n, 'code file or notebook')}, {plural(p, 'PDF')} |")
    return "\n".join(rows)


def practice_rows():
    rows = ["| Practice set | Covers | Problems | Starter | Solutions |", "|---|---|---|---|---|"]
    for a in asg.PRACTICE_SETS:
        rows.append(f"| {a['title'].split(': ', 1)[1]} | {a['chapters']} | {len(a['problems'])} | "
                    f"[notebook](assignments/{a['id']}.ipynb) | [solutions](assignments/solutions/{a['id']}.ipynb) |")
    return "\n".join(rows)


def main_readme(topics_by_key, n_files, n_pdf, hb_stats):
    thumb_url = ""
    watch_badge = ""
    watch_block = ""
    start_video = "1. **Watch** the video and use the timestamps in the [chapter table](#chapter-overview) to jump around."
    if VIDEO_URL:
        vid_id = re.search(r"v=([\w-]+)", VIDEO_URL).group(1)
        thumb_url = f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
        watch_badge = f"[![Watch on YouTube](https://img.shields.io/badge/YouTube-Watch%20the%20video-red?logo=youtube&logoColor=white)]({VIDEO_URL})\n"
        watch_block = f"[![Hello DSA video]({thumb_url})]({VIDEO_URL})\n"
    chapters = chapter_table(topics_by_key, lambda t: f"recursion/{t.folder}/")
    return f"""# Hello DSA

{watch_badge}![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**Master Data Structures and Algorithms the visual way.** A complete **28-chapter handbook** (recursion to dynamic programming, graphs and the DSA
behind AI), the full code and whiteboard notes from the **Hello DSA** video, auto-checked practice, and a DSA + AI roadmap.
Share your progress with **{HASHTAG}**.

> 👋 **Coming from the video?** Every chapter of the video links to its code file and notes in the [chapter table](#chapter-overview),
> and the [recursion folder](recursion/README.md) has everything from the video in one place.
>
> 📘 **Want to go deeper than the video?** The [Hello DSA Handbook](handbook/README.md) explains every topic in the same story-first style, with runnable code.
>
> 🧭 **New to all of this?** Follow the [DSA + AI roadmap](roadmap/README.md).

{watch_block}
## Contents

- [Start here](#start-here) · [Set up](#set-up) · [Prerequisite](#prerequisite-python)
- [The Hello DSA Handbook](#the-hello-dsa-handbook)
- [What the video covers](#what-the-video-covers) · [Chapter overview](#chapter-overview)
- [Recursion: complete code and notes](#recursion-complete-code-and-notes) · [Checkpoint assignments](#checkpoint-assignments)
- [More DSA topics](#more-dsa-topics) · [DSA + AI roadmap](roadmap/README.md)
- [Resources explained](#resources-explained) · [Where to find everything](#where-to-find-everything)
- [Repository layout](#repository-layout) · [FAQ](#faq)

## Start here

{start_video}
2. **Read the matching [handbook](handbook/README.md) chapter** for the full explanation (each chapter lists the video timestamps it covers).
3. **Open the topic folder** for the part you are watching. Each one has the code, the notes (PDF) and a page that lists them by chapter.
4. **Run the code yourself**, change it, and break it on purpose.
5. **Test yourself** with the [assignments](assignments/README.md), then compare with the solutions.
6. **Plan what comes next** with the [roadmap](roadmap/README.md).

## Set up

You need Python 3.9 or newer. The recursion code uses only the standard library, so you can run a file with one command:

```bash
git clone {REPO_URL}.git
cd {REPO_NAME}
python3 recursion/01-introduction-to-recursion/code/03-factorial.py
```

For the notebooks and assignments:

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
jupyter lab
```

No install? Download the ZIP (*Code*, then *Download ZIP*) or upload a notebook to [Google Colab](https://colab.research.google.com/).

## Prerequisite: Python

The video assumes you know Python functions, scope and slicing. If any of that is new, the free
[Hello Python course]({PY_REPO}) covers it: [functions]({PY_REPO}/tree/main/python/37-intro-to-functions),
[scope]({PY_REPO}/tree/main/python/41-variable-scope) and [slicing]({PY_REPO}/tree/main/python/09-concatenation-slicing).

## The Hello DSA Handbook

The video teaches recursion in depth. The **handbook** takes the same teaching style across the *whole* subject: foundations, recursion and
backtracking, every core data structure, sorting and searching, dynamic programming, greedy algorithms, an interview playbook, and how it all
shows up inside AI systems. Every code example is executed when this repository is built, so the outputs you read are real.

{handbook_table(hb_stats)}

[Open the handbook](handbook/README.md) for learning paths (following the video, interview preparation, struggling with recursion, and more).

## What the video covers

The video starts with an introduction to data structures and algorithms and then goes deep on recursion in four topics.

{topic_rows()}

## Chapter overview

All {len(cur.CHAPTERS)} chapters, each linked to the code and notes that go with it.

<details>
<summary><b>Show the full chapter table</b></summary>

{chapters}

</details>

## Recursion: complete code and notes

Open a topic to see its chapters, every code file with a description, the PDF notes with page counts, the class notebooks and practice tasks.

{topic_rows()}

The longer notes that run across the whole series are listed on the [recursion page](recursion/README.md#notes-that-cover-the-whole-series).

## Checkpoint assignments

Test yourself at the end of each topic. Every problem has a check cell that tells you instantly whether you got it right, and whether you really used recursion.

{assignment_rows()}

The two assignments from the video (sum of digits and power) have starter files with tests and worked solutions in
[`01-introduction-to-recursion`](recursion/01-introduction-to-recursion/).

### Practice sets for the rest of the handbook

More auto-checked notebooks, one set for each group of chapters:

{practice_rows()}

## More DSA topics

The same notes and code for the topics around recursion, so you can keep going after the video.

{subject_rows()}

See the [DSA topics page](dsa-topics/README.md) for the suggested order, or the [roadmap](roadmap/README.md) for the full plan.

## Resources explained

Links used in the video and the code, and what each one is good for.

{resource_rows()}

> Some of these sites block automated link checkers. If one does not open, search for its title.

## Where to find everything

| You want | Go to |
|---|---|
| A full explanation of a topic, with runnable code | The [handbook](handbook/README.md) |
| The code for a video chapter | The chapter table above, or the topic page in [`recursion/`](recursion/) |
| The whiteboard notes (PDF) | `notes/` inside each topic, or [`recursion/notes/`](recursion/notes/) for the long notes |
| A runnable notebook with outputs | `notebooks/` inside each topic |
| Practice with instant feedback | [`assignments/`](assignments/README.md) |
| Linked list, stack, queue, trees, hashmaps, complexity | [`dsa-topics/`](dsa-topics/README.md) |
| A study plan | [`roadmap/`](roadmap/README.md) |
| Every file and link in one table | [INDEX.md](INDEX.md) |

**Tips:** PDFs open in the browser on GitHub. For long PDFs, download the file for faster scrolling. Notebook and code file names start with a number that follows the video order.

## Repository layout

```
{REPO_NAME}/
├── README.md                 you are here
├── INDEX.md                  every file and link in one table
├── requirements.txt          jupyterlab, numpy, matplotlib
├── handbook/                 28 chapters with runnable code (handbook/code/)
├── roadmap/                  the DSA + AI roadmap
├── recursion/                the video: code, notes, notebooks
│   ├── 01-introduction-to-recursion/   code/ notes/ notebooks/ solutions/
│   ├── 02-recursion-and-arrays/
│   ├── 03-searching-and-sorting/
│   ├── 04-recursion-and-strings/
│   └── notes/                long recursion notes (PDF)
├── assignments/              four checkpoints, four practice sets and solutions
├── dsa-topics/               arrays, complexity, linked list, stack, queue, trees, hashmaps, DP
└── scripts/                  maintainer tooling (learners can ignore)
```

The repository holds {n_files} code files and notebooks and {n_pdf} PDFs.

## FAQ

**How is the handbook different from the video?** The video teaches recursion with live coding; the handbook covers the whole subject in written form with the same story-first approach, and adds backtracking, data structures, graphs, DP, greedy, patterns and DSA for AI. Each chapter says which video timestamps it matches.

**Which file matches the part of the video I am on?** Use the [chapter table](#chapter-overview). It lists the code file and notes for every chapter.

**A starter file fails when I run it.** That is intended: starters and assignment templates have blanks for you to fill. `01-intro-to-recursion.py` ends in a RecursionError on purpose, to show what happens without a stopping condition.

**The PDFs are large.** They are whiteboard notes saved as images. Clone the repository once, or download single files from GitHub.

**Do I need to know recursion before the other DSA topics?** For linked list, trees and dynamic programming, yes. Stack, queue, hashmaps and complexity are friendlier first steps. The [roadmap](roadmap/README.md) shows the order.

**I found a mistake.** Open an [issue]({REPO_URL}/issues) with the file name and what happened.

## Contributing

Corrections and clearer explanations are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Released under the [MIT License](LICENSE). Created by **Mayank Aggarwal**. If this helped you, star the repo and share it with
{HASHTAG}.
"""


def index_page(topics):
    ch_for = {}
    for ts, title, key, refs in cur.CHAPTERS:
        for r in refs:
            ch_for.setdefault((key, r), (ts, title))
    L = ["# Complete index", "", "Every file in the repository and every external link, in one place.", "",
         "## Recursion files", "", "| Topic | File | Type | Video chapter |", "|---|---|---|---|"]
    for t in topics:
        for f in t.files:
            ref = ("notes:" if f.kind == cur.NOTES else "code:") + Path(f.dest).name
            ts_title = ch_for.get((t.key, ref))
            v = f"{vid(ts_title[0])} {ts_title[1]}" if ts_title else ""
            L.append(f"| {t.title} | [{Path(f.dest).name}](recursion/{t.folder}/{f.dest}) | {ICON[f.kind]} {LABEL[f.kind]} | {v} |")
    L += ["", "## Handbook", "", "| # | Chapter | Level | Runnable code |", "|---|---|---|---|"]
    for ch in hbm.HANDBOOK:
        L.append(f"| {int(ch.num)} | [{ch.title}](handbook/{ch.filename}) | {ch.level} | [`{ch.num}-{ch.slug}.py`](handbook/code/{ch.num}-{ch.slug}.py) |")
    L += ["", "## Assignments", "", "| Notebook | Type |", "|---|---|"]
    for a in asg.ASSIGNMENTS + asg.PRACTICE_SETS:
        L.append(f"| [{a['id']}](assignments/{a['id']}.ipynb) | ✏️ Assignment |")
        L.append(f"| [{a['id']} (solutions)](assignments/solutions/{a['id']}.ipynb) | ✅ Solutions |")
    L += ["", "## More DSA topics", "", "| Topic | File | Type |", "|---|---|---|"]
    for s in cur.SUBJECTS:
        for f in s.files:
            L.append(f"| {s.title} | [{Path(f.dest).name}](dsa-topics/{s.folder}/{f.dest}) | {ICON[f.kind]} {LABEL[f.kind]} |")
    L += ["", "## External resources", "", resource_rows(), "", "[Course home](README.md)", ""]
    return "\n".join(L)


LICENSE = """MIT License

Copyright (c) 2026 Mayank Aggarwal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

CONTRIBUTING = """# Contributing

Thanks for helping learners! The most useful contributions are:

- **Typos and wrong explanations** in READMEs or notebooks.
- **Broken links** (please say which page and which link).
- **New practice questions** for a topic, ideally with a short solution.

## How

1. Open an issue that names the file and the chapter (for example "recursion/02: sum of array").
2. For small fixes, open a pull request that changes only the file concerned.
3. Keep code runnable with the standard library only (the complexity notebooks also use numpy and matplotlib).

## A note on the `scripts/` folder

The topic pages, tables, handbook pages and assignment notebooks are produced by `scripts/build.py` from the original class files and from
the Markdown sources in `scripts/handbook_src/`. Code blocks in those sources are executed during the build and their outputs are inserted, so
a handbook edit means editing the source file. This keeps the text, the outputs and the links consistent. If you change a README by
hand, mention it in your pull request and the maintainer will carry the change into the generator.
"""


# ------------------------------------------------------------------ verification
def verify_chapters():
    last = -1
    for ts, title, key, refs in cur.CHAPTERS:
        s = seconds(ts)
        assert s > last, f"chapter out of order: {ts} {title}"
        last = s
    assert seconds(cur.CHAPTERS[0][0]) == 0 and last < 11 * 3600 + 9 * 60 + 23


def run_code_files(repo):
    failures, ran = [], 0
    for p in sorted(repo.rglob("*.py")):
        rp = p.relative_to(repo)
        if "scripts" in rp.parts:
            continue
        in_solutions = "solutions" in rp.parts
        is_starter = any(f.dest == "/".join(rp.parts[2:]) and f.kind == cur.TEMPLATE
                         for t in cur.TOPICS if t.folder == rp.parts[1] for f in t.files) if rp.parts[0] == "recursion" and len(rp.parts) > 2 else False
        if is_starter:
            continue
        ran += 1
        try:
            r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, timeout=120,
                               stdin=subprocess.DEVNULL, cwd=p.parent)
            ok = r.returncode == 0
            if in_solutions:
                ok = ok and "All test cases passed" in r.stdout
        except subprocess.TimeoutExpired:
            ok = False
        if p.name in EXPECTED_FAIL:
            ok = not ok
        if not ok:
            failures.append(str(rp))
    return ran, failures


def verify_links(repo):
    broken, total = [], 0
    for md in repo.rglob("*.md"):
        if "scripts" in md.relative_to(repo).parts:
            continue
        text = md.read_text(encoding="utf-8")
        for m in re.finditer(r"\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
            target = m.group(1)
            if re.match(r"(https?:|mailto:)", target):
                continue
            total += 1
            path_part, _, anchor = target.partition("#")
            dest = md if not path_part else (md.parent / unquote(path_part))
            if not dest.exists():
                broken.append((str(md.relative_to(repo)), target))
            elif anchor and dest.suffix == ".md":
                heads = re.findall(r"^#{1,6} (.+?)\s*$", dest.read_text(encoding="utf-8"), re.M)
                slugs = {gh_slug(re.sub(r"\[(.*?)\]\(.*?\)", r"\1", h)) for h in heads}
                if anchor not in slugs:
                    broken.append((str(md.relative_to(repo)), target))
    for nb_path in repo.rglob("*.ipynb"):
        nb = nbformat.read(nb_path, as_version=4)
        nbformat.validate(nb)
        for m in re.finditer(r"\]\(([^)\s]+)\)", nb.cells[0].source):
            t = m.group(1)
            if t.startswith("http"):
                continue
            total += 1
            if not (nb_path.parent / t).exists():
                broken.append((str(nb_path.relative_to(repo)), t))
    return total, broken


# ------------------------------------------------------------------ main
def build(a):
    global VIDEO_URL, OUT_ROOT
    VIDEO_URL = a.video_url or DEFAULT_VIDEO_URL
    src, repo = Path(a.src), Path(a.repo)
    OUT_ROOT = str(repo)
    repo.mkdir(parents=True, exist_ok=True)
    clean_dir(repo)
    verify_chapters()
    notes = []
    topics = cur.TOPICS
    topics_by_key = {t.key: t for t in topics}

    # copy topic files
    for t in topics:
        t_dir = repo / "recursion" / t.folder
        copy_files(t.folder, t.files, src, t_dir, topic_banner(t, t_dir, repo), notes)
    master_dir = repo / "recursion" / "notes"
    master_dir.mkdir(parents=True, exist_ok=True)
    for f in cur.MASTER_NOTES:
        shutil.copy2(src / f.src, master_dir / f.dest)
        pdf_meta(master_dir / f.dest)
    build_template_solutions(repo, src)
    # subjects
    for s in cur.SUBJECTS:
        s_dir = repo / "dsa-topics" / s.folder
        copy_files(s.folder, s.files, src, s_dir, subject_banner(s, s_dir, repo), notes)
        for f in s.files:
            if f.kind == cur.NOTES:
                pdf_meta(s_dir / f.dest)

    # pages
    for i, t in enumerate(topics):
        (repo / "recursion" / t.folder / "README.md").write_text(topic_page(t, i, topics, topics_by_key), encoding="utf-8")
    (repo / "recursion" / "README.md").write_text(recursion_readme(topics, topics_by_key, cur.MASTER_NOTES), encoding="utf-8")
    for s in cur.SUBJECTS:
        (repo / "dsa-topics" / s.folder / "README.md").write_text(subject_page(s), encoding="utf-8")
    (repo / "dsa-topics" / "README.md").write_text(dsa_topics_readme(None), encoding="utf-8")
    (repo / "recursion" / "youtube-chapters.txt").write_text(
        "\n".join(f"{ts} {title}" for ts, title, _k, _r in cur.CHAPTERS) + "\n", encoding="utf-8")
    (repo / "roadmap").mkdir(exist_ok=True)
    (repo / "roadmap" / "README.md").write_text(roadmap_readme(), encoding="utf-8")

    hb_stats = build_handbook(repo)
    n_problems = verify_assignments()
    build_assignments(repo)

    n_files = sum(1 for p in repo.rglob("*") if p.suffix in (".ipynb", ".py") and "scripts" not in p.relative_to(repo).parts)
    n_pdf = sum(1 for _ in repo.rglob("*.pdf"))
    (repo / "README.md").write_text(main_readme(topics_by_key, n_files, n_pdf, hb_stats), encoding="utf-8")
    (repo / "INDEX.md").write_text(index_page(topics), encoding="utf-8")
    (repo / "LICENSE").write_text(LICENSE, encoding="utf-8")
    (repo / "CONTRIBUTING.md").write_text(CONTRIBUTING, encoding="utf-8")
    (repo / ".gitignore").write_text(".ipynb_checkpoints/\n.DS_Store\nIcon?\n__pycache__/\n.venv/\nvenv/\n*.pyc\n", encoding="utf-8")
    (repo / "requirements.txt").write_text("jupyterlab>=4.0\nnumpy\nmatplotlib\n", encoding="utf-8")

    total, broken = verify_links(repo)
    ran, failures = run_code_files(repo)
    print(f"video chapters: {len(cur.CHAPTERS)} in order; handbook chapters: {len(hb_stats)} (every code block executed, "
          f"{sum(st['ran'] for st in hb_stats.values())} blocks, hidden asserts included)")
    print(f"assignment problems verified (solutions pass, starters fail): {n_problems}")
    print(f"code files executed: {ran}, unexpected failures: {len(failures)}")
    for f in failures:
        print("  FAILED:", f)
    print(f"links checked: {total}, broken: {len(broken)}")
    for b in broken:
        print("  BROKEN:", b)
    for n in dict.fromkeys(notes):
        print(" -", n)
    print(f"code files and notebooks: {n_files}, pdfs: {n_pdf}")
    if broken or failures:
        raise SystemExit(1)


def cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--video-url", default=DEFAULT_VIDEO_URL)
    build(ap.parse_args())


if __name__ == "__main__":
    cli()
