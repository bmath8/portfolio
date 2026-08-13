import io, re
REPO = r"C:\Brian\02_Projects\portfolio"

def fix(path, is_mc):
    s = io.open(path, encoding="utf-8").read()
    # clean any bad escaped insert from the previous run
    s = s.replace('<main id=\\"main\\">', '').replace('</main>', '')
    if '<main id="main">' in s:
        print(path, "already ok"); return
    if is_mc:
        s = s.replace("</header>", "</header>\n<main id=\"main\">", 1)
        s = s.replace('<footer class="foot">', "</main>\n<footer class=\"foot\">", 1)
    else:
        s = s.replace('<div class="aurora"></div>', '<div class="aurora"></div>\n<main id="main">', 1)
        s = s.replace('<footer id="contact">', "</main>\n<footer id=\"contact\">", 1)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "main opened:", '<main id="main">' in s, "closed:", "</main>" in s)

fix(REPO + r"\index.html", True)
fix(REPO + r"\neural.html", False)
