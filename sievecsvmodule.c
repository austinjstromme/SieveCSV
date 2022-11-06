#define PY_SSIZE_T_CLEAN
#include <Python.h>

static PyObject*
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;
    if (!PyArg_ParseTuple(args, "s", &command)) {
        return NULL;
    }
    sts = system(command);
    return PyLong_FromLong(sts);
}

static PyMethodDef SpamMethods[] = {
    {"system", spam_system, METH_VARARGS, "Execute a shell command."},
    {NULL, NULL, 0, NULL}
};

PyDoc_STRVAR(spam_doc, "Module named spam");
static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    spam_doc,
    -1,
    SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void) {
    return PyModule_Create(&spammodule);
}

int
main(int argc, char *argv[]) 
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }
    if(PyImport_AppendInittab("spam", PyInit_spam) == -1) {
        fprintf(stderr, "Error: could not extend in-built modules table\n");
        exit(1);
    }

    Py_SetProgramName(program);
    Py_Initialize();
    PyObject *pmodule = PyImport_ImportModule("spam");
    if (!pmodule) {
        PyErr_Print();
        fprintf(stderr, "Error: could not import module 'spam'\n");
    }
    PyMem_RawFree(program);
    return 0;
}
