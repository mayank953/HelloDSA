"""Render the Hello DSA Handbook from scripts/handbook_src/*.md.

Authoring format
----------------
Source files are plain Markdown. Code fences are special:

    ```python            run it, show it, and insert a real **Output** block after it
    ```python hide       run it but do not show it (hidden asserts that prove the claims in the text)
    ```python no-run     show it only (pseudo-code, or code that would loop forever)
    ```python expect-error   run it, show it, and show the error it raises (for example a RecursionError)

Blocks of one chapter share a namespace, like cells in a notebook, so a function defined in an earlier
block can be used later. Outputs are always produced by the real run, so documentation cannot drift from
the code. The runnable blocks of each chapter are also saved as handbook/code/<chapter>.py.
"""
import contextlib
import hashlib
import io
import linecache
import re
from dataclasses import dataclass, field
from pathlib import Path

FENCE = re.compile(r"^(\s*)(`{3,})(.*)$")
MAX_OUTPUT_LINES = 45


class HandbookError(Exception):
    pass


@dataclass
class Chapter:
    num: str
    slug: str
    title: str
    part: str
    level: str          # Beginner / Intermediate / Advanced
    blurb: str
    video: list = field(default_factory=list)      # [(timestamp, label)]
    related: list = field(default_factory=list)    # [(label, repo-relative path)]

    @property
    def filename(self):
        return f"{self.num}-{self.slug}.md"


def split_blocks(text):
    """Yield ('text', str) and ('code', info, code, fence_indent) pieces in order."""
    lines = text.split("\n")
    i, buf = 0, []
    while i < len(lines):
        m = FENCE.match(lines[i])
        if m:
            if buf:
                yield ("text", "\n".join(buf))
                buf = []
            indent, ticks, info = m.group(1), m.group(2), m.group(3).strip()
            j = i + 1
            body = []
            while j < len(lines) and not re.match(rf"^\s*{ticks}\s*$", lines[j]):
                body.append(lines[j])
                j += 1
            if j >= len(lines):
                raise HandbookError(f"unclosed code fence starting at line {i + 1}")
            yield ("code", info, "\n".join(body), indent, ticks)
            i = j + 1
        else:
            buf.append(lines[i])
            i += 1
    if buf:
        yield ("text", "\n".join(buf))


def run_block(ns, code, tag, expect_error):
    fname = f"<{tag}-{hashlib.md5(code.encode()).hexdigest()[:8]}>"
    linecache.cache[fname] = (len(code), None, code.splitlines(True), fname)
    buf = io.StringIO()
    err = None
    with contextlib.redirect_stdout(buf):
        try:
            exec(compile(code, fname, "exec"), ns)
        except BaseException as exc:     # noqa: BLE001
            err = exc
    if err is not None and not expect_error:
        raise HandbookError(f"{tag}: block raised {err.__class__.__name__}: {err}\n--- code ---\n{code}")
    if err is None and expect_error:
        raise HandbookError(f"{tag}: block was expected to raise but did not\n--- code ---\n{code}")
    return buf.getvalue(), err


def error_line(err):
    if isinstance(err, RecursionError):
        return "RecursionError: maximum recursion depth exceeded"
    msg = str(err).splitlines()[0] if str(err) else ""
    return f"{err.__class__.__name__}: {msg}".rstrip(": ")


def render_chapter(ch, src_text):
    """Return (rendered_markdown, runnable_code_for_py_file, stats)."""
    ns = {"__name__": "__handbook__"}
    out, py, shown, ran = [], [], 0, 0
    for n, piece in enumerate(split_blocks(src_text), 1):
        if piece[0] == "text":
            out.append(piece[1])
            continue
        _kind, info, code, indent, ticks = piece
        parts = info.split()
        lang, flags = (parts[0] if parts else ""), set(parts[1:])
        if lang != "python":
            out.append(f"{indent}{ticks}{info}\n{code}\n{indent}{ticks}")
            continue
        tag = f"{ch.num}-block{n}"
        if "hide" in flags:
            run_block(ns, code, tag, "expect-error" in flags)
            ran += 1
            continue
        fence_open = f"{indent}{ticks}python"
        shown_block = f"{fence_open}\n{code}\n{indent}{ticks}"
        if "no-run" in flags:
            out.append(shown_block)
            shown += 1
            continue
        stdout, err = run_block(ns, code, tag, "expect-error" in flags)
        ran += 1
        shown += 1
        text_out = stdout.rstrip("\n")
        if err is not None:
            text_out = (text_out + "\n" if text_out else "") + error_line(err)
        block = shown_block
        if text_out.strip():
            lines = text_out.split("\n")
            if len(lines) > MAX_OUTPUT_LINES:       # keep the head and the last lines (the error is at the end)
                head = MAX_OUTPUT_LINES - 6
                omitted = len(lines) - head - 3
                lines = lines[:head] + [f"... ({omitted} more lines)"] + lines[-3:]
            block += f"\n\n{indent}**Output**\n\n{indent}{ticks}text\n" + "\n".join(indent + l if l else l for l in lines) + f"\n{indent}{ticks}"
        out.append(block)
        if "expect-error" not in flags:
            py.append(code)
    body = "\n".join(out)
    code_file = (f'"""{ch.num}. {ch.title}\n\nAll runnable code from this chapter of the Hello DSA Handbook, in order.\n'
                 f'Run it with: python {ch.num}-{ch.slug}.py\n"""\n\n' + "\n\n".join(py))
    code_file += "\n\nprint('\\n[all code in this chapter ran successfully]')\n"
    words = len(re.findall(r"\w+", re.sub(r"```.*?```", "", body, flags=re.S)))
    return body, code_file, {"blocks": shown, "ran": ran, "minutes": max(3, round(words / 190))}
