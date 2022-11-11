#define PY_SSIZE_T_CLEAN
#include <Python.h>

const int MAX_ROWS = 1024;
const int MAX_COLS = 32; 
const int MAX_CHARS_IN_CELL = 64;

struct CSV_Grid {
    char*** table;
    int rows;
    int cols;
};

typedef struct CSV_Grid CSV_Grid;

static const CSV_Grid parse(const char* filename, int* col_idxs, const char** filters) {
    // this is mostly filler to generate a random grid
    CSV_Grid grid;
    const int ROWS = 10;
    const int COLS = 5;
    const int MAX_LEN = 20;
    char*** table = (char***) malloc(ROWS * sizeof(char**));
    for (int i = 0; i < ROWS; i++) {
        table[i] = (char**) malloc(COLS * sizeof(char*));
        for (int j = 0; j < COLS; j++) {
            table[i][j] = (char*) malloc(MAX_LEN * sizeof(char));
            sprintf(table[i][j], "row%dcol%d", i, j);
        }
    }
    grid.rows = ROWS;
    grid.cols = COLS;
    grid.table = table;
    return grid;
}

PyObject* wrap_grid(CSV_Grid grid) {
    PyObject* py_grid = PyList_New(0);
    for (int i = 0; i < grid.rows; i++) {
        PyObject* row = PyList_New(0);
        for (int j = 0; j < grid.cols; j++) {
            if (grid.table[i][j] == NULL) {
                PyList_Append(row, Py_None);
            } else {
                PyList_Append(row, PyUnicode_FromString(grid.table[i][j]));
            }
        }
        PyList_Append(py_grid, row);
    }
    return py_grid;
}

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

    PyObject* ret_val = wrap_grid(parse(filename, col_idxs, filters));
    free(col_idxs);
    free(filters);
    return ret_val;
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
