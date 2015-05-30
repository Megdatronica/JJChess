#ifndef PIECE_H
#define PIECE_H

#include <string>
#include "constants.h"

// Piece object provides information about how to display a piece given its 
// type.
class Piece{

public:
    Piece(int, int);

    const int type;
    const bool isWhite;
    std::string display;

    void getDisplay();

private:
    const int displaySize;

};

#endif