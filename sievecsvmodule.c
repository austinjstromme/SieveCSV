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

    if (!PyArg_ParseTuple(args, "s(i)(s)", &filename, &col_idxs, &filters)) {
        return NULL;
    }
    
    printf("%s\n", filename);
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

>>>>>>> 1628ac1e4039e798f651534f3fee6e45ea1055f1
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
