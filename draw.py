import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import Mandelbrot as Mand


cmap = cm.get_cmap("Spectral")
colors = [x[:3] for x in cmap(np.linspace(0,1,30))]
n_colors = len(colors)
fig, ax = plt.subplots(ncols=1, figsize=[9,9])

class Paint:
	def __init__(self, N = 451, M = 451):
		self.N = N
		self.M = M

	def static_draw(self, ax, n_max = 10, h = 0.01, x0 = 0, y0 = 0):

		color_mat = np.zeros([self.N,self.M,3]) 
		ax.set_xticks([])
		ax.set_yticks([])
		n = np.array(Mand.iterate(self.N, self.M, n_max, h, x0, y0), dtype=int)
		for i in range(self.N):
			for j in range(self.M):
				color_mat[i,j] = colors[n[i,j]%n_colors]
		ax.imshow(color_mat, cmap="gray", interpolation="nearest")
		plt.save("Mandelbrot_static.png", dpi=300)
		plt.show()

	def iter_animate(self, ax, iter_times = 30, h=0.01, x0 = 0., y0 = 0., save=True):

		color_mat = np.zeros([self.N,self.M,3]) 
		img = ax.imshow(color_mat, cmap="gray", interpolation="nearest", extent = [-2,2,-2,2])
		text = ax.text(-1, 2.1, "")
		ax.set_yticks([])
		ax.set_xticks([])

		def init():
			img.set_data(np.zeros([self.N,self.M,3]))
			text.set_text("")
			return img, text

		def update(data):
			n, i = data
			text.set_text("iteration times = {}".format(i+1))
			for i in range(self.N):
				for j in range(self.M):
					color_mat[i,j] = colors[n[i,j]%n_colors]
			img.set_data(color_mat)
			return (text, img)
			
		def data_gen():
			for i in range(iter_times):
				print("iteration times = {}".format(i+1))
				n = np.array(Mand.iterate(self.N, self.M, i, h, x0, y0), dtype=int)[:]
				yield (n, i)

		anim = animation.FuncAnimation(fig, update, data_gen, init_func=init, interval=500)
		if save:
			anim.save('Mandelbrot_iter.gif', writer='imagemagick', fps=300)
		plt.show()

	def zoom_animate(self, ax, n_steps = 40, h0 = 0.01, x = -0.1648, y = -1.035 ,save = True):

		color_mat = np.zeros([self.N,self.M,3]) 
		img = ax.imshow(color_mat, cmap="gray", interpolation="nearest", extent = [-2,2,-2,2])
		ax.scatter(0, 0, s=100, facecolors='none', edgecolors='r')	
		text = ax.text(-2, 2.1, "")
		ax.set_yticks([])
		ax.set_xticks([])

		def init():
			img.set_data(np.zeros([self.N,self.M,3]))
			text.set_text("")
			return img, text

		def update(data):
			n, i, n_max, x, y = data
			text.set_text("iteration times = {0}; frames count = {1}; x, y = {2:.3f}, {3:.3f},".format(n_max, i, x, y))
			print("iteration times = {0}, frames count = {1}".format(n_max, i+1))
			for i in range(self.N):
				for j in range(self.M):
					color_mat[i,j] = colors[n[i,j]%n_colors]
			img.set_data(color_mat)
			return (text, img)
			
		def data_gen():
			scale_rate = 1.2
			h = h0
			for i in range(n_steps):
				h = h/scale_rate
				n_max = min(int(1/h),3000)
				n = np.array(Mand.iterate(self.N, self.M, n_max, h, x, y), dtype=int)[:]
				yield (n, i, n_max, x, y)

		# def save_figs():
		# 	for n, k, n_max, x, y in data_gen():
		# 		text.set_text("iteration times = {0}; frames count = {1}; x, y = {2:.3f}, {3:.3f},".format(n_max, k, x, y))
		# 		for i in range(self.N):
		# 			for j in range(self.M):
		# 				color_mat[i,j] = colors[n[i,j]%n_colors][:]
		# 		img.set_data(color_mat)
		# 		print("saving img {}...".format(k))
		# 		plt.savefig("./imgs/img{}.png".format(k), dpi=300)

		anim = animation.FuncAnimation(fig, update, data_gen, init_func=init, interval=500)
		print("saving animation...")
		if save:
			anim.save('Mandelbrot_zoom.gif', writer='imagemagick', fps = 100)
		# plt.show()
