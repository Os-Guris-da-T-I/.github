"""Render SVGs exactly like GitHub does (through <img>) and save PNGs for review."""
import sys, os, pathlib
from playwright.sync_api import sync_playwright

def render(paths, out_dir, wait=3.2, bg="#0d1117", scale=1):
    pathlib.Path(out_dir).mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for path in paths:
            path = os.path.abspath(path)
            pg = b.new_page(viewport={"width": 1240, "height": 300}, device_scale_factor=scale)
            html=os.path.join(out_dir,"_wrap.html")
            open(html,"w").write(f"<body style='margin:20px;background:{bg}'><img id=i src='file://{path}' style='width:1200px;display:block'></body>")
            pg.goto("file://"+os.path.abspath(html))
            pg.wait_for_timeout(int(wait * 1000))
            h = pg.evaluate("document.getElementById('i').getBoundingClientRect().height")
            pg.set_viewport_size({"width": 1240, "height": int(h) + 40})
            pg.screenshot(path=os.path.join(out_dir, os.path.basename(path).replace(".svg", ".png")))
            pg.close()
        b.close()

if __name__ == "__main__":
    render(sys.argv[2:], sys.argv[1], wait=float(os.environ.get("WAIT", 3.2)), bg=os.environ.get("BG", "#0d1117"))
