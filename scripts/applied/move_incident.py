import io, re
for path in (r"C:\Brian\02_Projects\portfolio\index.html", r"C:\Brian\02_Projects\portfolio\neural.html"):
    s = io.open(path, encoding="utf-8").read()
    m = re.search(r'\n\s*<div class="incident">.*?</div>\n(?=\s*</div>|\s*<)', s, re.S)
    if not m:
        print(path, "no incident block found"); continue
    block = m.group(0)
    s = s.replace(block, "\n", 1)
    # re-insert after the first project article closes, as a full-width sibling
    i = s.index("</article>") + len("</article>")
    s = s[:i] + "\n" + block.strip() + "\n" + s[i:]
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "incident moved to full width")
