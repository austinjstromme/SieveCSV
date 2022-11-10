#include <Python.h>
#include "parse.h"

const PyObject* wrap_grid(CSV_Grid grid) {
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