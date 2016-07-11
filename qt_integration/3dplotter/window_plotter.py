from ui_window_plotter import Ui_WindowPlotter
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from math import *
import parser
import time
import gs


def create_grid_from_samples(samples, x_res, y_res):
	lines = []

	for y in range(y_res - 1):
		for x in range(x_res - 1):
			lines.append(samples[y * x_res + x])
			lines.append(samples[y * x_res + x + 1])
			lines.append(samples[y * x_res + x])
			lines.append(samples[(y + 1) * x_res + x])

	for x in range(x_res - 1):
		lines.append(samples[(y_res - 1) * x_res + x])
		lines.append(samples[(y_res - 1) * x_res + x + 1])

	for y in range(y_res - 1):
		lines.append(samples[y * x_res + x_res - 1])
		lines.append(samples[(y + 1) * x_res + x_res - 1])

	return lines


class WindowPlotter(QMainWindow):
	def __init__(self, renderer, render_system):
		super().__init__()

		self.renderer, self.render_system = renderer, render_system

		# create the window UI from the pre-compiled resource (PyUIC5)
		self.ui = Ui_WindowPlotter()
		self.ui.setupUi(self)

		# retrieve the Qt widget system handle
		self.view_handle = gs.int_to_voidp(int(self.ui.viewport_widget.winId()))
		# create a proxy renderer window over the Qt widget system window handle
		self.window = renderer.NewOutputWindow(16, 16, 32, gs.Window.Windowed, self.view_handle)
		self.aspect_ratio = gs.Vector2(1, 1)

		self.function = None  # the function to evaluate over the grid

		# start a periodic timer to refresh the output
		self.display_timer = QTimer()
		self.display_timer.timeout.connect(self.update)
		self.display_timer.start(1000//50)

		# store the graph orientation and mouse
		self.prev_mx, self.prev_my = 0, 0
		self.graph_euler = gs.Vector3()
		self.distance = -16

		self.on_FormulaLineEdit_textEdited(self.ui.FormulaLineEdit.text())

	def mousePressEvent(self, event):
		self.prev_mx, self.prev_my = event.x(), event.y()

	def mouseMoveEvent(self, event):
		dx, dy = event.x() - self.prev_mx, event.y() - self.prev_my
		self.graph_euler.x -= dy * 0.005
		self.graph_euler.y -= dx * 0.005
		self.prev_mx, self.prev_my = event.x(), event.y()

	def wheelEvent(self, event):
		self.distance += event.angleDelta().y() * 0.01

	def resizeEvent(self, event):
		size = event.size()
		self.aspect_ratio = gs.Vector2(size.height() / size.width(), 1)
		self.renderer.SetViewport(gs.fRect(0, 0, size.width(), size.height()))

	def update(self):
		if self.function is None:
			return

		# collect grid samples by evaluating the function
		x_min, x_max = self.ui.XMinDoubleSpinBox.value(), self.ui.XMaxDoubleSpinBox.value()
		y_min, y_max = self.ui.YMinDoubleSpinBox.value(), self.ui.YMaxDoubleSpinBox.value()
		resolution = self.ui.ResolutionSpinBox.value()

		samples = []
		y = y_min
		while y < y_max:
			x = x_min
			while x < x_max:
				try:
					z = eval(self.function)
				except:
					z = 0
				samples.append(gs.Vector3(x, y, z))
				x += resolution
			y += resolution

		lines = create_grid_from_samples(samples, ceil((x_max - x_min) / resolution), ceil((y_max - y_min) / resolution))

		# set and clear the output window
		self.renderer.SetOutputWindow(self.window)
		self.renderer.Clear(gs.Color.Grey)

		# orient view toward origin
		self.renderer.SetProjectionMatrix(gs.ComputePerspectiveProjectionMatrix(0.1, 100, 3.2, self.aspect_ratio))

		view_matrix = gs.Matrix4.TranslationMatrix(gs.Vector3(0, 0, self.distance)).LookAt(gs.Vector3.Zero)
		self.renderer.SetViewMatrix(view_matrix)

		# orient world matrix (grid matrix)
		self.renderer.SetWorldMatrix(gs.Matrix4(gs.Matrix3.FromEuler(self.graph_euler)))

		# draw lines
		self.render_system.DrawLineAuto(len(lines) // 2, lines)

		self.renderer.DrawFrame()
		self.renderer.ShowFrame()

	def on_FormulaLineEdit_textEdited(self, text):
		try:
			self.function = parser.expr(text).compile()
		except:
			self.function = None
