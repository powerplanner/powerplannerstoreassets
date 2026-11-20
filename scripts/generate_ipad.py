import os
from PIL import Image, ImageDraw, ImageFilter
from .common import (
    INPUT_DIR,
    OUTPUT_DIR,
    FONT_EXTRABOLD,
    FONT_MEDIUM,
    get_font,
    make_background,
    add_drop_shadow,
    build_ipad_mockup,
    build_phone_mockup,
)

W, H = 2048, 2732
SRC_IPAD = os.path.join(INPUT_DIR, "ipad")
SRC_IPHONE = os.path.join(INPUT_DIR, "iphone")
OUT_IPAD = os.path.join(OUTPUT_DIR, "ipad")

SLIDES = [
    {
        "type": "ipad_and_phone",
        "src": os.path.join(SRC_IPAD, "1.Calendar.png"),
        "phone_src": os.path.join(SRC_IPHONE, "1.Calendar.png"),
        "out": "1_iPad_Calendar_Homework_Planner.png",
        "headline": ["The ultimate", "homework planner"],
        "subtitle": ["Organize classes, assignments, and exams—with", "cross-platform online sync across iPad, iPhone, Mac & Web."],
        "bg_top": (22, 30, 78),
        "bg_bot": (10, 14, 38),
        "glow1": (76, 110, 245),
        "glow2": (56, 189, 248),
    },
    {
        "type": "ipad",
        "src": os.path.join(SRC_IPAD, "2.Agenda.png"),
        "out": "2_iPad_Agenda_Never_Miss_Deadline.png",
        "headline": ["Never miss", "a deadline"],
        "subtitle": ["See what's due today, next week, and", "beyond—color-coded by class."],
        "bg_top": (24, 28, 82),
        "bg_bot": (11, 13, 36),
        "glow1": (121, 80, 242),
        "glow2": (34, 139, 230),
    },
    {
        "type": "ipad",
        "src": os.path.join(SRC_IPAD, "3.Schedule.png"),
        "out": "3_iPad_Schedule_Manage_Schedule.png",
        "headline": ["Manage your", "class schedule"],
        "subtitle": ["View class times, buildings, and", "room numbers at a glance."],
        "bg_top": (16, 36, 74),
        "bg_bot": (8, 16, 36),
        "glow1": (12, 166, 120),
        "glow2": (34, 139, 230),
    },
    {
        "type": "ipad",
        "src": os.path.join(SRC_IPAD, "4.Grades.png"),
        "out": "4_iPad_Grades_Track_Grades.png",
        "headline": ["Track your grades", "& test \"What If?\""],
        "subtitle": ["See weighted category totals and", "simulate scores before finals."],
        "bg_top": (20, 32, 76),
        "bg_bot": (9, 14, 36),
        "glow1": (59, 91, 219),
        "glow2": (43, 180, 120),
    },
    {
        "type": "ipad",
        "src": os.path.join(SRC_IPAD, "5.GPA.png"),
        "out": "5_iPad_GPA_Calculate_GPA.png",
        "headline": ["Calculate your", "GPA effortlessly"],
        "subtitle": ["Automatic semester and cumulative", "GPA tracking across all credits."],
        "bg_top": (28, 26, 80),
        "bg_bot": (12, 11, 35),
        "glow1": (112, 72, 232),
        "glow2": (66, 99, 235),
    },
    {
        "type": "ipad",
        "src": os.path.join(SRC_IPAD, "6.RightClick.png"),
        "out": "6_iPad_QuickActions_Edit_Fast.png",
        "headline": ["Quick actions at", "your fingertips"],
        "subtitle": ["Edit, duplicate, weight categories, or", "convert to events in a single tap."],
        "bg_top": (18, 32, 72),
        "bg_bot": (9, 15, 34),
        "glow1": (16, 152, 173),
        "glow2": (76, 110, 245),
    },
    {
        "type": "ipad",
        "src": os.path.join(SRC_IPAD, "Widgets.jpg"),
        "out": "7_iPad_Widgets_And_Reminders.png",
        "headline": ["Widgets &", "smart reminders"],
        "subtitle": ["Get timely reminders for assignments and", "classes, plus live Home Screen widgets."],
        "bg_top": (28, 24, 76),
        "bg_bot": (12, 10, 34),
        "glow1": (132, 94, 247),
        "glow2": (76, 110, 245),
    },
]


def run():
    os.makedirs(OUT_IPAD, exist_ok=True)
    f_head = get_font(FONT_EXTRABOLD, 112)
    f_sub = get_font(FONT_MEDIUM, 44)

    for slide in SLIDES:
        canvas = make_background(W, H, slide["bg_top"], slide["bg_bot"], slide["glow1"], slide["glow2"], 0.50, 0.52)

        text_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tsd = ImageDraw.Draw(text_shadow)
        text_main = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmd = ImageDraw.Draw(text_main)

        hy = 104
        for line in slide["headline"]:
            lw = tmd.textlength(line, font=f_head)
            lx = (W - lw) // 2
            tsd.text((lx, hy + 6), line, font=f_head, fill=(0, 0, 0, 110))
            tmd.text((lx, hy), line, font=f_head, fill=(255, 255, 255, 255))
            hy += 124

        text_shadow = text_shadow.filter(ImageFilter.GaussianBlur(10))
        canvas = Image.alpha_composite(canvas, text_shadow)
        canvas = Image.alpha_composite(canvas, text_main)

        sub_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(sub_layer)
        sy = 378
        for line in slide["subtitle"]:
            lw = sd.textlength(line, font=f_sub)
            sd.text(((W - lw) // 2, sy), line, font=f_sub, fill=(214, 226, 255, 232))
            sy += 58
        canvas = Image.alpha_composite(canvas, sub_layer)

        if slide["type"] == "ipad":
            ipad, iw, ih = build_ipad_mockup(slide["src"], scr_w=1560, scr_h=2081)
            canvas = add_drop_shadow(canvas, ipad, ((W - iw) // 2, 528), (0, 36), 50, 200)
        elif slide["type"] == "ipad_and_phone":
            ipad, iw, ih = build_ipad_mockup(slide["src"], scr_w=1420, scr_h=1894)
            canvas = add_drop_shadow(canvas, ipad, (96, 560), (0, 34), 48, 200)
            phone, pw, ph = build_phone_mockup(slide["phone_src"], scr_w=580, scr_h=1261)
            canvas = add_drop_shadow(canvas, phone, (1356, 1280), (-14, 28), 44, 215)

        out_path = os.path.join(OUT_IPAD, slide["out"])
        canvas.convert("RGB").save(out_path, format="PNG", optimize=True)
        print(f"[iPad] Saved {out_path}")
