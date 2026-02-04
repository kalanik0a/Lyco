"""Lyco Image Mosaic - compose image mosaics from YAML and edit layouts in a GUI."""

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List

from PIL import Image


def parse_resolution(text: str) -> tuple[int, int]:
    """Parse a WxH string like 1920x1080 into (width, height)."""
    try:
        w_str, h_str = text.lower().split("x", 1)
        w = int(w_str)
        h = int(h_str)
        if w <= 0 or h <= 0:
            raise ValueError
        return w, h
    except Exception as exc:
        raise SystemExit(
            f"Invalid resolution '{text}'. Use WIDTHxHEIGHT, e.g. 2560x1440"
        ) from exc


def load_yaml(path: Path) -> dict:
    """Load YAML layout config as a dict."""
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise SystemExit(
            "Missing dependency: PyYAML. Install with: python -m pip install pyyaml"
        ) from exc

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise SystemExit("Config root must be a mapping/object.")
    return data


def save_yaml(path: Path, data: dict) -> None:
    """Save YAML layout config."""
    try:
        import yaml  # type: ignore
    except Exception as exc:
        raise SystemExit(
            "Missing dependency: PyYAML. Install with: python -m pip install pyyaml"
        ) from exc

    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)


@dataclass
class Item:
    file: str
    x: int
    y: int
    w: int
    h: int
    resolution: str


def compose_from_yaml(config_path: Path, output_override: str | None) -> None:
    """Compose a transparent PNG from a YAML layout file."""
    data = load_yaml(config_path)

    output_path = output_override or data.get("output") or "wallpaper.png"

    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise SystemExit("Config must include non-empty 'items' list.")

    # Optional explicit canvas size
    canvas_w = data.get("canvas_width")
    canvas_h = data.get("canvas_height")
    if canvas_w is not None and canvas_h is not None:
        try:
            canvas_w = int(canvas_w)
            canvas_h = int(canvas_h)
        except Exception as exc:
            raise SystemExit("canvas_width and canvas_height must be integers") from exc
        if canvas_w <= 0 or canvas_h <= 0:
            raise SystemExit("canvas_width and canvas_height must be > 0")

    placed = []
    max_right = 0
    max_bottom = 0

    for idx, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise SystemExit(f"Item #{idx} must be an object.")

        try:
            x = int(item["x"])
            y = int(item["y"])
            file_path = Path(item["file"])
        except Exception as exc:
            raise SystemExit(f"Item #{idx} must include x, y, file") from exc

        res = item.get("resolution")
        if not isinstance(res, str):
            raise SystemExit(f"Item #{idx} must include resolution like 1920x1080")
        w, h = parse_resolution(res)

        with Image.open(file_path) as im:
            im = im.convert("RGBA")
            im = im.resize((w, h), Image.LANCZOS)
            placed.append((im, x, y, w, h))

        max_right = max(max_right, x + w)
        max_bottom = max(max_bottom, y + h)

    if canvas_w is None or canvas_h is None:
        canvas_w = max_right
        canvas_h = max_bottom

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    for im, x, y, _w, _h in placed:
        canvas.paste(im, (x, y))

    canvas.save(output_path)


