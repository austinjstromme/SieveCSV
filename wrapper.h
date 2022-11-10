#ifndef WRAPPER_H_
#define WRAPPER_H_

#include <Python.h>
#include "parse.h"
const PyObject* wrap_grid(CSV_Grid grid);
#endif 