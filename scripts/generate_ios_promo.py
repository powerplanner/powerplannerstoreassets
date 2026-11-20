import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from .common import (
    INPUT_DIR,
    OUTPUT_DIR,
    FONT_EXTRABOLD,
    FONT_BOLD,
    FONT_MEDIUM,
    get_font,
    make_background,
    add_drop_shadow,
    build_phone_mockup,
    build_macbook_mockup,
)

SRC_IPHONE = os.path.join(INPUT_DIR, "iphone", "1.Calendar.png")
SRC_MAC = os.path.join(INPUT_DIR, "mac", "1.Calendar.png")
OUT_PROMO = os.path.join(OUTPUT_DIR, "ios_promo")


def draw_unique_icon(d, icon_type, bx, by, bs):
    cx, cy = bx + bs // 2, by + bs // 2
    w = 7
    white = (255, 255, 255, 255)
    if icon_type == "calendar":
        d.rounded_rectangle([bx + 26, by + 30, bx + 94, by + 94], radius=12, outline=white, width=w)
        d.line([(bx + 26, by + 48), (bx + 94, by + 48)], fill=white, width=w)
        d.line([(bx + 44, by + 20), (bx + 44, by + 34)], fill=white, width=w)
        d.line([(bx + 76, by + 20), (bx + 76, by + 34)], fill=white, width=w)
        for dx in (42, 60, 78):
            for dy in (63, 79):
                d.ellipse([bx + dx - 4, by + dy - 4, bx + dx + 4, by + dy + 4], fill=white)
    elif icon_type == "schedule":
        d.ellipse([bx + 24, by + 24, bx + 96, by + 96], outline=white, width=w)
        d.line([(cx, cy - 20), (cx, cy), (cx + 16, cy + 12)], fill=white, width=w, joint="curve")
    elif icon_type == "grades":
        d.rounded_rectangle([bx + 28, by + 64, bx + 42, by + 92], radius=4, fill=white)
        d.rounded_rectangle([bx + 53, by + 46, bx + 67, by + 92], radius=4, fill=white)
        d.rounded_rectangle([bx + 78, by + 28, bx + 92, by + 92], radius=4, fill=white)
    elif icon_type == "sync":
        d.arc([bx + 26, by + 26, bx + 94, by + 94], start=205, end=350, fill=white, width=w)
        d.arc([bx + 26, by + 26, bx + 94, by + 94], start=25, end=170, fill=white, width=w)
        d.polygon([(bx + 95, by + 54), (bx + 82, by + 42), (bx + 99, by + 36)], fill=white)
        d.polygon([(bx + 25, by + 66), (bx + 38, by + 78), (bx + 21, by + 84)], fill=white)


def render_header_asset():
    W, H = 3840, 1646
    canvas = make_background(W, H, (22, 30, 78), (10, 14, 38), (76, 110, 245), (56, 189, 248), 0.68, 0.50)

    f_head = get_font(FONT_EXTRABOLD, 136)
    f_sub = get_font(FONT_MEDIUM, 46)

    text_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tsd = ImageDraw.Draw(text_shadow)
    text_main = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmd = ImageDraw.Draw(text_main)

    tx, hy = 640, 560
    for line in ["The ultimate", "homework planner"]:
        tsd.text((tx, hy + 8), line, font=f_head, fill=(0, 0, 0, 115))
        tmd.text((tx, hy), line, font=f_head, fill=(255, 255, 255, 255))
        hy += 150

    text_shadow = text_shadow.filter(ImageFilter.GaussianBlur(12))
    canvas = Image.alpha_composite(canvas, text_shadow)
    canvas = Image.alpha_composite(canvas, text_main)

    sub_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sub_layer)
    sd.text((tx, 905), "Calendar  •  Schedule  •  Grades & GPA  •  Online Sync", font=f_sub, fill=(214, 226, 255, 232))
    canvas = Image.alpha_composite(canvas, sub_layer)

    phone, pw, ph = build_phone_mockup(SRC_IPHONE, scr_w=780, scr_h=1696)
    canvas = add_drop_shadow(canvas, phone, (2320, 190), (-16, 32), 48, 200)

    out_path = os.path.join(OUT_PROMO, "iOS_Header_Asset_3840x1646.png")
    canvas.convert("RGB").save(out_path, format="PNG", optimize=True)
    print(f"[Promo] Saved {out_path}")


