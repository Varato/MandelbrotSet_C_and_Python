import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools as it
import Mandelbrot as Mand


(N, M) = (451, 451)


def static_draw(ax, RGB, n_max=10):
	h = 0.01/100
	x0 = -0.75
	y0 = -0.2
	colors = [RGB*x for x in np.tanh(np.linspace(0,n_max/15,n_max+1))]

	n = np.array(Mand.iterate(n_max, h, x0, y0), dtype=int)
	print(n)
	if np.max(n) > n_max:
		print(np.max(n))
	print("safe", n_max)
	color_mat = np.zeros([N,M,3])
	for i in range(N):
		for j in range(M):
			color_mat[i,j] = colors[n[i,j]]
	ax.set_xticks([])
	ax.set_yticks([])
	ax.imshow(color_mat, cmap="gray", interpolation="nearest")
	plt.show()



def iter_animate(fig, ax, RGB, iter_times = 10):
	extent = [-2.2, 2.2, -2.2, 2.2]
	color_mat = np.zeros([N,M,3]) 
	img = ax.imshow(color_mat, cmap="gray", interpolation="nearest", extent=extent)
	text = ax.text(1.1, 2.3, "")
	h = 0.01
	x0 = -1
	y0 = -1

	colors = [RGB*x for x in np.tanh(np.linspace(0,iter_times/5,iter_times+1))]

	def init():
		pass
	def update(data):
		n, i = data
		text.set_text("iteration times = {}".format(i+1))
		for i in range(N):
			for j in range(M):
				color_mat[i,j] = colors[n[i,j]][:]
		img.set_data(color_mat)
		return (text, img)
		
	def data_gen():
		for i in range(iter_times):
			n = np.array(Mand.iterate(i, h, x0, y0), dtype=int)[:]
			if np.max(n) > i+1:
				print(i)
				print(np.max(n))
				quit()
			yield (n, i)


	anim = animation.FuncAnimation(fig, update, data_gen, init_func=init, interval=500)
	# anim.save('Mandelbrot_colored2.gif', writer='imagemagick', fps=300)
	plt.show()

def zoom_in_animate(fig, ax):
	h = 0.01
	scale_rate = 5
	x = b

	def init():
		pass
	def update(data):
		n, i = data
		text.set_text("iteration times = {}".format(i+1))
		for i in range(N):
			for j in range(M):
				color_mat[i,j] = colors[n[i,j]][:]
		img.set_data(color_mat)
		return (text, img)
		
	def data_gen():
		for i in range(iter_times):
			n = np.array(Mand.iterate(i, h, x0, y0), dtype=int)[:]
			if np.max(n) > i+1:
				print(i)
				print(np.max(n))
				quit()
			yield (n, i)


	anim = animation.FuncAnimation(fig, update, data_gen, init_func=init, interval=500)
	# anim.save('Mandelbrot_colored2.gif', writer='imagemagick', fps=300)
	plt.show()





if __name__=="__main__":
	fig, ax = plt.subplots(ncols=1, figsize=[9,9])
	RGB = np.array([0.5,1,0.5])
	static_draw(ax, RGB, n_max=120)
	# iter_animate(fig, ax, RGB = RGB, iter_times=30)
