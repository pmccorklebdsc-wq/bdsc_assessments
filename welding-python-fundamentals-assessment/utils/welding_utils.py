"""Utility helpers provided to students for the Module 3 Python Fundamentals
assessment built on the Welding Defect Detection dataset.

The goal is to keep the student-facing surface area pure-Python. All
functions accept and return standard ``list`` / ``tuple`` / ``dict`` /
``int`` / ``float`` objects. NumPy and PIL are used internally only for
file I/O and plotting; they are *never* exposed to the student.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


Pixel = tuple[int, int, int]
ImageList = list[list[Pixel]]


def _show() -> None:
    """Call ``plt.show()`` only on interactive backends.

    When the script is run headless (e.g. ``MPLBACKEND=Agg`` during grading)
    matplotlib's ``Agg`` canvas warns "non-interactive, and thus cannot be
    shown". We swallow that case silently so log output stays clean.
    """
    backend = matplotlib.get_backend().lower()
    if backend in {"agg", "pdf", "ps", "svg", "cairo", "template"}:
        return
    plt.show()


def load_coco_metadata(json_path: str | Path) -> dict:
    """Read a COCO ``_annotations.coco.json`` file and return the parsed dict.

    The returned object is exactly what ``json.load`` produces: a nested
    structure of ``dict`` and ``list``. Top-level keys are
    ``info``, ``licenses``, ``categories``, ``images``, ``annotations``.
    """
    json_path = Path(json_path)
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_image_as_lists(image_path: str | Path) -> ImageList:
    """Load a JPEG/PNG and return it as ``list[list[(R, G, B)]]``.

    No NumPy is exposed: each row is a Python ``list`` of ``(R, G, B)``
    integer tuples in ``0..255``. This is intentionally inefficient — the
    point is for students to iterate over real pixel data with plain Python.
    """
    image_path = Path(image_path)
    with Image.open(image_path) as img:
        rgb = img.convert("RGB")
        width, height = rgb.size
        flat = list(rgb.getdata())  # list of (R, G, B) tuples, row-major

    pixels: ImageList = [
        [flat[y * width + x] for x in range(width)] for y in range(height)
    ]
    return pixels


def load_image_small(image_path: str | Path, size: int = 64) -> ImageList:
    """Load an image and shrink it to ``size x size`` pixels.

    Beginners loop over images with plain Python ``for`` loops, which is
    slow on a 640x640 frame (~410 000 pixels). This helper returns a tiny
    version (default 64x64 = 4 096 pixels) so every loop finishes in well
    under a second on any laptop. The shape is still
    ``list[list[(R, G, B)]]`` so all the student's code still works.
    """
    image_path = Path(image_path)
    with Image.open(image_path) as img:
        rgb = img.convert("RGB").resize((size, size))
        flat = list(rgb.getdata())
    return [[flat[y * size + x] for x in range(size)] for y in range(size)]


def _pixels_to_array(pixels: ImageList) -> np.ndarray:
    """Internal helper: convert a student-style nested list back to a NumPy
    array purely so we can hand it to matplotlib for display."""
    return np.array(pixels, dtype=np.uint8)


def plot_image(pixels: ImageList, title: str | None = None) -> None:
    """Display an image stored as ``list[list[(R, G, B)]]``."""
    arr = _pixels_to_array(pixels)
    plt.figure(figsize=(6, 6))
    plt.imshow(arr)
    if title:
        plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    _show()


def plot_channel(
    pixels: ImageList,
    channel: str = "R",
    title: str | None = None,
) -> None:
    """Show one channel of an image as a heatmap.

    ``channel`` must be one of ``"R"``, ``"G"``, ``"B"`` or ``"intensity"``.
    The intensity option uses the standard Rec. 601 luminance formula
    ``0.299 R + 0.587 G + 0.114 B``.
    """
    arr = _pixels_to_array(pixels).astype(np.float32)
    channel = channel.upper()
    if channel == "R":
        data = arr[:, :, 0]
        cmap = "Reds"
    elif channel == "G":
        data = arr[:, :, 1]
        cmap = "Greens"
    elif channel == "B":
        data = arr[:, :, 2]
        cmap = "Blues"
    elif channel == "INTENSITY":
        data = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
        cmap = "gray"
    else:
        raise ValueError(
            f"channel must be one of R, G, B, intensity (got {channel!r})"
        )

    plt.figure(figsize=(6, 6))
    plt.imshow(data, cmap=cmap, vmin=0, vmax=255)
    plt.colorbar(label=f"{channel.lower()} 0..255")
    if title:
        plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    _show()


def plot_overlay(
    pixels: ImageList,
    mask: list[list[int]],
    title: str | None = None,
) -> None:
    """Greyscale the background; keep original color where ``mask == 1``.

    ``pixels`` and ``mask`` must have the same height and width. ``mask``
    is a ``list[list[int]]`` of 0/1 values.
    """
    arr = _pixels_to_array(pixels)
    h, w, _ = arr.shape
    if len(mask) != h or any(len(row) != w for row in mask):
        raise ValueError("mask shape does not match image shape")

    mask_arr = np.array(mask, dtype=bool)

    luminance = (
        0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
    ).astype(np.uint8)
    grey_rgb = np.stack([luminance] * 3, axis=-1)

    out = grey_rgb.copy()
    out[mask_arr] = arr[mask_arr]

    plt.figure(figsize=(6, 6))
    plt.imshow(out)
    if title:
        plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    _show()


def plot_list(
    values: Sequence[float],
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
) -> None:
    """Quick line plot of any 1-D sequence of numbers."""
    plt.figure(figsize=(8, 3.5))
    plt.plot(list(values))
    if title:
        plt.title(title)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    _show()


def save_current_figure(path: str | Path) -> None:
    """Convenience helper for the §10 deliverable: save the *most recently
    shown* figure to ``path`` (creating parent directories as needed).

    Call this *immediately after* a ``plot_*`` call. It re-uses the active
    matplotlib figure, so no extra arguments are required.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.gcf().savefig(path, dpi=150, bbox_inches="tight")


__all__ = [
    "load_coco_metadata",
    "load_image_as_lists",
    "load_image_small",
    "plot_image",
    "plot_channel",
    "plot_overlay",
    "plot_list",
    "save_current_figure",
]
