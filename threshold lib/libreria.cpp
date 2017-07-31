#define M 5000

#include <Python.h>
#include <vector>
#include <string>
using namespace std;

#define MODULE "th"
#define DESCRIPTION "transform a rgb image array to black and while depending of the threshold"

struct rgb{
    int r,g,b;
};

rgb num2rgb(int num){
    rgb a;
    a.r = num & 255;
    a.g = (num >> 8) & 255;
    a.b = (num >> 16) & 255;
	return a;
}

int rgb2num(rgb c){
    return c.r + (c.g << 8) + (c.b << 16);
}

int get_num(PyObject* obj, int x, int y){
    return (int)PyLong_AsLong( PyList_GetItem(PyList_GetItem(obj,x), y) );
}

void set_num(PyObject* obj, int x, int y, int value){
    PyObject *val = PyLong_FromLong( (long)value );
    PyList_SetItem( PyList_GetItem(obj,x), y , val);
}

static PyObject *funcion(PyObject *self, PyObject *args) {

	PyObject *txt;
	int length;
	int w,h;
	int th, margin;

    if (!PyArg_ParseTuple(args, "Oiiiii", &txt, &length, &w, &h, &th, &margin)) {
		return NULL;
	}

    int black = 0, avg = 0;

    for (int x = 0; x < w; x++){
        for (int y = 0; y < h; y++){
            rgb color = num2rgb( get_num(txt,x,y) );
            int r = color.r, g = color.g, b = color.b;
            avg = (r+g+b)/3;
            if (avg > th){
                avg = 255;
            }else{
                avg = 0;
                black ++;
            }

            if (x < margin){
                avg = 255;
            }
            if (x > w - margin){
                avg = 255;
            }
            if (y < margin){
                avg = 255;
            }
            if (y > h-margin){
                avg = 255;
            }

            rgb average;
            average.r = avg; average.g = avg; average.b = avg;
            set_num( txt, x, y, rgb2num(average) );
        }
    }

    return txt;
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
