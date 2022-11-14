#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdarg.h>

struct CSV_Grid {
    char*** table;
    int rows;
    int cols;
};

typedef struct CSV_Grid CSV_Grid;

static const int DEBUG_MODE = 0;
static void debug_printf(const char* format, ...) {
    if (DEBUG_MODE != 0) {
        va_list args;
        va_start(args, format);
        vprintf(format, args);
        va_end(args);
    }
}

static const int MAX_ROWS = 128;
static const int MAX_COLS = 64;
static const int MAX_LEN_ENTRY = 64;


/*
Given a list of char* filters to match on, choose one of them to base
the raw filter on. Assign to filter_len the filter's length.
*/
static char* make_raw_filter(const char** filters, int* filter_len, int filter_count) {
    if (filters == NULL || filter_count == 0 || strlen(filters[0]) == 0) {
        return NULL;
    }

    // For now, just take the first filter in the sequence. 
    // If the length is >= 4, take first 4 characters. 
    // If the length is < 4, take the whole filter.
    char* raw_filter;
    if (strlen(filters[0]) < 4) {
        raw_filter = (char*) malloc(5 * sizeof(char));
        strncpy(raw_filter, filters[0], 5);
        *filter_len = strlen(filters[0]);
    } else {
        raw_filter = (char*) malloc(5 * sizeof(char));
        strncpy(raw_filter, filters[0], 4);
        *filter_len = 4;
    }
    return raw_filter;
}

/*
Given a char* representing a raw filter to use (whose length is filter_len), check
against file at its current pointer. Return 1 if it's a match
(meaning at the current position there might be a valid row by our filters) or 0 if not.

On returning, file's start should be moved back to where it was at the beginning of the
function. 

Assumes that each row will be much longer than our filter, or at least 8 characters per row.
*/
static const int apply_raw_filter(FILE* file, char* raw_filter, int filter_len) {
    // Currently I will not use SIMD. Goal will be to get it working without SIMD, 
    // then modify to use SIMD. 
    fpos_t old_start;
    fgetpos(file, &old_start);
    int ans = 1;
    for (int i = 0; i < filter_len; i++) {
        int current_char = fgetc(file);
        if (current_char == EOF) {
            ans = 0; // No character in file to correspond to.
            break;
        }
        if (current_char != (int) (raw_filter[i])) {
            ans = 0; // Current char in file doesn't match the filter.
            break;
        }
    }
    fsetpos(file, &old_start);
    return ans;
}

/*
Given file at current pointer, rewind to first character of row contains start of pointer. 
This is the character after the last newline before the start of the current pointer.
Returns the number of characters before the old start pointer to which the new start pointer is.
*/
static const long rewind_row_start(FILE* file) {
    long bytes_from_start = ftell(file);
    long bytes_backwards = 0;
    while (bytes_backwards < bytes_from_start) {
        fseek(file, -1 * sizeof(char), SEEK_CUR); // go one char backwards
        int next_char = fgetc(file); // read the char and move one forward
        if (next_char == '\n') {
            break;
        }

        fseek(file, -1 * sizeof(char), SEEK_CUR); // go backwards again
        bytes_backwards += 1;
    }
    return bytes_backwards;
}

