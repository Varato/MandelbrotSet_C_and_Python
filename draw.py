import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import itertools as it
import Mandelbrot as Mand


(N, M) = (451, 451)


def static_draw(ax, RGB, n_max=10):
	h = 0.01/100
	x0 = -0.75
	y0 = -0.2
	colors = [RGB*x for x in np.tanh(np.linspace(0,n_max/15,n_max+1))]

	n = np.array(Mand.iterate(n_max, h, x0, y0), dtype=int)
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
	text = ax.text(-0.5, 2.3, "")
	h = 0.01
	x0 = 0.
	y0 = 0.

	colors = [RGB*x for x in np.linspace(0,iter_times/5,iter_times+1)]

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
			print("iteration times = {}".format(i+1))
			n = np.array(Mand.iterate(i, h, x0, y0), dtype=int)[:]
			yield (n, i)


	anim = animation.FuncAnimation(fig, update, data_gen, init_func=init, interval=500)
	anim.save('Mandelbrot_colored2.gif', writer='imagemagick', fps=300)
	# plt.show()

def zoom_in_animate(fig, ax):
	extent = [-2.2, 2.2, -2.2, 2.2]
	color_mat = np.zeros([N,M,3]) 
	img = ax.imshow(color_mat, cmap="gray", interpolation="nearest", extent=extent)
	ax.scatter(0, 0, s=80, facecolors='none', edgecolors='r')	
	text = ax.text(-1.5, 2.3, "")
	ax.set_yticks([])
	ax.set_xticks([])

	cmap = cm.get_cmap("Spectral")
	colors = [x[:3] for x in cmap(np.linspace(0,1,30))]
	n_colors = len(colors)

	def init():
		pass
	def update(data):
		n, i, n_max, x, y = data
		text.set_text("iteration times = {0}; frames count = {1}; x, y = {2:.3f}, {3:.3f},".format(n_max, i, x, y))
		print("iteration times = {0}, frames count = {1}".format(n_max, i+1))
		for i in range(N):
			for j in range(M):
				color_mat[i,j] = colors[n[i,j]%n_colors]
		img.set_data(color_mat)
		return (text, img)
		
	def data_gen():
		q = np.array([-0.0098,-0.806])
		h0 = 0.01
		scale_rate = 1.2
		for i in range(60):
			h = h0/scale_rate**i
			n_max = min(int(1/h),30000)
			n = np.array(Mand.iterate(n_max, h, q[0], q[1]), dtype=int)[:]
			yield (n, i, n_max, q[0], q[1])

	def save_figs():
		for n, k, n_max, x, y in data_gen():
			# colors = [RGB*x for x in np.tanh(np.linspace(0,5,n_max+1))]
			text.set_text("iteration times = {0}; frames count = {1}; x, y = {2:.3f}, {3:.3f},".format(n_max, k, x, y))
			for i in range(N):
				for j in range(M):
					color_mat[i,j] = colors[n[i,j]%n_colors][:]
			img.set_data(color_mat)
			print("saving img {}...".format(k))
			plt.savefig("./imgs/img{}.png".format(k), dpi=300)
	# save_figs()


	anim = animation.FuncAnimation(fig, update, data_gen, init_func=init, interval=500)
	print("saving animation...")
	anim.save('Mandelbrot_zoom_ultimate.gif', writer='imagemagick', fps=300)
	# plt.show()





if __name__=="__main__":
	fig, ax = plt.subplots(ncols=1, figsize=[9,9])
	RGB = np.array([0.5,1,0.5])
	# static_draw(ax, RGB, n_max=120)
	# iter_animate(fig, ax, RGB = RGB, iter_times=50)
	zoom_in_animate(fig, ax)
