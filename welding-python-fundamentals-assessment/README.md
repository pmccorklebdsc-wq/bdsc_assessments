# Welding Python Fundamentals Assessment

> **Module 3 — Programming · Python Fundamentals Assessment**
> Built around the [Welding Defect Detection v1i](https://universe.roboflow.com/final-year-project-kswbt/welding-defect-detection) dataset (CC BY 4.0).

This repository is a self-contained, gradeable assessment that exercises every
core Python construct (variables, types, operators, strings, lists, tuples,
dictionaries, functions, control flow, file I/O) using **real welding
inspection imagery** instead of toy data.

The companion document
**`Module_03_Assessment_Welding_Python_Fundamentals.md`**
(in the BWXT pilot Content Delivery folder) is the assignment brief — read it
first.

---

## What's in this repo

```
welding-python-fundamentals-assessment/
├── README.md
├── requirements.txt
├── .gitignore
├── assessment.py                        # student-facing skeleton (TODOs)
│
├── notebooks/
│   ├── assessment.ipynb                 # NOTEBOOK version of the assessment
│   ├── assessment_solution.ipynb        # NOTEBOOK reference solution
│   ├── build_notebook.py                # regenerates assessment.ipynb
│   └── build_solution_notebook.py       # regenerates assessment_solution.ipynb
│
├── data/
│   └── Welding Defect Detection.v1i.coco/
│       ├── README.dataset.txt
│       ├── README.roboflow.txt
│       └── test/
│           ├── _annotations.coco.json   # COCO-format metadata
│           └── *.jpg                    # 21 frames, 640 × 640
│
├── utils/
│   ├── __init__.py
│   └── welding_utils.py                 # provided helpers (do not modify)
│
├── solution/                            # INSTRUCTOR ONLY
│   ├── __init__.py
│   └── assessment_solution.py           # full reference implementation (script)
│
└── outputs/                             # plots written by your code land here
    └── .gitkeep
```

Students may complete the assessment **either** by editing `assessment.py`
**or** by working through `notebooks/assessment.ipynb`. Both produce the
same `session_log.txt` and `outputs/highlight_frame_0.png`.

> ⚠️ `solution/` is for the instructor. Strip it before publishing the
> repo to students (see *Distribution* below).

---

## Setup

```bash
git clone <this repo>
cd welding-python-fundamentals-assessment

python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell

pip install -r requirements.txt
```

Sanity-check the helpers (pure smoke test, no plots shown):

```bash
python -c "from utils.welding_utils import load_coco_metadata; \
print(len(load_coco_metadata('data/Welding Defect Detection.v1i.coco/test/_annotations.coco.json')['images']), 'images')"
# -> 21 images
```

---

## How students run it

**Option A — script:**

```bash
python assessment.py
```

**Option B — Jupyter notebook:**

```bash
pip install jupyter
jupyter lab notebooks/assessment.ipynb
```

Either way, the expected artifacts after a successful run are:

- `session_log.txt` — append-only log written by every task.
- `outputs/highlight_frame_0.png` — defect-highlight overlay for frame 0.

To regenerate the notebooks from the build scripts (for instructors who edit
the assessment content):

```bash
python notebooks/build_notebook.py
python notebooks/build_solution_notebook.py
```

---

## Provided helpers — `utils/welding_utils.py`

All helpers exchange **plain Python objects** with the student. NumPy and PIL
are used internally only for file I/O and rendering — students never see them.

| Function | Returns / shows |
| --- | --- |
| `load_coco_metadata(path)` | parsed nested `dict` (`info`, `licenses`, `categories`, `images`, `annotations`) |
| `load_image_as_lists(path)` | full-resolution `list[list[(R, G, B)]]` — row-major, ints in `0..255` |
| `load_image_small(path, size=64)` | **same shape, shrunk to 64×64** so beginner loops finish instantly |
| `plot_image(pixels, title=None)` | shows the RGB image |
| `plot_channel(pixels, channel, title=None)` | heatmap of `"R"`, `"G"`, `"B"`, or `"intensity"` |
| `plot_overlay(pixels, mask, title=None)` | greys the background, keeps color where `mask[y][x] == 1` |
| `plot_list(values, title, xlabel, ylabel)` | one-line line plot |
| `save_current_figure(path)` | save the most recent figure (creates parent dirs) |

---

## How instructors run the reference solution

From the repo root, either:

```bash
# Script version
python -m solution.assessment_solution

# Notebook version (executed end-to-end, in place)
MPLBACKEND=Agg jupyter execute notebooks/assessment_solution.ipynb
```

Both produce the *exact* `session_log.txt` and `outputs/highlight_frame_0.png`
that a fully correct submission should yield (numbers may differ in the last
decimal due to floating-point summation order — that is fine).

To render plots without opening any windows during grading, force the
`Agg` matplotlib backend:

```bash
MPLBACKEND=Agg python -m solution.assessment_solution
```

---

## Grading checklist

The full rubric lives in
`Module_03_Assessment_Welding_Python_Fundamentals.md`. At a glance:

- [ ] `python assessment.py` runs end-to-end without manual edits.
- [ ] `session_log.txt` contains entries for every Task 1–11.
- [ ] `outputs/highlight_frame_0.png` shows the bead in color over a grey background.
- [ ] All four image functions (`rgb_to_intensity`, `average_intensity`,
      `min_max_intensity`, `row_stats`) return reasonable values.
- [ ] Task 10 pixel category counts add up to 4 096 (the 64×64 working image).
- [ ] Every list / tuple / dict operation in Tasks 7–8 is demonstrated.

---

## Distribution

To prepare a clean copy for students, delete the instructor solution:

```bash
rm -rf solution/
```

(Or distribute as a GitHub Classroom assignment that excludes `solution/`.)

---

## Dataset & license

- Dataset: *Welding Defect Detection v1i* — Final Year Project / KSWBT
  via Roboflow, **CC BY 4.0**.
- See `data/Welding Defect Detection.v1i.coco/README.dataset.txt` and
  `README.roboflow.txt` for the original notice.

This assessment scaffolding (code, README, brief) is © IARL 2026 and may be
freely reused for non-commercial workforce training.
