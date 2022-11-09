#define PY_SSIZE_T_CLEAN
#include <Python.h>

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

    // PyObject* tbr = Py_BuildValue("[i,i, s, s]", col_idxs[0], col_idxs[1], filters[0], filters[1]);

    free(col_idxs);
    free(filters);
 
    // return tbr;

    return PyUnicode_FromString(filename);
    // parse inputs from python
    // pass to internal_parse
    // get result from internal_parse
    // pass to output_wrapper
    // return
}

// typedef struct SieveCSVOutput {
//     // TODO, but oonly knowable after starting
//     // file pointer
// }

// static SieveCSVOutput* internal_parse(const char* filename, int* col_idxs, const char** filters) {
//     return NULL;
// }

// static PyObject* output_wrapper(SieveCSVOutput* internal_iterator) {
//     return NULL;
// }

static PyMethodDef SieveCSVMethods[] = {
//    {"system", SieveCSV_system, METH_VARARGS, "Execute a shell command."},
    {"parse_csv", SieveCSV_parse, METH_VARARGS |  METH_KEYWORDS, "Parse a CSV file and return an iterator."},
    {NULL, NULL, 0, NULL}
};

//PyDoc_STRVAR(spam_doc, "Module named spam");
static struct PyModuleDef SieveCSVmodule = {
    PyModuleDef_HEAD_INIT,
    "SieveCSV",
    "An example Python C extension module",
    -1,
    SieveCSVMethods
};

PyMODINIT_FUNC
PyInit_SieveCSV(void) {
    return PyModule_Create(&SieveCSVmodule);
}

//int
//main(int argc, char *argv[]) 
//{
//    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
//    if (program == NULL) {
//        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
//        exit(1);
//    }
//    if(PyImport_AppendInittab("SieveCSV", PyInit_SieveCSV) == -1) {
//        fprintf(stderr, "Error: could not extend in-built modules table\n");
//        exit(1);
//    }
//
//    Py_SetProgramName(program);
//    Py_Initialize();
//    PyObject *pmodule = PyImport_ImportModule("SieveCSV");
//    if (!pmodule) {
//        PyErr_Print();
//        fprintf(stderr, "Error: could not import module 'SieveCSV'\n");
//    }
//    PyMem_RawFree(program);
//   return 0;
//}
