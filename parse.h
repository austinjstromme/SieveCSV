#ifndef PARSE_H_
#define PARSE_H_

const int MAX_ROWS = 1024;
const int MAX_COLS = 32; 
const int MAX_CHARS_IN_CELL = 64;

struct CSV_Grid {
    char*** table;
    int rows;
    int cols;
};

typedef struct CSV_Grid CSV_Grid;
const CSV_Grid parse(const char* filename, int* col_idxs, const char** filters);
#endif 