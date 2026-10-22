"""Exercise real image codecs/rendering without a browser or network."""
import importlib.metadata
from pathlib import Path
import tomllib

from PIL import Image
import pytest

from browser_harness.video_render import contact_sheet, masked_frame


def test_pillow_exact_source_and_installed_pin():
    project = tomllib.loads((Path(__file__).parents[2] / "pyproject.toml").read_text())
    assert [d for d in project["project"]["dependencies"] if d.lower().startswith("pillow")] == ["pillow==13.0.0"]
    assert importlib.metadata.version("Pillow") == "13.0.0"
    assert "pillow==13.0.0" in importlib.metadata.requires("browser-harness")


@pytest.mark.parametrize("mode", ["RGB", "RGBA", "L"])
def test_contact_sheet_decodes_resizes_and_draws_labels(tmp_path, mode):
    source = tmp_path / "frame.png"
    Image.new(mode, (800, 450), 255 if mode == "L" else "white").save(source)
    output = tmp_path / "sheet.png"
    contact_sheet([{"path": str(source), "label": "Sample", "time": 1.25}], output, "Review")
    with Image.open(output) as image:
        image.load()
        assert image.mode == "RGB"
        assert image.size == (1640, 317)
        assert image.getpixel((200, 100)) == (255, 255, 255)
        # A rendered title and label must change their dark backgrounds.
        assert len(set(image.crop((8, 15, 180, 35)).get_flattened_data())) > 1
        assert len(set(image.crop((8, 284, 180, 304)).get_flattened_data())) > 1


def test_privacy_mask_scales_coordinates_and_preserves_outside_pixels(tmp_path):
    source = tmp_path / "frame.png"
    Image.new("RGBA", (200, 100), "red").save(source)
    comp = {
        "viewport": {"w": 100, "h": 50},
        "redact": {"frame.png": [{"x": 20, "y": 10, "w": 20, "h": 10,
                                    "pad": 0, "radius": 0, "fill": "black", "stroke": "black"}]},
    }
    image = masked_frame(tmp_path, comp, "frame.png")
    assert image.mode == "RGB"
    assert image.size == (200, 100)
    assert image.getpixel((60, 30)) == (0, 0, 0)
    assert image.getpixel((10, 10)) == (255, 0, 0)
    output = tmp_path / "masked.jpg"
    image.save(output, quality=95)
    with Image.open(output) as decoded:
        decoded.load()
        assert max(decoded.getpixel((60, 30))) < 10
        assert decoded.getpixel((10, 10))[0] > 240
