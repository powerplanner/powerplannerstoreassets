# Power Planner App Store Asset Generator

Generates App Store-ready opaque RGB PNGs across all targets:

- **iPhone** (`output/iphone/`): 7 screenshots at `1320 x 2868`
- **iPad** (`output/ipad/`): 7 screenshots at `2048 x 2732`
- **Mac** (`output/mac/`): 7 screenshots at `2560 x 1600`
- **iOS Promo** (`output/ios_promo/`): Header Asset (`3840 x 1646`) & Search Result Asset (`3840 x 2560`)

## Setup

Requires Python 3.9+ (`pillow` and `numpy`):

```bash
pip install -r requirements.txt
```

## Usage

Run everything:

```bash
python3 generate_all.py
# or with npm:
npm run generate
```

Or generate a single target:

```bash
python3 generate_all.py --target iphone   # or: ipad | mac | promo
```

## Updating Raw Screenshots

Replace the files in `input/iphone/`, `input/ipad/`, or `input/mac/` keeping the same filenames:

- `input/iphone/`: `1.Calendar.png`, `2.Agenda.png`, `3.Schedule.png`, `4.Grades.png`, `5.GPA.png`, `6.RightClick.png`, `Widgets.jpg`
- `input/ipad/`: `1.Calendar.png`, `2.Agenda.png`, `3.Schedule.png`, `4.Grades.png`, `5.GPA.png`, `6.RightClick.png`, `Widgets.jpg`
- `input/mac/`: `1.Calendar.png`, `2.Schedule.png`, `3.Assignments.png`, `4.Grades.png`, `5.GPA.png`, `6.DayView.png`, `Widgets.png`

To change headlines, subtitles, or colors, edit the `SLIDES` list in `scripts/generate_iphone.py`, `scripts/generate_ipad.py`, `scripts/generate_mac.py`, or `scripts/generate_ios_promo.py`.
