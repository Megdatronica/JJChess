#ifndef MOVE_H
#define MOVE_H

#include "constants.h"

extern const int CASTLE_KINGS_SIDE;
extern const int CASTLE_QUEENS_SIDE;

// Contains the initial and final position of a piece during a move,
// and information about whether the move is a castle move
class Move{

public:

    // Will initialise no values
    Move();


    // Inputs:
    // from_x, from_y:     current grid position of piece on board
    // to_x, to_y:         final grid position of piece after move has been made
    Move(int fromX, int fromY, int toX, int toY);


    // Inputs:
    // fromSquare:       current grid position of piece on board
    // toSquare:         final grid position of piece after move has been made
    //
    // Both inputs should be between 0 and 63, where for column x and row y,
    // index = y*BOARD_SIZE + x
    Move(int fromSquare, int toSquare);


    // Inputs:
    // playerColour:     true if move is being made by white
    // side:             equal to either CASTLE_QUEENS_SIDE or CASTLE_KINGS_SIDE
    //
    // This constructor is ONLY used for castling moves
    Move(bool playerColour, int side);


    // Returns true if the move is a castling move
    bool isCastle();


    // If move is a castling move, returns true and fills passed parameters with
    // details.
    // Outputs:
    //     isWhite:      will be true if player making castle is white
    //     side:         either CASTLE_KINGS_SIDE or CASTLE_QUEENS_SIDE
    //
    // Returns true if move is a castle move. If this function returns false, 
    // isWhite and side will be unchanged.
    bool isCastle(bool &isWhite, int &side);

    // Current location of piece on board: x value, y value and single value
    int fromX, fromY, fromSquare;

    // Location piece is moving to on board: x value, y value and single value
    int toX, toY, toSquare;

private:

    bool playerColour;      // True if player making move is white
    int castleSide;         // Either CASTLE_KINGS_SIDE or CASTLE_QUEENS_SIDE

};


#endif