def draw_feature_cards(canvas, start_x, bottom_y):
    W, H = canvas.size
    f_title = get_font(FONT_BOLD, 90)

    features = [
        ("Calendar & Agenda", (56, 189, 248), "calendar"),
        ("Weekly Class Schedule", (16, 185, 129), "schedule"),
        ("Grades & GPA Calculator", (167, 139, 250), "grades"),
        ("Cross-Platform Sync", (99, 102, 241), "sync"),
    ]

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    card_w, card_h, gap = 1600, 248, 54
    total_h = len(features) * card_h + (len(features) - 1) * gap
    start_y = bottom_y - total_h

    for idx, (title, accent, icon_type) in enumerate(features):
        cy = start_y + idx * (card_h + gap)
        d.rounded_rectangle(
            [start_x, cy, start_x + card_w, cy + card_h],
            radius=44,
            fill=(14, 20, 56, 205),
            outline=(255, 255, 255, 72),
            width=3,
        )
        bx, by = start_x + 44, cy + (card_h - 128) // 2
        bs = 128
        d.rounded_rectangle([bx, by, bx + bs, by + bs], radius=32, fill=(*accent, 245))
        draw_unique_icon(d, icon_type, bx + 4, by + 4, 120)

        bbox = d.textbbox((0, 0), title, font=f_title)
        th = bbox[3] - bbox[1]
        ty = cy + (card_h - th) // 2 - bbox[1]
        d.text((bx + bs + 44, ty), title, font=f_title, fill=(255, 255, 255, 255))

    return Image.alpha_composite(canvas, layer)


def render_search_result_asset():
    W, H = 3840, 2560
    canvas = make_background(W, H, (22, 30, 78), (10, 14, 38), (76, 110, 245), (56, 189, 248), 0.68, 0.50)

    macbook, mw, mh = build_macbook_mockup(SRC_MAC, scr_w=1780, scr_h=1171)
    canvas = add_drop_shadow(canvas, macbook, (1360, 190), (0, 36), 52, 200)

    x_grid = np.linspace(0.0, W - 1.0, W, dtype=np.float32)[None, :]
    t = np.clip((x_grid - 1220.0) / (2040.0 - 1220.0), 0.0, 1.0)
    scrim_alpha = (225.0 * 0.5 * (1.0 + np.cos(np.pi * t))).astype(np.uint8)
    scrim_arr = np.zeros((H, W, 4), dtype=np.uint8)
    scrim_arr[..., 0] = 16
    scrim_arr[..., 1] = 24
    scrim_arr[..., 2] = 64
    scrim_arr[..., 3] = scrim_alpha
    canvas = Image.alpha_composite(canvas, Image.fromarray(scrim_arr, mode="RGBA"))

    phone, pw, ph = build_phone_mockup(SRC_IPHONE, scr_w=780, scr_h=1696)
    py = 610
    canvas = add_drop_shadow(canvas, phone, (2780, py), (-20, 32), 50, 225)

    f_head = get_font(FONT_EXTRABOLD, 174)
    f_sub = get_font(FONT_MEDIUM, 76)

    text_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tsd = ImageDraw.Draw(text_shadow)
    text_main = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmd = ImageDraw.Draw(text_main)

    lx, hy = 180, 190
    for line in ["The ultimate", "homework", "planner"]:
        tsd.text((lx, hy + 10), line, font=f_head, fill=(0, 0, 0, 135))
        tmd.text((lx, hy), line, font=f_head, fill=(255, 255, 255, 255))
        hy += 186

    text_shadow = text_shadow.filter(ImageFilter.GaussianBlur(14))
    canvas = Image.alpha_composite(canvas, text_shadow)
    canvas = Image.alpha_composite(canvas, text_main)

    sub_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sub_layer)
    sy = 788
    for line in ["Plan classes, track grades,", "and sync everywhere."]:
        sd.text((lx, sy), line, font=f_sub, fill=(224, 234, 255, 245))
        sy += 94
    canvas = Image.alpha_composite(canvas, sub_layer)

    canvas = draw_feature_cards(canvas, start_x=lx, bottom_y=py + ph)

    out_path = os.path.join(OUT_PROMO, "iOS_Search_Result_Asset_3840x2560.png")
    canvas.convert("RGB").save(out_path, format="PNG", optimize=True)
    print(f"[Promo] Saved {out_path}")


def run():
    os.makedirs(OUT_PROMO, exist_ok=True)
    render_header_asset()
    render_search_result_asset()
