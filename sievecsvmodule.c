#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "parse.h"
#include "wrapper.h"

static PyObject*
SieveCSV_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;
    if (!PyArg_ParseTuple(args, "s", &command)) {
        return NULL;
    }
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyObject*
SieveCSV_parse(PyObject *self, PyObject *args) {
    const char *filename;
    int* col_idxs;
    const char **filters;
    char err_buf[500];

    PyObject *colraw;
    PyObject *filtraw;

    if (!PyArg_ParseTuple(args, "sOO", &filename, &colraw, &filtraw)) {
        return NULL;
    }

    if(!PyList_Check(colraw) || !PyList_Check(filtraw)) {
        PyErr_SetString(PyExc_TypeError, "column and filter must be lists");
        return NULL;
    }

    int col_size = PyList_Size(colraw);
    int filt_size = PyList_Size(filtraw);
    if(filt_size != col_size) {
        sprintf(err_buf, "column and filter must be different lengths (currently %i and %i)", col_size, filt_size);
        PyErr_SetString(PyExc_IndexError, err_buf);
        return NULL;
    }
    
    col_idxs = malloc(col_size * sizeof(int));
    filters = malloc(col_size * sizeof(char *));
    for(int i = 0; i < col_size; i++) {
	    PyObject *col_idx = PyList_GetItem(colraw, i);
	    PyObject *filter = PyList_GetItem(filtraw, i);
        if(!PyLong_Check(col_idx)) {
            sprintf(err_buf, "column entry at index %i was not an integer", i);
            PyErr_SetString(PyExc_TypeError, err_buf);
            return NULL;
        }
        if(!PyUnicode_Check(filter)) {
            sprintf(err_buf, "filter entry at index %i was not a string", i);
            PyErr_SetString(PyExc_TypeError, err_buf);
            return NULL;
        }
        col_idxs[i] = (int) PyLong_AsLong(col_idx);
        filters[i] = PyUnicode_AsUTF8AndSize(filter, NULL);
    }

    // PyObject* ret_val = wrap_grid(parse(filename, col_idxs, filters));
    free(col_idxs);
    free(filters);
    return PyLong_FromLong(69);
}

static PyMethodDef SieveCSVMethods[] = {
    {"parse_csv", SieveCSV_parse, METH_VARARGS |  METH_KEYWORDS, "Parse a CSV file and return an iterator."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef SieveCSVmodule = {
    PyModuleDef_HEAD_INIT,
    "SieveCSV",
    "A C++ Python extension module for fast parsing.",
    -1,
    SieveCSVMethods
};

PyMODINIT_FUNC
PyInit_SieveCSV(void) {
    return PyModule_Create(&SieveCSVmodule);
}
