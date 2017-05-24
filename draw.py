import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools as it
import Mandelbrotset as Mand


true_color = True
(N, M) = (450, 450)


def static_draw(ax, colors, n_max=10):
	h = 0.01
	x0 = -2.2
	y0 = -2.2
	n = Mand.iterate(n_max, h, x0, y0)
	color_mat = np.zeros([N,M,3])
	for i in range(N):
		for j in range(M):
			color_mat[i,j] = colors[n[i,j]][:3] if true_color else colors[n[i,j]]
	ax.set_xticks([])
	ax.set_yticks([])
	ax.imshow(color_mat, cmap="gray", interpolation="nearest")
	plt.show()



def iter_animate(fig, ax, iter_times = 10):
	extent = [-2.2, 2.2, -2.2, 2.2]
	color_mat = np.zeros([N,M,3]) 
	if true_color:
		colors = [np.array([0.6,1,0.4])*x for x in np.tanh(np.linspace(0,3,iter_times+1))]
	gray_scale = np.linspace(0, 1, iter_times+1)
	img = ax.imshow(color_mat, cmap="gray", interpolation="nearest", extent=extent)
	text = ax.text(1.1, 2.3, "")
	h = 0.01
	x0 = -2.2
	y0 = -2.2

	def init():
		pass
	def update(data):
		n, i = data
		text.set_text("iteration times = {}".format(i+1))
		for i in range(N):
			for j in range(M):
				color_mat[i,j] = colors[n[i,j]][:3] \
					if true_color else gray_scale[n[i,j]]
		img.set_data(color_mat)
		return (text, img)
		
	def data_gen():
		for i in range(iter_times):
			print("iteration times: {}".format(i))
			# result = check_output(["gcc Mandelbrot.c -o mand"])
			result = check_output(["./mand", str(i), str(h), str(x0), str(y0)])
			n = np.loadtxt("result.csv", delimiter=",", dtype=int)
			yield (n, i)


	anim = animation.FuncAnimation(fig, update, data_gen, init_func=init, interval=1000)
	anim.save('Mandelbrot_colored2.gif', writer='imagemagick', fps=300)
	plt.show()

def zoom_in_animate(fig, ax):
	h = 0.01
	v_trans = np.array([-0.5, 0])
	scale_rate = 0.5





if __name__=="__main__":
	# n_max = 50
	fig, ax = plt.subplots(ncols=1, figsize=[9,9])
	# colors1 = [np.array([0.2,1,0])*x for x in np.linspace(0,1,n_max+1)]
	colors2 = [np.array([0.6,1,0.4])*x for x in np.tanh(np.linspace(0,3,n_max+1))]
	# static_draw(ax1, colors1, n_max=n_max)
	static_draw(ax2, colors2, n_max=n_max)
	# plt.savefig("Mandelbrot_wine.png", dpi = 300)
	# plt.show()
	iter_animate(fig, ax, iter_times=30)
