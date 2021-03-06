#include "/Users/xinchen/anaconda3/include/python3.5m/Python.h"
#include <math.h>
 
void iterate(int N, int M, int ** n, int n_max, double h, double x0, double y0);
void C_mat_gen(int N, int M, double *** C_mat, double x0, double y0, double h);
void show_array(int ** n, int N, int M);

void iterate(int N, int M, int **n, int n_max, double h, double x0, double y0)
{
	double ***C_mat;
	double ***Z_mat;
	int *passed;
	double z0,z1;
	int i, j, k;

	// malloc Z_mat
	Z_mat = (double ***) malloc(N*sizeof(double **));
	for(i = 0; i < N; i++){
		Z_mat[i] = (double **) malloc(M*sizeof(double *));
		for(j=0; j< M; j++){
			Z_mat[i][j] = (double *) malloc(2*sizeof(double));
			Z_mat[i][j][0] = 0;
			Z_mat[i][j][1] = 0;
		}
	}
	// malloc C_mat
	C_mat = (double ***) malloc(N*sizeof(double **));
	for(i = 0; i < N; i++){
		C_mat[i] = (double **) malloc(M*sizeof(double *));
		for(j=0; j< M; j++){
			C_mat[i][j] = (double *) malloc(2*sizeof(double));
		}
	}

	// malloc passed
	passed = (int *) malloc(N*M*sizeof(int));
	for(i = 0; i< N*M; i++) passed[i] = 0;


	// generates C_mat
	C_mat_gen(N, M, C_mat, x0, y0, h);

	for(k = 0; k<n_max; k++){
		for(i = 0; i<N; i++)
			for(j = 0; j<M; j++){
				if(passed[i*M+j]==1) continue;
				z0 = Z_mat[i][j][0];
				z1 = Z_mat[i][j][1];
				Z_mat[i][j][0] = C_mat[i][j][0] + z0*z0 - z1*z1;
				Z_mat[i][j][1] = C_mat[i][j][1] + 2*z0*z1;
				if( pow( Z_mat[i][j][0]*Z_mat[i][j][0]
						+Z_mat[i][j][1]*Z_mat[i][j][1], 0.5 ) >= 2.0){
					passed[i*M+j] = 1;
					n[i][j] = k+1;
				}
			}
	}
	free(Z_mat); free(C_mat); free(passed);
}

void C_mat_gen(int N, int M, double *** C_mat, double x0, double y0, double h)
{
	/* generates C matrix
	x0, y0: lower left coordinates
	N, M: dimensions of C matrix
	h: step size */
	int i, j;
	double c[2];
	for(i = 0; i<N; i++)
		for(j = 0; j<M; j++){
			c[0] = x0 + (j-(int)(M/2))*h;
			c[1] = y0 + ((int)(N/2)-i)*h;
			C_mat[i][j][0] = c[0];
			C_mat[i][j][1] = c[1];
		}
}


void show_array(int ** n, int N, int M)
{
	for(int i = 0; i<N; i++)
		for(int j = 0; j<M; j++){
			if(j==M-1)
				printf("%d\n", n[i][j]);
			else
				printf("%d,", n[i][j]);
		}
}
static PyObject * wraped_iterate(PyObject *self, PyObject *args)
{
	int n_max;
	int **n;
	double h, x0, y0;
	int N, M;
	int i, j;


    if (!PyArg_ParseTuple(args, "lllddd", &N, &M, &n_max, &h, &x0, &y0))
        return NULL;

	n = (int **) malloc(N*sizeof(int *));
	for(i = 0; i < N; i++){
		*(n+i) = (int *) malloc(M*sizeof(int));
		for(j = 0; j<M; j++)
			*(*(n+i)+j) = 0;
	}

    iterate(N, M, n, n_max, h, x0, y0);

	PyObject *res = PyList_New(N);
    for(i = 0; i<N; i++){
    	PyObject *inner_list = PyList_New(M);
    	for(j=0; j<M; j++){
    		PyList_SetItem( inner_list, j, PyLong_FromLong(n[i][j]) );
    	}
    	PyList_SetItem(res, i, inner_list);
    }
    free(n);
    return res;
}

// Methods table
static PyMethodDef MandMethods[] = {
    {
        "iterate", //method name
        wraped_iterate,  //method as C func
        METH_VARARGS,
        ""
    },
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef MandModule = {
  PyModuleDef_HEAD_INIT,

  "Mandelbrot",           /* name of module */
  "the Mandelbrot module",  /* Doc string (may be NULL) */
  -1,                 /* Size of per-interpreter state or -1 */
  MandMethods       /* Method table */
};

/* Module initialization function */
PyMODINIT_FUNC
PyInit_Mandelbrot(void) {
  return PyModule_Create(&MandModule);
} 















