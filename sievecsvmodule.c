#include <stdio.h>
void foo() {
    printf("ding dong");
}

// #define PY_SSIZE_T_CLEAN
// #include <Python.h>


// static PyObject*
// sievecsv_yeet(PyObject *self, PyObject *args) {
//     printf("what the fuck");
//     return PyLong_FromLong(20);
// }

// static PyMethodDef SieveCSVMethods[] = {
//     {"yeet", sievecsv_yeet, METH_VARARGS, "Yeet"},
//     {NULL, NULL, 0, NULL}
// };

// static struct PyModuleDef sievecsvmodule = {
//     PyModuleDef_HEAD_INIT,
//     "sievecsv",
//     NULL, // we don't have documentation.... yet. 
//     -1,
//     SieveCSVMethods
// }

// PyMODINIT_FUNC
// PyInit_sievecsv(void)
// {
//     return PyModule_Create(&sievecsvmodule);
// }

// int 
// main(int argc, char *argv[]) {
//     wchar_t *program = Py_DecodeLocale(argv[0], NULL);
//     if (program == NULL) {
//         fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
//         exit(1);
//     }

//     /* Add a built-in module, before Py_Initialize */
//     if (PyImport_AppendInittab("sievecsv", PyInit_sievecsv) == -1) {
//         fprintf(stderr, "Error: could not extend in-built modules table\n");
//         exit(1);
//     }

//     /* Pass argv[0] to the Python interpreter */
//     Py_SetProgramName(program);

//     /* Initialize the Python interpreter.  Required.
//        If this step fails, it will be a fatal error. */
//     Py_Initialize();

//     /* Optionally import the module; alternatively,
//        import can be deferred until the embedded script
//        imports it. */
//     PyObject *pmodule = PyImport_ImportModule("sievecsv");
//     if (!pmodule) {
//         PyErr_Print();
//         fprintf(stderr, "Error: could not import module 'sievecsv'\n");
//     }

//     PyMem_RawFree(program);
//     return 0;
// }