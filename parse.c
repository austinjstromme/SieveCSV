#include <stdlib.h>
#include <stdio.h>
#include "parse.h"

const CSV_Grid parse(const char* filename, int* col_idxs, const char** filters) {
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