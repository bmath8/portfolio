#!/usr/bin/env python3
"""Check the documentation against the repo, not against itself.

Why this exists: the same four figures live in seven files and have drifted
three times (25 -> 26 -> 29 -> 30 agents, 81 -> 157 -> 221 tests) because each
copy was maintained by hand. README.md's "The numbers" is now the single
definition; this catches the copies when they fall behind it.

Run:  python3 scripts/check_docs.py     (exit 1 if anything is stale)

Deliberately exempt, because a naive scan flags all of these wrongly:

  * historical records - docs/CHANGELOG-v7.md, docs/archive/**, "Done" entries.
    A changelog states what was true when it shipped. Rewriting it to match
    today destroys the only record of what changed.
  * prose that NAMES the wrong form in order to forbid it, e.g.
    "link to /neural, never /neural.html".
  * paths in other repos or on Brian's machine - facts.py, evidence-bank.md,
    build_strong_resumes.py - referenced on purpose.
  * runtime URLs the host serves, e.g. /_vercel/insights/script.js.
  * files named as removed, e.g. "the old password gate (middleware.js)".

WHAT THIS DOES NOT CHECK, deliberately:

  Broken file references. A first attempt flagged 35, and every single one was
  a false positive - paths in other repos, runtime URLs the host serves, files
  correctly described as deleted, and prose whose whole point is that a file
  does NOT exist ("option-1-mission-control.html was never committed"). A check
  that cries wolf 35 times out of 35 trains you to ignore it, so it is not here.
  If you add one, it needs the same exemption discipline as the rules above.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS  = {".git", ".claude", "node_modules"}
HISTORICAL = ("docs/archive/", "docs/CHANGELOG-", "docs/plans/", "docs/specs/",
              "docs/AUDIT-")
EXTERNAL = {"facts.py", "evidence-bank.md", "build_strong_resumes.py",
            "render_pdfs.py", "build_variants.py", "render_variants.py",
            "test_guardrails.py", "middleware.js", "ESCALATION_PACKET.md",
            "demo-bar.js", "MASTER_PROJECT_INVENTORY.md", "RATE_LIMITING.md",
            "REDIS_RATE_LIMIT_MIGRATION.md", "script.js"}

def truth():
    agents = len(json.loads((ROOT / "agents.json").read_text()))
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    tests = re.search(r'data-n="(\d+)"[^>]*>[\s\S]{0,200}?tests|(\d+) tests', page)
    tests = int(re.search(r'(\d+) tests', page).group(1))
    return agents, tests

def docs():
    for p in sorted(ROOT.rglob("*.md")):
        if SKIP_DIRS & set(p.parts):            continue
        rel = str(p.relative_to(ROOT))
        if rel.startswith(HISTORICAL):          continue
        yield p, rel

def declared():
    """The figures README.md's table declares. That table is the definition, so
    it is the first thing that has to be right - an earlier version of this
    checker only scanned the prose form "N agents" and sailed straight past a
    wrong number in the table itself. Caught by deliberately corrupting the
    table and watching the checker pass."""
    t = (ROOT / "README.md").read_text(encoding="utf-8")
    out = {}
    for label, key in (("Agents", "agents"), ("Tests", "tests")):
        m = re.search(rf"^\|\s*{label}\s*\|\s*\*\*(\d+)\*\*", t, re.M)
        if m:
            out[key] = int(m.group(1))
    return out

def main():
    agents, tests = truth()
    print(f"repo truth: {agents} agents (agents.json), {tests} tests (index.html)\n")
    bad = []

    # 1. the definition itself
    d = declared()
    if d.get("agents") is None or d.get("tests") is None:
        bad.append('README.md: "The numbers" table is missing or unparseable — '
                   "that table is the single definition; without it nothing else can be checked")
    else:
        if d["agents"] != agents:
            bad.append(f"README.md: the numbers table declares {d['agents']} agents, "
                       f"agents.json has {agents}")
        if d["tests"] != tests:
            bad.append(f"README.md: the numbers table declares {d['tests']} tests, "
                       f"index.html says {tests}")
    for p, rel in docs():
        for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
            # Prose that FORBIDS a form, or NARRATES a transition, legitimately
            # names the stale value. An arrow or "superseded" is the general
            # signal for the second case; without this the checker flags the
            # very sentences that explain why a number changed.
            if re.search(r'\bnever\b|\bnot\b\s+`?/neural\.html|\bold\b|\bremoved\b'
                         r'|drifted|quoted|superseded|->|→', line):
                continue
            for m in re.finditer(r'\b(\d{1,3})\s+(?:scheduled\s+)?agents\b', line):
                if m.group(1) != str(agents):
                    bad.append(f"{rel}:{i}: '{m.group(0)}' but agents.json has {agents}")
            for m in re.finditer(r'\b(\d{1,3})\s*/\s*(\d{1,3})\s+tests|\b(\d{1,3})\s+tests\b', line):
                got = m.group(1) or m.group(3)
                if got and got != str(tests):
                    bad.append(f"{rel}:{i}: '{m.group(0).strip()}' but the page says {tests}")
            if re.search(r'127\.0\.0\.1|localhost', line):
                continue                        # local static server has no cleanUrls
            if re.search(r'https?://[^\s`]*?/neural\.html|\]\(/neural\.html', line):
                bad.append(f"{rel}:{i}: production URL should be /neural (cleanUrls)")
    if bad:
        print("STALE:")
        for b in bad: print("  ✗", b)
        print(f"\n{len(bad)} issue(s). Fix README.md's \"The numbers\" first, then the copies.")
        return 1
    print("clean — every doc agrees with the repo")
    return 0

if __name__ == "__main__":
    sys.exit(main())
