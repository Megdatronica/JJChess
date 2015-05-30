#ifndef GAME_STATE_H
#define GAME_STATE_H


#include "constants.h"
#include "board.h"
#include <string>


class GameState {

public:

    // Calls initVariables().
    GameState();


    // Fills the array movePoints with available legal squares for the piece at
    // squareValue to move to.
    //
    // Inputs:
    // int squareValue:          Grid reference of location of piece to be moved
    // bool playerColour:        True if piece at squareValue is white
    //
    // Outputs:
    // int* movePoints:   Pointer to an array which will be filled with ints 
    //                    0-63 (or castling ints) representing the available 
    //                    squares for the piece to move
    //
    // Returns:
    // int:			   Number of squares put into movePoints
    int getPieceMoves(bool playerColour, int squareValue, int* movePoints)
        const;


    // Returns an array with available legal moves (all pieces) for the team
    // of the passed colour. The int numMoves will be set to the number of moves
    // in the returned array.
    //
    // Note that the returned array must be deleted by the caller.
    Move* getPlayerMoves(bool playerColour, int &numMoves) const;


    // Changes the state of the game to reflect the passed move being made, and 
    void makeMove(Move &move);


    // Calls board.promotePawn to the given piece type.
    void promotePawn(int piece);


    // True if the current player can promote a pawn
    bool canPromotePawn();


    // Should be called after a move has been made.
    // Returns:
    // 0:      Nothing to report. Continue play.
    // 1/-1:   The move has caused the white/black player to be in check.
    // 2/-2:   White/black has won
    // 3:      The game has been drawn by stalemate
    // 4:      The fifty-move limit has been reached and the game has been drawn
    // 5:      Only the two kings remain; game is drawn
    int getStatus();


    // Changes whose turn it is
    void swapTurn();


    // Returns a representation of the passed move as a string in short
    // algebraic notation (ignoring check or checkmate). Note that this should
    // be called BEFORE the move has been made.
    std::string getSAN(Move &move);


    bool isWhiteTurn;   // True if it is currently white's turn.
    int moveCount;    // Number of player moves (not 'full' moves)

    Board board;       // Contains the state of the game

private:

    // Sets all counts to zero and sets all bools to relevant initial value
    void initVariables();


    // For the passed move, updates the relevant variables of this instance of 
    // Game: whiteCanCastleKSide, blackCanCastleQSide, moveCount,
    // fiftyMoveRuleCount, and so on. Will do this even if the move is a castle
    // move.
    //
    // Sould only be called when the move has been definitively chosen to be 
    // made, but HAS NOT BEEN MADE YET.
    void updateCounts(Move &move);


    // Returns true if the game board is in check for the passed colour.
    bool isInCheck(bool playerColour) const;


    // For the team of the passed colour, returns false if the king or the 
    // king's rook have moved at some previous point.
    bool couldCastleKingsSide(bool playerColour) const;


    // For the team of the passed colour, returns false if the king or the
    // queen's rook have moved at some previous point.
    bool couldCastleQueensSide(bool playerColour) const;


    // If the piece at squareValue is a pawn and can take another pawn via en
    // passant, the function returns true and fills moveValue with the square
    // that can be taken
    bool canPassant(bool playerColour, int squareValue, int &moveValue) const;


    // Returns true if the passed move is allowed
    bool isLegalMove(Move &move) const;



    bool whiteCanCastleKSide, whiteCanCastleQSide;
    bool blackCanCastleKSide, blackCanCastleQSide;

    // Contains an int representing the square just behind a pawn that was just
    // moved, which can be 'taken' by another pawn
    int enPassantVal;

    // Number of player moves without a take or a pawn move
    int   fiftyMoveRuleCount;

};


#endif