#ifndef CONSTANTS_H
#define CONSTANTS_H

const int BOARD_SIZE = 8;

const bool WHITE = true;
const bool BLACK = false;

const int WHITE_KING = 1;
const int WHITE_QUEEN = 2;
const int WHITE_BISHOP = 3;
const int WHITE_KNIGHT = 4;
const int WHITE_ROOK = 5;
const int WHITE_PAWN = 6;

const int BLACK_KING = -1;
const int BLACK_QUEEN = -2;
const int BLACK_BISHOP = -3;
const int BLACK_KNIGHT = -4;
const int BLACK_ROOK = -5;
const int BLACK_PAWN = -6;

const int WHITE_CHECK = 1;
const int BLACK_CHECK = -1;
const int WHITE_WIN = 2;
const int BLACK_WIN = -2;
const int STALEMATE = 3;
const int FIFTY_MOVE_DRAW = 4;
const int KING_DRAW = 5;

#endif