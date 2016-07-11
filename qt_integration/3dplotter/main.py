from PyQt5.QtWidgets import QApplication
from window_plotter import WindowPlotter
import sys
import gs


# hook the engine log
def on_log(msgs):
	for i in range(msgs.GetSize()):
		print(msgs.GetMessage(i))

gs.GetOnLogSignal().Connect(on_log)

# mount the system file driver
gs.GetFilesystem().Mount(gs.StdFileDriver("../../pkg.core"), "@core")

# create the renderer
renderer = gs.EglRenderer()

# initialize the default renderer output window
# this window will stay hidden as we output to a Qt widget directly
if not renderer.Open(8, 8, 32, gs.Window.Hidden):
	sys.exit(0)

# initialize the render system, which is used to draw through the renderer
render_system = gs.RenderSystem()
if not render_system.Initialize(renderer):
	sys.exit(0)

# create the application
qt_app = QApplication(sys.argv)

# create the Qt window
window = WindowPlotter(renderer, render_system)
window.show()

# execute the application
res = qt_app.exec()
sys.exit(res)
