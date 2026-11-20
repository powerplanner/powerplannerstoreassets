import os
from PIL import Image, ImageDraw, ImageFilter
from .common import (
    INPUT_DIR,
    OUTPUT_DIR,
    FONT_EXTRABOLD,
    FONT_MEDIUM,
    get_font,
    rounded_mask,
    make_background,
    add_drop_shadow,
    build_phone_mockup,
    build_macbook_mockup,
)

W, H = 2560, 1600
SRC_MAC = os.path.join(INPUT_DIR, "mac")
SRC_IPHONE = os.path.join(INPUT_DIR, "iphone")
OUT_MAC = os.path.join(OUTPUT_DIR, "mac")

SLIDES = [
    {
        "type": "mac_and_phone",
        "src": os.path.join(SRC_MAC, "1.Calendar.png"),
        "phone_src": os.path.join(SRC_IPHONE, "1.Calendar.png"),
        "out": "1_Mac_Calendar_Homework_Planner.png",
        "headline": "The ultimate homework planner",
        "subtitle": "Organize classes, assignments, and exams—with cross-platform online sync across Mac, iPhone, iPad, Android & Web.",
        "bg_top": (22, 30, 78),
        "bg_bot": (10, 14, 38),
        "glow1": (76, 110, 245),
        "glow2": (56, 189, 248),
    },
    {
        "type": "window",
        "src": os.path.join(SRC_MAC, "2.Schedule.png"),
        "out": "2_Mac_Schedule_Manage_Schedule.png",
        "headline": "Manage your class schedule",
        "subtitle": "View class times, buildings, and room numbers across your week.",
        "bg_top": (16, 36, 74),
        "bg_bot": (8, 16, 36),
        "glow1": (12, 166, 120),
        "glow2": (34, 139, 230),
    },
    {
        "type": "window",
        "src": os.path.join(SRC_MAC, "3.Assignments.png"),
        "out": "3_Mac_Agenda_Never_Miss_Deadline.png",
        "headline": "Never miss a deadline",
        "subtitle": "See what's due today, next week, and beyond—color-coded by class.",
        "bg_top": (24, 28, 82),
        "bg_bot": (11, 13, 36),
        "glow1": (121, 80, 242),
        "glow2": (34, 139, 230),
    },
    {
        "type": "window",
        "src": os.path.join(SRC_MAC, "4.Grades.png"),
        "out": "4_Mac_Grades_Track_Grades.png",
        "headline": "Track your grades & test \"What If?\"",
        "subtitle": "See weighted category totals and simulate scores before finals.",
        "bg_top": (20, 32, 76),
        "bg_bot": (9, 14, 36),
        "glow1": (59, 91, 219),
        "glow2": (43, 180, 120),
    },
    {
        "type": "window",
        "src": os.path.join(SRC_MAC, "5.GPA.png"),
        "out": "5_Mac_GPA_Calculate_GPA.png",
        "headline": "Calculate your GPA effortlessly",
        "subtitle": "Automatic semester and cumulative GPA tracking across all your credits.",
        "bg_top": (28, 26, 80),
        "bg_bot": (12, 11, 35),
        "glow1": (112, 72, 232),
        "glow2": (66, 99, 235),
    },
    {
        "type": "window",
        "src": os.path.join(SRC_MAC, "6.DayView.png"),
        "out": "6_Mac_DayView_Plan_Your_Day.png",
        "headline": "Plan every hour of your day",
        "subtitle": "Focus on today's classes, locations, and due items in a dedicated day view.",
        "bg_top": (18, 32, 72),
        "bg_bot": (9, 15, 34),
        "glow1": (16, 152, 173),
        "glow2": (76, 110, 245),
    },
    {
        "type": "mac_widgets",
        "src": os.path.join(SRC_MAC, "3.Assignments.png"),
        "widgets_src": os.path.join(SRC_MAC, "Widgets.png"),
        "out": "7_Mac_Widgets_And_Reminders.png",
        "headline": "Widgets & smart reminders",
        "subtitle": "Get timely reminders for assignments and classes, plus live Desktop widgets.",
        "bg_top": (28, 24, 76),
        "bg_bot": (12, 10, 34),
        "glow1": (132, 94, 247),
        "glow2": (76, 110, 245),
    },
]


