"""きざみ（docs/schedule）のアイコンを作る。python3 scripts/make_schedule_icons.py"""
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent.parent / "docs" / "schedule" / "icons"
BG = (196, 83, 47)
FG = (255, 255, 255)
SOFT = (255, 255, 255, 150)


def draw(size, safe=1.0, rounded=True):
    s = 4  # 拡大して描いて縮小（輪郭をなめらかにする）
    W = size * s
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, W - 1, W - 1], radius=int(W * 0.22), fill=BG)
    else:
        d.rectangle([0, 0, W, W], fill=BG)
    # 内容は中央の safe 割合に収める
    c = W / 2
    u = W * safe / 512  # 512 基準の単位
    x0 = c - 165 * u
    # 目盛り（縦の線と刻み）
    d.rounded_rectangle([x0, c - 170 * u, x0 + 14 * u, c + 170 * u], radius=7 * u, fill=FG)
    for i in range(9):
        y = c - 160 * u + i * 40 * u
        ln = 44 * u if i % 2 == 0 else 26 * u
        d.rounded_rectangle([x0, y - 5 * u, x0 + ln, y + 5 * u], radius=5 * u, fill=FG)
    # 予定の帯（長さの違う3本）
    bars = [(-130, -60, 230), (-40, -5, 170), (15, 85, 260), (105, 140, 120)]
    for top, bot, ln in bars:
        bx = x0 + 70 * u
        d.rounded_rectangle([bx, c + top * u, bx + ln * u, c + bot * u], radius=12 * u,
                            fill=FG if (bot - top) > 40 else (255, 255, 255, 170))
    return img.resize((size, size), Image.LANCZOS)


OUT.mkdir(parents=True, exist_ok=True)
draw(192).save(OUT / "icon-192.png")
draw(512).save(OUT / "icon-512.png")
draw(512, safe=0.78, rounded=False).save(OUT / "maskable-512.png")
draw(180, rounded=False).convert("RGB").save(OUT / "apple-touch-icon.png")
print("ok")
