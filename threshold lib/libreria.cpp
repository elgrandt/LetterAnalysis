#include <Python.h>

#define MODULE "th"
#define DESCRIPTION "transform a rgb image array to black and while depending of the threshold"

static PyObject *funcion(PyObject *self, PyObject *args) {

	char *obj_array;
	int w,h;
	int th, margin;

	/* MI FUNCION */
    if (!PyArg_ParseTuple(args, "siiii", &obj_array, &w, &h, &th, &margin)) {
		return NULL;
	}

	Py_RETURN_NONE;
}

static PyMethodDef module_functions[] = {
	{ "threshold", (PyCFunction)funcion, METH_VARARGS, NULL },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef moduledef = {
	PyModuleDef_HEAD_INIT,
	MODULE,              /* m_name */
	DESCRIPTION,         /* m_doc */
	-1,                  /* m_size */
	module_functions,    /* m_methods */
	NULL,                /* m_reload */
	NULL,                /* m_traverse */
	NULL,                /* m_clear */
	NULL,                /* m_free */
};

PyMODINIT_FUNC PyInit_th(void){
	return PyModule_Create(&moduledef);
}