class LayoutItem:
    """A draggable rectangle that represents an image placement in the layout."""

    def __init__(self, item: Item, index: int, on_move, on_snap):
        from PyQt5.QtCore import QRectF
        from PyQt5.QtGui import QBrush, QPen, QColor, QFont, QPixmap, QImage
        from PyQt5.QtWidgets import QGraphicsItem

        self.item = item
        self.index = index
        self.on_move = on_move
        self.on_snap = on_snap

        self.rect = QRectF(0, 0, item.w, item.h)
        self.pixmap = None
        try:
            # Load and scale image for preview
            img = Image.open(item.file).convert("RGBA")
            img = img.resize((item.w, item.h), Image.LANCZOS)
            data = img.tobytes("raw", "RGBA")
            qimg = QImage(data, item.w, item.h, QImage.Format_RGBA8888)
            self.pixmap = QPixmap.fromImage(qimg)
        except Exception:
            self.pixmap = None

        self.brush = QBrush(QColor(50, 150, 230, 60))
        self.pen = QPen(QColor(50, 150, 230), 2)
        self.text_color = QColor(255, 255, 255)
        self.font = QFont("Sans", 14)

        class RectItem(QGraphicsItem):
            def __init__(self, outer):
                super().__init__()
                self.outer = outer
                self.setFlags(
                    QGraphicsItem.ItemIsMovable
                    | QGraphicsItem.ItemIsSelectable
                    | QGraphicsItem.ItemSendsGeometryChanges
                )
                self.setPos(outer.item.x, outer.item.y)

            def boundingRect(self):
                return self.outer.rect

            def paint(self, painter, option, widget=None):
                if self.outer.pixmap:
                    painter.drawPixmap(0, 0, self.outer.pixmap)
                painter.setBrush(self.outer.brush)
                painter.setPen(self.outer.pen)
                painter.drawRect(self.outer.rect)
                painter.setPen(self.outer.text_color)
                painter.setFont(self.outer.font)
                painter.drawText(8, 20, str(self.outer.index))

            def itemChange(self, change, value):
                from PyQt5.QtWidgets import QGraphicsItem
                if change == QGraphicsItem.ItemPositionChange:
                    from PyQt5.QtCore import QPointF
                    pos = value
                    new_x = int(pos.x())
                    new_y = int(pos.y())
                    if self.outer.on_snap:
                        new_x, new_y = self.outer.on_snap(self.outer.item, new_x, new_y)
                    self.outer.item.x = int(new_x)
                    self.outer.item.y = int(new_y)
                    self.outer.on_move(self.outer.item)
                    return QPointF(self.outer.item.x, self.outer.item.y)
                return super().itemChange(change, value)

            def mousePressEvent(self, event):
                from PyQt5.QtCore import Qt
                if event.modifiers() & Qt.ControlModifier:
                    event.ignore()
                    return
                super().mousePressEvent(event)

            def mouseMoveEvent(self, event):
                from PyQt5.QtCore import Qt
                if event.modifiers() & Qt.ControlModifier:
                    event.ignore()
                    return
                super().mouseMoveEvent(event)

        self.graphics_item = RectItem(self)


class ZoomableGraphicsView:
    """Graphics view with Ctrl+wheel zoom and Ctrl+drag pan."""

    def __init__(self, scene, on_zoom):
        from PyQt5.QtWidgets import QGraphicsView
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPainter

        class _View(QGraphicsView):
            def __init__(self, scene, on_zoom):
                super().__init__(scene)
                self.on_zoom = on_zoom
                self._zoom = 1.0
                self.setRenderHint(QPainter.Antialiasing)
                self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
                self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
                self.setDragMode(QGraphicsView.NoDrag)

            def wheelEvent(self, event):
                if event.modifiers() & Qt.ControlModifier:
                    delta = event.angleDelta().y()
                    factor = 1.15 if delta > 0 else 1 / 1.15
                    new_zoom = self._zoom * factor
                    if 0.1 <= new_zoom <= 10:
                        self._zoom = new_zoom
                        self.scale(factor, factor)
                        if self.on_zoom:
                            self.on_zoom(self._zoom)
                    event.accept()
                else:
                    super().wheelEvent(event)

            def mousePressEvent(self, event):
                if event.button() == Qt.LeftButton and (event.modifiers() & Qt.ControlModifier):
                    self.setDragMode(QGraphicsView.ScrollHandDrag)
                super().mousePressEvent(event)

            def mouseReleaseEvent(self, event):
                super().mouseReleaseEvent(event)
                if self.dragMode() == QGraphicsView.ScrollHandDrag:
                    self.setDragMode(QGraphicsView.NoDrag)

        self.widget = _View(scene, on_zoom)


