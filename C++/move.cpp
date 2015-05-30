#include "move.h"
#include <cmath>
#include <iostream>


extern const int CASTLE_KINGS_SIDE = 100;
extern const int CASTLE_QUEENS_SIDE = 200;


Move::Move() {}


Move::Move(int fromX, int fromY, int toX, int toY) : fromX(fromX), fromY(fromY),
                                                     toX(toX), toY(toY) 
{
    fromSquare = fromY * BOARD_SIZE + fromX;
    toSquare = toY * BOARD_SIZE + toX;

    castleSide = -1;
}


Move::Move(int fromSquare, int toSquare) : fromSquare(fromSquare), 
                                           toSquare(toSquare)
{
    fromX = fromSquare % BOARD_SIZE;
    fromY = fromSquare / BOARD_SIZE;

    toX = toSquare % BOARD_SIZE;
    toY = toSquare / BOARD_SIZE;

    castleSide = -1;
}


Move::Move(bool playerColour, int side) : playerColour(playerColour), 
                                          castleSide(side)
{
    // Set public ints to -1 so that program will crash if anyone actually
    // tries to use them
    fromX = -1;
    fromY = -1;
    fromSquare = -1;
    toX = -1;
    toY = -1;
    toSquare = -1;
}


bool Move::isCastle() {
    return(castleSide == CASTLE_QUEENS_SIDE || castleSide == CASTLE_KINGS_SIDE);
}


bool Move::isCastle(bool &isWhite, int &side) {
    if (castleSide == CASTLE_QUEENS_SIDE || castleSide == CASTLE_KINGS_SIDE) {
        isWhite = playerColour;
        side = castleSide;
        return true;
    }
    return false;
}
