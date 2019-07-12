
"""Definition of additionla qt helper objects."""
from itertools import product
import logging
from os import path as op

import pyqtgraph as pg
from PyQt5 import uic
from pyqtgraph.Qt import (QtCore, QtGui, QtWidgets)

from ..defaults import DefaultGeometryConfig as Defaults
from ..gui_utils import create_button, get_icon


def warning(txt, title="Warning"):
    """Inform user about missing information."""
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Information)
    msg_box.setText(txt)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg_box.exec_()


class CircleShape(pg.EllipseROI):
    """Define a Elliptic Shape with a fixed aspect ratio (aka circle)."""

    def __init__(self, pos, size):
        """Create a circular region of interest.

        Parameters:
           pos (tuple) : centre of the circle (x, y)
           size (int) : diameter of the circle
        """
        pen = QtGui.QPen(QtCore.Qt.red, 0.002)
        pg.ROI.__init__(self,
                        pos=pos,
                        size=size,
                        removable=True,
                        movable=False,
                        invertible=False,
                        pen=pen)
        self.aspectLocked = True
        self.handleSize = 0
        _ = [self.removeHandle(handle) for handle in self.getHandles()]

    def __repr__(self):
        size = self.size()[0]
        return 'Circle(d:{})'.format(size)


class SquareShape(pg.RectROI):
    """Define a rectangular Shape with a fixed aspect ratio (aka square)."""

    def __init__(self, pos, size):
        """Create a squared region of interest.

        Parameters:
           pos (tuple) : centre of the circle (x, y)
           size (int) : diameter of the circle
        """
        pen = QtGui.QPen(QtCore.Qt.red, 0.002)
        pg.ROI.__init__(self,
                        pos=pos,
                        size=size,
                        removable=True,
                        movable=False,
                        invertible=False,
                        pen=pen)
        self.aspectLocked = True
        self.handleSize = 0
        _ = [self.removeHandle(handle) for handle in self.getHandles()]

    def __repr__(self):
        size = self.size()[0]
        return 'Square(a:{})'.format(size)


class DetectorHelper(QtGui.QDialog):
    """Setup widgets for quad. positions and geometry file selection."""

    filename_set_signal = QtCore.pyqtSignal()

    def __init__(self, det, fname, parent=None):
        """Create a table element for quad selection and file selection.

        Parameters:
            det (str): the detector (AGIPD or LPD)

        Keywords
            fname (str) :  file name of the geometry file (Default '')
        """
        super().__init__(parent)

        ui_file = op.join(op.dirname(__file__), 'editor/load_detector.ui')
        uic.loadUi(ui_file, self)

        self.setWindowTitle('{} Geometry'.format(det))

        self._det = det
        self.filename = fname
        self.quad_pos = None

        self.populate_table()

        self.bt_load_geometry.clicked.connect(self._get_files)
        self.bt_load_geometry.setIcon(get_icon('file.png'))
        self.bt_ok.clicked.connect(self._apply)
        self.bt_ok.setIcon(get_icon('gtk-ok.png'))
        self.bt_cancel.clicked.connect(self.close)
        self.bt_cancel.setIcon(get_icon('gtk-cancel.png'))

    def set_detector(self, det):
        """Sets a new detector"""
        self._det = det
        self.quad_pos = None
        self.populate_table()

    def _get_files(self):
        """Read the geometry filename of from the dialog."""
        file_format = Defaults.file_formats[self._det]
        f_type = '{} file format (*.{})'.format(*file_format)
        filename, _ = QtGui.QFileDialog.getOpenFileName(self,
                                                        'Load geometry file',
                                                        '.',
                                                        f_type)

        if filename is not None and filename:
            self.filename = filename
            #self.filename_set_signal.emit()

    def populate_table(self):
        """Update the Qudrant table."""
        quad_pos = self.quad_pos or Defaults.fallback_quad_pos[self._det]
        for n, quad_pos in enumerate(quad_pos):
            self.tb_quadrants.setItem(
                n, 0, QtGui.QTableWidgetItem(str(quad_pos[0])))
            self.tb_quadrants.setItem(
                n, 1, QtGui.QTableWidgetItem(str(quad_pos[1])))
        self.tb_quadrants.move(0, 0)

    def _apply(self):
        """Read quad. pos and update the detectors fallback positions."""
        quad_pos = [[None, None] for _ in range(self.tb_quadrants.rowCount())]
        for i, j in product(
                range(self.tb_quadrants.rowCount()),
                range(self.tb_quadrants.columnCount())):
            table_element = self.tb_quadrants.item(i, j)
            try:
                quad_pos[i][j] = float(table_element.text())
            except ValueError:
                warning('Table Elements must be Float')
                return
        if not self.filename and self._det != 'AGIPD':
            warning('You must Select a Geometry File')
            return
        self.quad_pos = quad_pos
        self.filename_set_signal.emit()
        self.close()

class QLogger(logging.Handler):
    """Logger object connected python logging."""

    def __init__(self, main_widget):
        """Create a Dialog that displays the log connected to logging.

        Parameters:
            main_widget : Parent creating this dialog
        """
        super().__init__()
        self.win = QtGui.QDialog(main_widget)
        layout = QtWidgets.QGridLayout()

        self.widget = QtGui.QPlainTextEdit()
        self.widget.setReadOnly(True)
        layout.addWidget(self.widget, 0, 0, 10, 10)
        ok_btn = create_button('Ok', 'ok')
        ok_btn.clicked.connect(lambda: self.win.close())
        layout.addWidget(ok_btn, 11, 0, 1, 1)
        self.win.setLayout(layout)

    def show(self):
        """Show the log window."""
        self.win.show()

    def emit(self, record):
        """Overload emit signal to write into text widget."""
        msg = self.format(record)
        self.widget.appendPlainText(msg)

    def write(self, m):
        """Overload write and do nothing."""
        pass