class LayoutEditor:
    """GUI editor for YAML layouts."""

    def __init__(self, config_path: Path):
        from PyQt5.QtWidgets import (
            QApplication,
            QMainWindow,
            QWidget,
            QVBoxLayout,
            QHBoxLayout,
            QPushButton,
            QLabel,
            QGraphicsScene,
            QFileDialog,
            QSplitter,
            QPlainTextEdit,
            QTextEdit,
            QFrame,
        )
        from PyQt5.QtCore import Qt, QRect, QSize, QTimer
        from PyQt5.QtGui import (
            QSyntaxHighlighter,
            QTextCharFormat,
            QColor,
            QFont,
            QPainter,
            QTextCursor,
            QTextFormat,
            QFontDatabase,
            QPalette,
        )

        self.config_path = config_path
        self.data = {}
        self.output = "wallpaper.png"
        self.items: List[Item] = []
        self.canvas_w = 1
        self.canvas_h = 1
        self.snap_threshold = 10

        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.setWindowTitle(f"Lyco Image Mosaic - {self.config_path}")
        self.window.resize(1200, 800)

        central = QWidget()
        self.window.setCentralWidget(central)
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        toolbar = QHBoxLayout()
        main_layout.addLayout(toolbar)

        self.coord_label = QLabel("X: -, Y: -")
        toolbar.addWidget(self.coord_label)

        self.zoom_label = QLabel("Zoom: 100%")
        toolbar.addWidget(self.zoom_label)

        self.yaml_status = QLabel("YAML: OK")
        toolbar.addWidget(self.yaml_status)

        save_btn = QPushButton("Save YAML")
        save_btn.clicked.connect(self.on_save)
        toolbar.addWidget(save_btn)

        apply_btn = QPushButton("Apply YAML")
        apply_btn.clicked.connect(self.on_apply_yaml)
        toolbar.addWidget(apply_btn)

        export_btn = QPushButton("Export PNG")
        export_btn.clicked.connect(self.on_export_png)
        toolbar.addWidget(export_btn)

        toolbar.addStretch(1)

        self.scene = QGraphicsScene(0, 0, self.canvas_w, self.canvas_h)
        view = ZoomableGraphicsView(self.scene, self.on_zoom)
        self.view = view.widget

        # YAML editor with line numbers + syntax highlighting.
        class LineNumberArea(QFrame):
            def __init__(self, editor):
                super().__init__(editor)
                self.editor = editor

            def sizeHint(self):
                return QSize(self.editor.line_number_area_width(), 0)

            def paintEvent(self, event):
                self.editor.line_number_area_paint_event(event)

        class LineNumberTextEdit(QPlainTextEdit):
            def __init__(self):
                super().__init__()
                self.line_number_area = LineNumberArea(self)
                self.blockCountChanged.connect(self.update_line_number_area_width)
                self.updateRequest.connect(self.update_line_number_area)
                self.cursorPositionChanged.connect(self.highlight_current_line)
                self.update_line_number_area_width(0)
                self.highlight_current_line()

            def line_number_area_width(self):
                digits = len(str(max(1, self.blockCount())))
                space = 6 + self.fontMetrics().horizontalAdvance("9") * digits
                return space

            def update_line_number_area_width(self, _):
                self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

            def update_line_number_area(self, rect, dy):
                if dy:
                    self.line_number_area.scroll(0, dy)
                else:
                    self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
                if rect.contains(self.viewport().rect()):
                    self.update_line_number_area_width(0)

            def resizeEvent(self, event):
                super().resizeEvent(event)
                cr = self.contentsRect()
                self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height()))

            def line_number_area_paint_event(self, event):
                pal = self.palette()
                painter = QPainter(self.line_number_area)
                painter.fillRect(event.rect(), pal.color(QPalette.AlternateBase))
                block = self.firstVisibleBlock()
                block_number = block.blockNumber()
                top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
                bottom = top + int(self.blockBoundingRect(block).height())
                while block.isValid() and top <= event.rect().bottom():
                    if block.isVisible() and bottom >= event.rect().top():
                        number = str(block_number + 1)
                        painter.setPen(pal.color(QPalette.Text))
                        painter.drawText(0, top, self.line_number_area.width() - 4, self.fontMetrics().height(),
                                         Qt.AlignRight, number)
                    block = block.next()
                    top = bottom
                    bottom = top + int(self.blockBoundingRect(block).height())
                    block_number += 1

            def highlight_current_line(self):
                extra = []
                if not self.isReadOnly():
                    selection = QTextEdit.ExtraSelection()
                    selection.format.setBackground(self.palette().color(QPalette.AlternateBase))
                    selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                    selection.cursor = self.textCursor()
                    selection.cursor.clearSelection()
                    extra.append(selection)
                self.setExtraSelections(extra)

        class YamlHighlighter(QSyntaxHighlighter):
            def __init__(self, document, palette: QPalette):
                super().__init__(document)
                self.rules = []
                base = palette.color(QPalette.Base)
                text = palette.color(QPalette.Text)
                is_dark = base.lightness() < 128

                def mix(c1: QColor, c2: QColor, t: float) -> QColor:
                    return QColor(
                        int(c1.red() * (1 - t) + c2.red() * t),
                        int(c1.green() * (1 - t) + c2.green() * t),
                        int(c1.blue() * (1 - t) + c2.blue() * t),
                    )

                key_format = QTextCharFormat()
                key_format.setForeground(mix(text, QColor(80, 160, 255) if is_dark else QColor(30, 110, 210), 0.6))
                key_format.setFontWeight(QFont.Bold)
                self.rules.append((r"^\\s*[^:#\\n]+(?=\\s*:)", key_format))

                string_format = QTextCharFormat()
                string_format.setForeground(mix(text, QColor(140, 220, 160) if is_dark else QColor(40, 140, 80), 0.6))
                self.rules.append((r"\"[^\"\\n]*\"", string_format))
                self.rules.append((r"'[^'\\n]*'", string_format))

                number_format = QTextCharFormat()
                number_format.setForeground(mix(text, QColor(255, 200, 120) if is_dark else QColor(180, 120, 30), 0.6))
                self.rules.append((r"\\b\\d+\\b", number_format))

                bool_format = QTextCharFormat()
                bool_format.setForeground(mix(text, QColor(255, 150, 200) if is_dark else QColor(160, 60, 120), 0.6))
                self.rules.append((r"\\b(true|false|null)\\b", bool_format))

                comment_format = QTextCharFormat()
                comment_format.setForeground(mix(text, QColor(140, 140, 140), 0.5))
                self.rules.append((r"#.*$", comment_format))

            def highlightBlock(self, text):
                import re
                for pattern, fmt in self.rules:
                    for match in re.finditer(pattern, text):
                        start = match.start()
                        length = match.end() - match.start()
                        self.setFormat(start, length, fmt)

        editor_container = QWidget()
        editor_layout = QVBoxLayout()
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_container.setLayout(editor_layout)

        self.yaml_editor = LineNumberTextEdit()
        mono = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        mono.setPointSize(10)
        mono.setKerning(True)
        mono.setStyleStrategy(QFont.PreferAntialias)
        mono.setStyleHint(QFont.TypeWriter)
        self.yaml_editor.setFont(mono)
        self.yaml_editor.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.yaml_editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.yaml_editor.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.yaml_editor.setTabStopDistance(self.yaml_editor.fontMetrics().horizontalAdvance(" ") * 2)
        self.yaml_highlighter = YamlHighlighter(self.yaml_editor.document(), self.app.palette())
        editor_layout.addWidget(self.yaml_editor)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(editor_container)
        splitter.addWidget(self.view)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        editor_container.setMinimumWidth(320)
        self.splitter = splitter
        main_layout.addWidget(splitter)

        self.layout_items = []
        self.error_timer = QTimer()
        self.error_timer.setSingleShot(True)
        self.error_timer.timeout.connect(self.validate_yaml_text)

        self.yaml_editor.textChanged.connect(self.on_yaml_text_changed)

        # Load initial YAML into both the editor and the scene.
        self.load_from_yaml_file()

        self.window.show()
        QTimer.singleShot(0, self.apply_splitter_ratio)
        self.app.exec_()

    def on_item_move(self, item: Item):
        self.coord_label.setText(f"X: {item.x}, Y: {item.y}")

    def snap_position(self, moving: Item, x: int, y: int) -> tuple[int, int]:
        # Snap edges if within threshold to another item's edges.
        snap = self.snap_threshold
        new_x = x
        new_y = y

        for other in self.items:
            if other is moving:
                continue

            # Horizontal snapping: left/right edges
            if abs(new_x - (other.x + other.w)) <= snap:
                new_x = other.x + other.w
            if abs((new_x + moving.w) - other.x) <= snap:
                new_x = other.x - moving.w
            if abs(new_x - other.x) <= snap:
                new_x = other.x
            if abs((new_x + moving.w) - (other.x + other.w)) <= snap:
                new_x = other.x + other.w - moving.w

            # Vertical snapping: top/bottom edges
            if abs(new_y - (other.y + other.h)) <= snap:
                new_y = other.y + other.h
            if abs((new_y + moving.h) - other.y) <= snap:
                new_y = other.y - moving.h
            if abs(new_y - other.y) <= snap:
                new_y = other.y
            if abs((new_y + moving.h) - (other.y + other.h)) <= snap:
                new_y = other.y + other.h - moving.h

        return new_x, new_y

    def on_zoom(self, zoom_value: float):
        self.zoom_label.setText(f"Zoom: {int(zoom_value * 100)}%")

    def apply_splitter_ratio(self):
        # Set initial pane ratio to roughly 1/3 editor and 2/3 canvas.
        total = max(1, self.window.width())
        left = max(320, total // 3)
        right = max(1, total - left)
        self.splitter.setSizes([left, right])

    def on_yaml_text_changed(self):
        self.error_timer.start(300)

    def validate_yaml_text(self):
        text = self.yaml_editor.toPlainText()
        try:
            import yaml  # type: ignore
            yaml.safe_load(text)
            self.yaml_status.setText("YAML: OK")
            self.yaml_status.setStyleSheet("color: #9ad27a;")
            self.clear_error_highlight()
        except Exception as exc:
            msg = str(exc)
            self.yaml_status.setText(f"YAML: {msg}")
            self.yaml_status.setStyleSheet("color: #ff8c8c;")
            self.highlight_error_line(msg)

    def highlight_error_line(self, msg: str):
        # Best-effort parse of line number from PyYAML error message.
        import re
        match = re.search(r"line\\s+(\\d+)", msg)
        if not match:
            self.clear_error_highlight()
            return
        line_no = int(match.group(1))
        cursor = self.yaml_editor.textCursor()
        cursor.movePosition(QTextCursor.Start)
        for _ in range(line_no - 1):
            cursor.movePosition(QTextCursor.Down)
        cursor.select(QTextCursor.LineUnderCursor)
        extra = QTextEdit.ExtraSelection()
        extra.cursor = cursor
        extra.format.setBackground(QColor(90, 40, 40))
        extras = self.yaml_editor.extraSelections()
        # Preserve current-line highlight at index 0 if present.
        if extras:
            extras = extras[:1]
        else:
            extras = []
        extras.append(extra)
        self.yaml_editor.setExtraSelections(extras)

    def clear_error_highlight(self):
        extras = self.yaml_editor.extraSelections()
        if extras:
            self.yaml_editor.setExtraSelections(extras[:1])

    def load_from_yaml_file(self):
        self.data = load_yaml(self.config_path)
        self.output = self.data.get("output", "wallpaper.png")
        self.yaml_editor.blockSignals(True)
        self.yaml_editor.setPlainText(self.config_path.read_text(encoding="utf-8"))
        self.yaml_editor.blockSignals(False)
        self.validate_yaml_text()
        self.apply_yaml_data(self.data)

    def apply_yaml_data(self, data: dict):
        items_data = data.get("items")
        if not isinstance(items_data, list) or not items_data:
            raise SystemExit("Config must include non-empty 'items' list.")

        self.items = []
        for idx, item in enumerate(items_data, start=1):
            if not isinstance(item, dict):
                raise SystemExit(f"Item #{idx} must be an object.")
            try:
                x = int(item["x"])
                y = int(item["y"])
                file_path = str(item["file"])
                res = str(item["resolution"])
            except Exception as exc:
                raise SystemExit(f"Item #{idx} must include x, y, file, resolution") from exc
            w, h = parse_resolution(res)
            self.items.append(Item(file=file_path, x=x, y=y, w=w, h=h, resolution=res))

        canvas_w = data.get("canvas_width")
        canvas_h = data.get("canvas_height")
        if canvas_w is None or canvas_h is None:
            max_right = max(i.x + i.w for i in self.items)
            max_bottom = max(i.y + i.h for i in self.items)
            canvas_w = max_right
            canvas_h = max_bottom
        self.canvas_w = int(canvas_w)
        self.canvas_h = int(canvas_h)

        self.scene.clear()
        self.layout_items = []
        for idx, it in enumerate(self.items, start=1):
            li = LayoutItem(it, idx, self.on_item_move, self.snap_position)
            self.layout_items.append(li)
            self.scene.addItem(li.graphics_item)
        self.scene.setSceneRect(0, 0, self.canvas_w, self.canvas_h)
        self.view.centerOn(self.canvas_w / 2, self.canvas_h / 2)

    def on_save(self):
        text = self.yaml_editor.toPlainText()
        try:
            import yaml  # type: ignore
            data = yaml.safe_load(text)
            if not isinstance(data, dict):
                raise ValueError("Config root must be a mapping/object.")
        except Exception as exc:
            self.yaml_status.setText(f"YAML: {exc}")
            self.yaml_status.setStyleSheet("color: #ff8c8c;")
            self.highlight_error_line(str(exc))
            return

        # Save text first, then apply to the scene.
        self.config_path.write_text(text, encoding="utf-8")
        self.apply_yaml_data(data)

        # Normalize to top-left origin and save with tight canvas bounds.
        min_x = min(it.x for it in self.items)
        min_y = min(it.y for it in self.items)
        max_right = max(it.x + it.w for it in self.items)
        max_bottom = max(it.y + it.h for it in self.items)

        shift_x = -min_x
        shift_y = -min_y

        items_out = []
        for it in self.items:
            items_out.append({
                "file": it.file,
                "x": it.x + shift_x,
                "y": it.y + shift_y,
                "resolution": it.resolution,
            })

        data_out = {
            "output": self.output,
            "canvas_width": max_right - min_x,
            "canvas_height": max_bottom - min_y,
            "items": items_out,
        }
        save_yaml(self.config_path, data_out)

        # Recenter the view by normalizing in-memory positions and scene bounds.
        self.canvas_w = data_out["canvas_width"]
        self.canvas_h = data_out["canvas_height"]
        for li in self.layout_items:
            li.item.x += shift_x
            li.item.y += shift_y
            li.graphics_item.setPos(li.item.x, li.item.y)
        self.scene.setSceneRect(0, 0, self.canvas_w, self.canvas_h)
        self.view.centerOn(self.canvas_w / 2, self.canvas_h / 2)
        self.yaml_editor.blockSignals(True)
        self.yaml_editor.setPlainText(self.config_path.read_text(encoding="utf-8"))
        self.yaml_editor.blockSignals(False)
        self.validate_yaml_text()

    def on_apply_yaml(self):
        text = self.yaml_editor.toPlainText()
        try:
            import yaml  # type: ignore
            data = yaml.safe_load(text)
            if not isinstance(data, dict):
                raise ValueError("Config root must be a mapping/object.")
        except Exception as exc:
            self.yaml_status.setText(f"YAML: {exc}")
            self.yaml_status.setStyleSheet("color: #ff8c8c;")
            self.highlight_error_line(str(exc))
            return
        self.apply_yaml_data(data)

    def on_export_png(self):
        from PyQt5.QtGui import QImage, QPainter
        from PyQt5.QtWidgets import QFileDialog
        from PyQt5.QtCore import Qt

        path, _ = QFileDialog.getSaveFileName(
            self.window,
            "Export Wallpaper PNG",
            self.output,
            "PNG Images (*.png)"
        )
        if not path:
            return

        image = QImage(self.canvas_w, self.canvas_h, QImage.Format_RGBA8888)
        image.fill(Qt.transparent)

        painter = QPainter(image)
        self.scene.render(painter)
        painter.end()

        image.save(path)


def run_gui(config_path: Path) -> None:
    """Launch the PyQt GUI editor."""
    LayoutEditor(config_path)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Lyco Image Mosaic: compose and edit image mosaics via YAML."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gui = sub.add_parser("gui", help="Open the GUI layout editor")
    gui.add_argument("-c", "--config", required=True, help="Path to YAML config")

    compose = sub.add_parser("compose", help="Compose a wallpaper from YAML")
    compose.add_argument("-c", "--config", required=True, help="Path to YAML config")
    compose.add_argument(
        "-o", "--output",
        default=None,
        help="Output PNG path (overrides config output if set)"
    )

    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.command == "gui":
        run_gui(Path(args.config))
        return

    if args.command == "compose":
        compose_from_yaml(Path(args.config), args.output)
        return


if __name__ == "__main__":
    main()
