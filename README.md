# Lyco Image Mosaic

Lyco Image Mosaic lets you compose a transparent wallpaper from a YAML layout file and edit layouts visually with a PyQt GUI.

![A screenshot of Lyco Image Mosaic](img/screenshot.png)


## Install

```powershell
python -m pip install -r requirements.txt
```

## YAML Layout Format

```yaml
output: wallpaper.png
canvas_width: 7680
canvas_height: 2160
items:
  - file: "img1.png"
    x: 0
    y: 0
    resolution: "1920x1080"
  - file: "img2.jpg"
    x: 1920
    y: 0
    resolution: "2560x1440"
```

Notes:
- `canvas_width` and `canvas_height` are optional. If omitted, Lyco uses the bounding box of items.
- Coordinates are normalized so `0,0` is the top-left of the entire layout when saving from the GUI.

## CLI Usage

Compose a wallpaper from YAML:

```powershell
python Lyco.py compose -c layout.yml -o wallpaper.png
```

## GUI Usage

Open the editor:

```powershell
python Lyco.py gui -c layout.yml
```

GUI controls:
- Drag rectangles to move items.
- Ctrl + Mouse Wheel to zoom.
- Ctrl + Click + Drag to pan.
- Export PNG to save a transparent wallpaper image.
- Save YAML to normalize coordinates and update canvas bounds.

## License

GNU General Public License v3.0. See `LICENSE`.