/*
Given file at current pointer, which is assumed to be the start of a row,
return a char** which is a row if and only if it meets the constraints of col_idx and filters,
whose lengths are filter_count. If returning a row, should set col_count to number of columns in row.
Regardless, increment bytes_read with the number of bytes read for this row. 

"Constraints set" currently defined as using substring (if filters[i] is a substring of the entry at)
column col_idxs[i] of the row, then it is acceptable. 

If number of columns is > MAX_COLS, only returns the first MAX_COLS columns. Also disregards filters for columns after the first MAX_COLS columns. 

Assumes that '\n' represents end-of-line and terminates a row. 
Assumes that ',', if not surrounded by a pair of '\"', separates an entry from the next.
Assumes that '\"' aren't inside a pair of '\"' unless immediately preceded by a '\"'.
*/
static char** maybe_get_row(FILE* file, int* col_idxs, const char** filters, int filter_count, long* total_bytes_read, int* col_count) {
    long bytes_read = 0;
    *col_count = 0;
    char** maybe_row = (char**) malloc(MAX_COLS * sizeof(char*));

    // Read a row into memory. 
    // Represented as implicit state machine, where state is combination of
    // (1) cell, the current entry being parsed, (2) *col_count, the number of rows
    // read so far, (3) is_between_quotes, which is 0 if not and 1 if true.
    int is_between_quotes = 0;
    char* entry = (char*) malloc((MAX_LEN_ENTRY + 1)* sizeof(char));
    sprintf(entry, "");
    while (1 == 1) {
        int peek = fgetc(file);
        if (peek != EOF) {
            
            debug_printf("current row character %c\n", peek);
        } else {
            debug_printf("current row character is EOF\n");
        }
        bytes_read += 1;
        // If end-of-file or end-of-line, end row.
        // If there is still room for a column (based on MAX_COLS and *col_count), write entry to row and increment *col_count. 
        if (peek == EOF || peek == '\n') { 
            if (*col_count < MAX_COLS) {
                maybe_row[*col_count] = entry;
                debug_printf("before malloc here\n");
                entry = (char*) malloc((MAX_LEN_ENTRY + 1)* sizeof(char));
                sprintf(entry, "");

                debug_printf("after malloc here\n");
                if (entry == NULL) {
                    debug_printf("a null pointer has been allocated\n");
                } else {
                    debug_printf("not a null pointer has been allocated\n");
                }
                *col_count += 1;
                is_between_quotes = 0;
            }
            break;
        }
        // If ',' and not is_between_quotes, end entry. If there's still room for a column, write entry to row and increment *col_count. 
        if (peek == ',' && is_between_quotes == 0) {
            if (*col_count < MAX_COLS) {
                maybe_row[*col_count] = entry;
                entry = (char*) malloc((MAX_LEN_ENTRY + 1)* sizeof(char));
                sprintf(entry, "");
                *col_count += 1;
                is_between_quotes = 0;
            }
            continue;
        }
        // If '\"': 
        // - If is_between_quotes == 0, is_between_quotes = 1.
        // - If is_between_quotes != 0, read the next character.
        // -- If EOF or newline, end entry. If room for a column, write entry to row and increment
        //    *col_count.
        // -- If another '\"', write a single '\"' to entry if has space.
        // -- Else, is_between_quotes = 0, and put back the character.
        if (peek == '\"') {
            if (is_between_quotes == 0) {
                is_between_quotes = 1;
            } else {
                int other_peek = fgetc(file);
                bytes_read += 1;
                if (other_peek == EOF || other_peek == '\n') {
                    if (*col_count < MAX_COLS) {
                        is_between_quotes = 0;
                        maybe_row[*col_count] = entry;
                        entry = (char*) malloc((MAX_LEN_ENTRY + 1)* sizeof(char));
                        sprintf(entry, "");
                        *col_count += 1;
                        is_between_quotes = 0;
                    }   
                    break;
                } else if (other_peek == '\"') {
                    if (strlen(entry) < MAX_LEN_ENTRY) {
                        entry[strlen(entry) + 1] = '\0';
                        entry[strlen(entry)] = '\"';
                    }
                } else {
                    is_between_quotes = 0;
                    ungetc(other_peek, file);
                    bytes_read -= 1;
                }
            }
            continue;
        }
        // By default, copy in the character.
        if (strlen(entry) < MAX_LEN_ENTRY) {
            entry[strlen(entry) + 1] = '\0';
            entry[strlen(entry)] = peek;
        }
    }
    *total_bytes_read += bytes_read;
    int is_good_row = 1;
    debug_printf("filter_count %d\n", filter_count);
    for (int j = 0; j < filter_count; j++) {
        if (col_idxs[j] > MAX_COLS) {
            continue;
        }
        if (col_idxs[j] >= *col_count) { 
            is_good_row = 0;
            break;
        }
        const char* loc = strstr(maybe_row[col_idxs[j]], filters[j]);
        if (loc != NULL) {
            continue;
        } else {
            is_good_row = 0;
            break;
        }
    }
    if (is_good_row != 0) {
        // if it's a good row, return it.
        return maybe_row;
    } else {
        // else, return a null pointer
        // maybe also free 
        for (int i = 0; i < *col_count; i++) {
            free(maybe_row[i]);
        }
        free(maybe_row);
        return NULL;
    }

}

