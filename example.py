from draw import *

if __name__=="__main__":
	paint = Paint(N = 451, M = 451)
	# paint.static_draw(ax, h=0.005, n_max=1000)
	# paint.iter_animate(ax, iter_times = 30, h=0.005)
	paint.zoom_animate(ax, n_steps=40, h0 = 0.01/1.2**2, x = -0.1648, y = -1.035)