def extract_mac_widget_cards(widgets_path):
    im = Image.open(widgets_path).convert("RGBA")
    w, h = im.size
    # Split cleanly into left & right half widget cards regardless of minor dimension changes
    mid = w // 2
    pad_x = int(w * 0.019)
    pad_y = int(h * 0.027)
    gap_half = int(w * 0.012)
    left = im.crop((pad_x, pad_y, mid - gap_half, h - pad_y))
    right = im.crop((mid + gap_half, pad_y, w - pad_x, h - pad_y))
    cards = []
    for card in (left, right):
        cw, ch = card.size
        mask = rounded_mask((cw, ch), radius=22)
        out = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        out.paste(card, (0, 0), mask)
        cards.append(out)
    return cards


def run():
    os.makedirs(OUT_MAC, exist_ok=True)
    f_head = get_font(FONT_EXTRABOLD, 92)

    for slide in SLIDES:
        canvas = make_background(W, H, slide["bg_top"], slide["bg_bot"], slide["glow1"], slide["glow2"], 0.50, 0.56)
        f_sub = get_font(FONT_MEDIUM, 36 if slide["type"] == "mac_and_phone" else 38)

        text_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tsd = ImageDraw.Draw(text_shadow)
        text_main = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmd = ImageDraw.Draw(text_main)

        hy = 76
        lw = tmd.textlength(slide["headline"], font=f_head)
        lx = (W - lw) // 2
        tsd.text((lx, hy + 6), slide["headline"], font=f_head, fill=(0, 0, 0, 110))
        tmd.text((lx, hy), slide["headline"], font=f_head, fill=(255, 255, 255, 255))

        text_shadow = text_shadow.filter(ImageFilter.GaussianBlur(10))
        canvas = Image.alpha_composite(canvas, text_shadow)
        canvas = Image.alpha_composite(canvas, text_main)

        sub_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sub_layer)
        slw = sd.textlength(slide["subtitle"], font=f_sub)
        sd.text(((W - slw) // 2, 196), slide["subtitle"], font=f_sub, fill=(214, 226, 255, 232))
        canvas = Image.alpha_composite(canvas, sub_layer)

        if slide["type"] == "mac_and_phone":
            macbook, mw, mh = build_macbook_mockup(slide["src"], scr_w=1580, scr_h=1040, glow1=slide["glow1"], glow2=slide["glow2"])
            canvas = add_drop_shadow(canvas, macbook, (136, 330), (0, 34), 48, 200)
            phone, pw, ph = build_phone_mockup(slide["phone_src"], scr_w=510, scr_h=1109)
            canvas = add_drop_shadow(canvas, phone, (1878, 384), (-14, 28), 42, 215)
        elif slide["type"] == "window":
            mac_win = Image.open(slide["src"]).convert("RGBA")
            win_scale = 1.68
            mw, mh = int(mac_win.width * win_scale), int(mac_win.height * win_scale)
            mac_win = mac_win.resize((mw, mh), Image.Resampling.LANCZOS)
            canvas.alpha_composite(mac_win, ((W - mw) // 2, 286))
        elif slide["type"] == "mac_widgets":
            mac_win = Image.open(slide["src"]).convert("RGBA")
            win_scale = 1.45
            mw, mh = int(mac_win.width * win_scale), int(mac_win.height * win_scale)
            mac_win = mac_win.resize((mw, mh), Image.Resampling.LANCZOS)
            canvas.alpha_composite(mac_win, (140, 340))

            left_card, right_card = extract_mac_widget_cards(slide["widgets_src"])
            card_scale = 1.60
            for idx, card in enumerate((left_card, right_card)):
                cw, ch = int(card.width * card_scale), int(card.height * card_scale)
                card_r = card.resize((cw, ch), Image.Resampling.LANCZOS)
                canvas = add_drop_shadow(canvas, card_r, (1660, 345 + idx * (ch + 44)), (0, 20), 30, 195)

        out_path = os.path.join(OUT_MAC, slide["out"])
        canvas.convert("RGB").save(out_path, format="PNG", optimize=True)
        print(f"[Mac] Saved {out_path}")
