import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS_DIR = os.path.join(ROOT_DIR, "fonts")
INPUT_DIR = os.path.join(ROOT_DIR, "input")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

FONT_EXTRABOLD = os.path.join(FONTS_DIR, "InterDisplay-ExtraBold.otf")
FONT_BOLD = os.path.join(FONTS_DIR, "InterDisplay-Bold.otf")
FONT_SEMIBOLD = os.path.join(FONTS_DIR, "Inter-SemiBold.otf")
FONT_MEDIUM = os.path.join(FONTS_DIR, "Inter-Medium.otf")


def get_font(path, size):
    return ImageFont.truetype(path, size)


def rounded_mask(size, radius, scale=2):
    w, h = size
    m = Image.new("L", (w * scale, h * scale), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, w * scale - 1, h * scale - 1], radius=radius * scale, fill=255)
    return m.resize((w, h), Image.Resampling.LANCZOS)


def make_background(w, h, bg_top, bg_bot, glow1, glow2, ring_cx_ratio=0.5, ring_cy_ratio=0.5):
    y = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None]
    x = np.linspace(0.0, 1.0, w, dtype=np.float32)[None, :]

    top = np.array(bg_top, dtype=np.float32)
    bot = np.array(bg_bot, dtype=np.float32)
    base = np.broadcast_to(top * (1.0 - y[..., None]) + bot * y[..., None], (h, w, 3)).copy()

    cx1, cy1 = ring_cx_ratio, ring_cy_ratio
    r1 = np.sqrt(((x - cx1) * (w / h)) ** 2 + (y - cy1) ** 2)
    g1 = np.exp(-(r1 ** 2) / (2 * (0.40 ** 2)))[..., None]
    base += np.array(glow1, dtype=np.float32) * g1 * 0.41

    cx2, cy2 = 0.85, 0.15
    r2 = np.sqrt(((x - cx2) * (w / h)) ** 2 + (y - cy2) ** 2)
    g2 = np.exp(-(r2 ** 2) / (2 * (0.32 ** 2)))[..., None]
    base += np.array(glow2, dtype=np.float32) * g2 * 0.27

    cx3, cy3 = 0.15, 0.86
    r3 = np.sqrt(((x - cx3) * (w / h)) ** 2 + (y - cy3) ** 2)
    g3 = np.exp(-(r3 ** 2) / (2 * (0.34 ** 2)))[..., None]
    base += np.array(glow1, dtype=np.float32) * g3 * 0.22

    arr = np.clip(base, 0, 255).astype(np.uint8)
    img = Image.fromarray(arr, mode="RGB").convert("RGBA")

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    cx = int(w * ring_cx_ratio)
    cy = int(h * ring_cy_ratio)
    r_inner = int(min(w, h) * 0.48)
    r_outer = int(min(w, h) * 0.65)
    od.ellipse([cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner], outline=(255, 255, 255, 14), width=2)
    od.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], outline=(255, 255, 255, 9), width=2)
    return Image.alpha_composite(img, overlay)