/*
Given the file at its current file pointer, reads the surrounding row(s), depending on what is covered
by the raw filter. 

Then, for each row, checks against all col_idxs and filters. 

If it all matches (exact value for each field in col_idxs), returns the row and sets col_count 
to the number of columns in the row. (If the row has > MAX_COLS columns, only return the first MAX_COLS. 
As a side-effect, if any col_idx is >= MAX_COLS, the corresponding filter is ignored.)

If the row doesn't match, returns null.

In either case, file's pointer should move to where its next row might be.
*/
static char*** maybe_get_rows(FILE* file, int* col_idxs, const char** filters, int filter_count,  int raw_filter_len, int* col_count, int* row_count) {
    long bytes_back = rewind_row_start(file);
    long bytes_to_read = bytes_back + raw_filter_len;
    if (raw_filter_len == 0) {
        bytes_to_read += 1;
    }
    char*** maybe_rows = (char***) malloc(MAX_ROWS * sizeof(char**));
    *row_count = 0;
    long bytes_read = 0;
    int max_col_count = 0;
    while (bytes_read < bytes_to_read && *row_count < MAX_ROWS) {
        int new_col_count;
        debug_printf("got to before maybe_get_row\n");
        char** maybe_row = maybe_get_row(file, col_idxs, filters, filter_count, &bytes_read, &new_col_count);
        debug_printf("bytes_read %d\n", bytes_read);
        debug_printf("ftell %ld\n", ftell(file));
        debug_printf("got to after maybe_get_row\n");
        if (maybe_row != NULL) {
            maybe_rows[*row_count] = maybe_row;
            *row_count += 1;
            if (new_col_count > max_col_count) {
                max_col_count = new_col_count;
            }
            debug_printf("max_col_count %d\n", max_col_count);
            for (int i = 0; i < max_col_count; i++) {
                debug_printf("entry[%d]: %s\n", i, maybe_row[i]);
            }
        }
    }

    *col_count = max_col_count;
    debug_printf("got to return of maybe_get_rows\n");
    return maybe_rows;
}


/*
Advance file's start pointer by 1 character. 
*/
static const void advance(FILE* file) {
    fseek(file, 1 * sizeof(char), SEEK_CUR);
}

/*
Given a filename, a list of column indices, and a list of strings, 
return a representation of all rows in the CSV named filename,
where, for i in [0, len(col_idxs)], the col_idxs[i]-th field is an exact match for filters[i].
*/
static const CSV_Grid parse(const char* filename, int* col_idxs, const char** filters, int filter_count) {
    // will return a grid of at most MAX_ROWS rows
    CSV_Grid grid;

    FILE* fp = fopen(filename, "rb");
    if (!fp) {
        return grid;
    }

    char*** table = (char***) malloc(MAX_ROWS * sizeof(char**));
    int raw_filter_len = 0;
    char* raw_filter = make_raw_filter(filters, &raw_filter_len, filter_count);
 
    int peeker; 
    int row_count = 0;
    int col_count = -1;

    while (row_count < MAX_ROWS) {
        peeker = fgetc(fp);
        if (peeker == EOF) {
            debug_printf("exiting due to end-of-file\n");
            break;
        }

        debug_printf("current character %c\n", peeker);
        ungetc(peeker, fp);
        if (apply_raw_filter(fp, raw_filter, raw_filter_len) != 0) {
            debug_printf("raw filter matches\n");
            int maybe_row_count;
            int new_col_count; 
            char*** maybe_rows = maybe_get_rows(fp, col_idxs, filters, filter_count, raw_filter_len, &new_col_count, &maybe_row_count);
            if (maybe_rows != NULL && maybe_row_count != 0) {
                for (int i = 0; i < maybe_row_count && row_count < MAX_ROWS; i++) {
                    table[row_count] = maybe_rows[i];
                    row_count += 1;
                }
                if (col_count == -1 || new_col_count > col_count) {
                    col_count = new_col_count; 
                }
            }
        } else {
            debug_printf("raw filter does not match\n");
            advance(fp); 
        }
        debug_printf("row_count %d MAX_ROWS %d\n", row_count, MAX_ROWS);
    } 
    if (ferror(fp)) {
        debug_printf("returning from fp with an error\n");
    } else {
        debug_printf("returning from fp with normal eof\n");
    }
    // in future, feof(fp) / ferror(fp) can check between end-of-file and error. for now, both return the same thing.

    grid.table = table;
    grid.rows = row_count;
    grid.cols = col_count;
    return grid;
}

PyObject* wrap_grid(CSV_Grid grid) {
    PyObject* py_grid = PyList_New(0);
    
    for (int i = 0; i < grid.rows; i++) {
        PyObject* row = PyList_New(0);
        for (int j = 0; j < grid.cols; j++) {
            if (grid.table == NULL || grid.table[i] == NULL || grid.table[i][j] == NULL) {
                PyList_Append(row, Py_None);
            } else {
                PyList_Append(row, PyUnicode_FromString(grid.table[i][j]));
            }
        }
        PyList_Append(py_grid, row);
    }
    return py_grid;
}

// static PyObject*
// SieveCSV_system(PyObject *self, PyObject *args)
// {
//    const char *command;
//    int sts;
//    if (!PyArg_ParseTuple(args, "s", &command)) {
//         return NULL;
//     }
//    sts = system(command);
//    return PyLong_FromLong(sts);
// }

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

    PyObject* ret_val = wrap_grid(parse(filename, col_idxs, filters, col_size));
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
