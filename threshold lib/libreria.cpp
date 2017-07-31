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

struct point{
    int x, y, w, h;
    point(int X, int Y){
        x = X;
        y = Y;
        w = 0;
        h = 0;
    }
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

static PyObject *threshold(PyObject *self, PyObject *args) {

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

bool is_black(PyObject *arr, int x, int y){
    rgb act = num2rgb( get_num( arr, x, y ) );
    return (act.r == 0 && act.g == 0 && act.b == 0);
}

bool is_inside(vector<point> vec, point p){
    for (int x = 0; x < vec.size(); x++){
        point act = vec[x];
        if (act.x == p.x && act.y == p.y){
            return true;
        }
    }
    return false;
}

vector<point> analyse_letter(PyObject *arr, int sx, int sy, int w, int h){
    bool finished = false;
    vector<point> points;
    int x = sx, y = sy;
    while (!finished){
        bool detected = false;
        point cases[8] = {point(x,y+1), point(x,y-1), point(x+1,y-1), point(x+1,y), point(x+1,y+1), point(x-1,y-1), point(x-1,y), point(x-1,y+1)};
        for (int n = 0; n < 8; n++){
            if (is_black(arr,cases[n].x,cases[n].y)){
                if (!is_inside(points,cases[n])){
                    points.push_back(cases[n]);
                    x = cases[n].x;
                    y = cases[n].y;
                    detected = true;
                    break;
                }
            }
        }
        if (!detected){
            finished = true;
        }
    }
    return points;
}

static PyObject *get_letters(PyObject *self, PyObject *args) {
	PyObject *arr;
	int length;
	int w,h;

    if (!PyArg_ParseTuple(args, "Oiii", &arr, &length, &w, &h)) {
		return NULL;
	}

    int separation = 20;
    int y1 = 0, y2 = separation;
    vector< vector<point> > letters;
    while (y2 < h){
	    bool detected = false;
	    int maxy = y1;
	    for (int x = 0; x < w; x++){
	        if (is_black(arr,x,y1) || is_black(arr,x,y2)){
	            if (!is_black(arr,x,y1) && is_black(arr,x,y2)){
	                y1 = y2;
	                y2 = y1 + separation;
	            }
	            for (int x2 = x-10; x2 < x+10; x2++){
    	            if (is_black(arr,x2,y2)){
    	                detected = true;
    	                vector<point> a = analyse_letter(arr, x2, y1, w, h);
    	                int maxx = x;
    	                for (int n = 0; n < a.size(); n++){
    	                    maxx = a[n].x > maxx ? a[n].x : maxx;
    	                    maxy = a[n].y > maxy ? a[n].y : maxy;
    	                }
    	                x = maxx;
    	                if (a.size() > 0){
        	                letters.push_back(a);
    	                    printf("x:%i, y:%i, s:%i\n",x2,y1,a.size());
                        }
    	            }
                }
           }
	    }
        y1 = maxy+100;
        y2 = maxy+100+separation;
	}

    PyObject *LETTERS = PyList_New(0);
    for (int x = 0; x < letters.size(); x++){
        PyObject *LETTER = PyList_New(0);
        for (int y = 0; y < letters[x].size(); y++){
            PyObject *POINT = PyList_New(0);
            PyList_Append(POINT, PyLong_FromLong(letters[x][y].x));
            PyList_Append(POINT, PyLong_FromLong(letters[x][y].y));
            PyList_Append(LETTER, POINT);
        }
        PyList_Append(LETTERS,LETTER);
    }

    return LETTERS;
}

static PyMethodDef module_functions[] = {
	{ "threshold", (PyCFunction)threshold, METH_VARARGS, NULL },
	{ "get_letters", (PyCFunction)get_letters, METH_VARARGS, NULL },
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