def add_drop_shadow(canvas, item, pos, offset=(0, 32), blur=48, alpha_strength=200):
    w, h = canvas.size
    iw, ih = item.size
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    alpha = item.split()[3]
    sil = Image.new("RGBA", (iw, ih), (4, 6, 18, alpha_strength))
    shadow.paste(sil, (pos[0] + offset[0], pos[1] + offset[1]), alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.alpha_composite(item, pos)
    return canvas


def build_phone_mockup(src_path, scr_w=948, scr_h=2061):
    scale_ratio = scr_w / 948.0
    bezel = max(10, round(22 * scale_ratio))
    rim = max(2, round(4 * scale_ratio))
    pad = bezel + rim
    frame_w = scr_w + pad * 2
    frame_h = scr_h + pad * 2
    btn_extra = max(5, round(12 * scale_ratio))
    total_w = frame_w + btn_extra * 2
    total_h = frame_h

    scr = Image.open(src_path).convert("RGBA").resize((scr_w, scr_h), Image.Resampling.LANCZOS)

    s = 2
    di_w = round(236 * scale_ratio)
    di_h = round(66 * scale_ratio)
    di_x = (scr_w - di_w) // 2
    di_y = round(24 * scale_ratio)
    di_band_h = round(120 * scale_ratio)
    di_hi = Image.new("RGBA", (scr_w * s, di_band_h * s), (0, 0, 0, 0))
    dh = ImageDraw.Draw(di_hi)
    dh.rounded_rectangle(
        [di_x * s, di_y * s, (di_x + di_w) * s, (di_y + di_h) * s],
        radius=(di_h // 2) * s,
        fill=(6, 7, 10, 255),
    )
    cam_cx = (di_x + di_w - round(34 * scale_ratio)) * s
    cam_cy = (di_y + di_h // 2) * s
    r_out = max(5, round(14 * scale_ratio))
    r_mid = max(2, round(7 * scale_ratio))
    r_in = max(1, round(3 * scale_ratio))
    dh.ellipse([cam_cx - r_out * s, cam_cy - r_out * s, cam_cx + r_out * s, cam_cy + r_out * s], fill=(18, 22, 34, 255))
    dh.ellipse([cam_cx - r_mid * s, cam_cy - r_mid * s, cam_cx + r_mid * s, cam_cy + r_mid * s], fill=(32, 48, 88, 255))
    dh.ellipse([cam_cx - r_in * s, cam_cy - r_in * s, cam_cx - 1 * s, cam_cy - 1 * s], fill=(120, 160, 255, 180))
    di_lo = di_hi.resize((scr_w, di_band_h), Image.Resampling.LANCZOS)
    scr.alpha_composite(di_lo, (0, 0))

    scr_radius = round(108 * scale_ratio)
    scr_mask = rounded_mask((scr_w, scr_h), radius=scr_radius)
    scr_clipped = Image.new("RGBA", (scr_w, scr_h), (0, 0, 0, 0))
    scr_clipped.paste(scr, (0, 0), scr_mask)

    hi = Image.new("RGBA", (total_w * s, total_h * s), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hi)

    fx0, fy0 = btn_extra * s, 0
    fx1, fy1 = (btn_extra + frame_w) * s - 1, frame_h * s - 1

    btn_color = (72, 82, 104, 255)
    bw = round(7 * scale_ratio)
    hd.rounded_rectangle([fx0 - bw * s, round(310 * scale_ratio) * s, fx0 + 4 * s, round(372 * scale_ratio) * s], radius=3 * s, fill=btn_color)
    hd.rounded_rectangle([fx0 - bw * s, round(425 * scale_ratio) * s, fx0 + 4 * s, round(545 * scale_ratio) * s], radius=3 * s, fill=btn_color)
    hd.rounded_rectangle([fx0 - bw * s, round(575 * scale_ratio) * s, fx0 + 4 * s, round(695 * scale_ratio) * s], radius=3 * s, fill=btn_color)
    hd.rounded_rectangle([fx1 - 4 * s, round(465 * scale_ratio) * s, fx1 + bw * s, round(635 * scale_ratio) * s], radius=3 * s, fill=btn_color)

    outer_r = round(134 * scale_ratio)
    hd.rounded_rectangle([fx0, fy0, fx1, fy1], radius=outer_r * s, fill=(96, 108, 134, 255))
    hd.rounded_rectangle([fx0 + 2 * s, fy0 + 2 * s, fx1 - 2 * s, fy1 - 2 * s], radius=(outer_r - 2) * s, fill=(48, 56, 74, 255))
    hd.rounded_rectangle([fx0 + rim * s, fy0 + rim * s, fx1 - rim * s, fy1 - rim * s], radius=(outer_r - 4) * s, fill=(10, 12, 18, 255))

    phone = hi.resize((total_w, total_h), Image.Resampling.LANCZOS)
    phone.alpha_composite(scr_clipped, (btn_extra + pad, pad))

    glare = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.rounded_rectangle(
        [btn_extra + 2, 2, btn_extra + frame_w - 3, frame_h - 3],
        radius=outer_r - 2,
        outline=(255, 255, 255, 45),
        width=2,
    )
    phone = Image.alpha_composite(phone, glare)
    return phone, total_w, total_h


def build_ipad_mockup(src_path, scr_w=1560, scr_h=2081):
    scale_ratio = scr_w / 1560.0
    bezel = round(34 * scale_ratio)
    rim = round(5 * scale_ratio)
    pad = bezel + rim
    frame_w = scr_w + pad * 2
    frame_h = scr_h + pad * 2

    scr = Image.open(src_path).convert("RGBA").resize((scr_w, scr_h), Image.Resampling.LANCZOS)
    scr_radius = round(42 * scale_ratio)
    scr_mask = rounded_mask((scr_w, scr_h), radius=scr_radius)
    scr_clipped = Image.new("RGBA", (scr_w, scr_h), (0, 0, 0, 0))
    scr_clipped.paste(scr, (0, 0), scr_mask)

    s = 2
    hi = Image.new("RGBA", (frame_w * s, frame_h * s), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hi)
    outer_r = round(74 * scale_ratio)
    hd.rounded_rectangle([0, 0, frame_w * s - 1, frame_h * s - 1], radius=outer_r * s, fill=(92, 104, 130, 255))
    hd.rounded_rectangle([2 * s, 2 * s, frame_w * s - 3, frame_h * s - 3], radius=(outer_r - 2) * s, fill=(46, 54, 72, 255))
    hd.rounded_rectangle([rim * s, rim * s, (frame_w - rim) * s - 1, (frame_h - rim) * s - 1], radius=(outer_r - 5) * s, fill=(10, 12, 18, 255))

    ipad = hi.resize((frame_w, frame_h), Image.Resampling.LANCZOS)
    ipad.alpha_composite(scr_clipped, (pad, pad))

    glare = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glare)
    gd.rounded_rectangle([2, 2, frame_w - 3, frame_h - 3], radius=outer_r - 2, outline=(255, 255, 255, 42), width=2)
    ipad = Image.alpha_composite(ipad, glare)
    return ipad, frame_w, frame_h


def build_macbook_mockup(mac_src_path, scr_w=1580, scr_h=1040, glow1=(76, 110, 245), glow2=(56, 189, 248)):
    bezel = 22
    lid_w = scr_w + bezel * 2
    lid_h = scr_h + bezel * 2
    base_w = int(lid_w * 1.13)
    base_h = 44
    total_w = base_w
    total_h = lid_h + base_h

    y = np.linspace(0.0, 1.0, scr_h, dtype=np.float32)[:, None]
    x = np.linspace(0.0, 1.0, scr_w, dtype=np.float32)[None, :]
    wall = np.zeros((scr_h, scr_w, 3), dtype=np.float32)
    wall += np.array([28, 46, 110], dtype=np.float32) * (1.0 - y[..., None])
    wall += np.array([15, 24, 62], dtype=np.float32) * y[..., None]
    r_glow = np.sqrt((x - 0.78) ** 2 + (y - 0.22) ** 2)
    wall += np.array(glow2, dtype=np.float32) * np.exp(-(r_glow ** 2) / 0.22)[..., None] * 0.42
    r_glow2 = np.sqrt((x - 0.22) ** 2 + (y - 0.78) ** 2)
    wall += np.array(glow1, dtype=np.float32) * np.exp(-(r_glow2 ** 2) / 0.24)[..., None] * 0.30
    desktop = Image.fromarray(np.clip(wall, 0, 255).astype(np.uint8), mode="RGB").convert("RGBA")

    mac_win = Image.open(mac_src_path).convert("RGBA")
    win_scale = (scr_w / 1580.0) * 1.32
    mw = int(mac_win.width * win_scale)
    mh = int(mac_win.height * win_scale)
    mac_win = mac_win.resize((mw, mh), Image.Resampling.LANCZOS)
    wx = (scr_w - mw) // 2 - int(30 * (scr_w / 1580.0))
    wy = (scr_h - mh) // 2 + 10
    desktop.alpha_composite(mac_win, (wx, wy))

    scr_mask = rounded_mask((scr_w, scr_h), radius=22)
    scr_clipped = Image.new("RGBA", (scr_w, scr_h), (0, 0, 0, 0))
    scr_clipped.paste(desktop, (0, 0), scr_mask)

    s = 2
    hi = Image.new("RGBA", (total_w * s, total_h * s), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hi)

    lx0 = ((total_w - lid_w) // 2) * s
    lx1 = lx0 + lid_w * s
    ly0 = 0
    ly1 = lid_h * s

    hd.rounded_rectangle([lx0, ly0, lx1, ly1], radius=40 * s, fill=(76, 84, 104, 255))
    hd.rounded_rectangle([lx0 + 3 * s, ly0 + 3 * s, lx1 - 3 * s, ly1 - 3 * s], radius=37 * s, fill=(14, 16, 22, 255))

    nw, nh = 160 * s, 28 * s
    nx0 = (total_w * s - nw) // 2
    hd.rounded_rectangle([nx0, (bezel - 4) * s, nx0 + nw, (bezel + 24) * s], radius=8 * s, fill=(14, 16, 22, 255))

    by0 = lid_h * s - 6 * s
    by1 = total_h * s
    hd.rounded_rectangle([0, by0, total_w * s, by1], radius=18 * s, fill=(56, 63, 80, 255))
    hd.rectangle([0, by0, total_w * s, by0 + 16 * s], fill=(86, 96, 118, 255))
    tw, th = 220 * s, 14 * s
    tx0 = (total_w * s - tw) // 2
    hd.rounded_rectangle([tx0, by0, tx0 + tw, by0 + th], radius=7 * s, fill=(28, 32, 42, 255))

    macbook = hi.resize((total_w, total_h), Image.Resampling.LANCZOS)
    macbook.alpha_composite(scr_clipped, ((total_w - lid_w) // 2 + bezel, bezel))
    return macbook, total_w, total_h
