#ifndef BOARD_H
#define BOARD_H

#include <string>
#include "constants.h"
#include "move.h"
#include "piece.h"


const int INVALID_SQUARE = -10;

// Upper limit on the number of positions that a piece could be able to move to
// (number of spaces that a queen in the centre of a blank board has available)
const int MAX_PIECE_MOVES = 4 * (BOARD_SIZE - 1);

// Greastest possible number of moves a player can make.
// Source: https://chessprogramming.wikispaces.com/Chess+Position.
const int MAX_AVAILABLE_MOVES = 218;

const int RIGHT = 1;
const int LEFT  = -1;
const int UP    = 1;
const int DOWN  = -1;


// Stores the arrangement of the pieces on a board, and determines the legality 
// of moves.
class Board {

public:

    // Set the values of board::grid to the initial arrangement for the 
    // beginning of a game
    void setUp();


    // Changes the state of the board to reflect the passed move being made.
    // The universe may explode if it is not passed a legal move.
    void makeMove(Move &move);


    // Returns the piece at (x, y). If there is no piece, returns 0. If (x, y)
    // is not a valid square on the board, returns -10.
    int getPiece(int x, int y) const;


    // Returns the piece at the square represented by squareValue (should equal
    // y*BOARD_SIZE + x). If squareValue is not a valid square on the board,
    // will return -10.
    int getPiece(int squareValue) const;


    // A move is POSSIBLE if it takes a piece to a square that:
    //    - exists on the board, and
    //    - does not contain another piece of the same colour.
    // 
    // A castling move is considered POSSIBLE if the king and rook are in the
    // correct position and the space between them is empty.
    bool isPossibleMove(Move &move) const;


    // A move is VALID if, after the move has been made, the King of the player
    // who made it in not in check.
    //
    // A castling move is VALID if by making it, the king does not castle into,
    // out of, or through check.
    bool isValidMove(Move &move) const;


    // A castling move is considered POSSIBLE if the king and rook are in the
    // correct position and the space between them is empty.
    bool isPossibleCastleMove(bool playerColour, int side) const;


    // A castling move is VALID if by making it, the king does not castle into,
    // out of, or through check. Note that this function will return true if a 
    // castling move is valid, regardless of whether the king/rook has already 
    // moved.
    bool isValidCastleMove(bool playerColour, int side) const;


    // Returns true if move is possible and valid.
    //
    // Note that this function will return true if a castling move is valid,
    // regardless of whether the king/rook has already moved.
    bool isPossibleValidMove(Move &move) const;


    // If the passed move is an en Passant move, returns true and sets
    // enPassantVal to the value of the square with the pawn to be taken.
    bool Board::isPassantMove(Move &move, int &enPassantVal) const;


    // Fills the array movePoints with available squares for the piece at 
    // squareValue, excluding castling.
    //
    // Inputs:
    // int squareValue:          Grid reference of location of piece to be moved
    // bool playerColour:        True if piece at squareValue is white
    //
    // Outputs:
    // int* movePoints:   Pointer to an array which will be filled with ints 
    // 0-63 representing the available squares for the piece to move
    //
    // Returns:
    // int:			   Number of squares put into movePoints
    int getPieceMoves(bool playerColour, int squareValue, int* movePoints)
        const;


    // If the passed move moves a king, returns true and fills &piece with the
    // value of the piece (+-1). Note that this function WILL also return true
    // for castling moves.
    bool isKingMove(Move &move, int &piece) const;


    // If the passed move moves a rook, returns true and fills &piece with the
    // value of the piece (+-5). Note that this function will NOT return true
    // for castling moves.
    bool isRookMove(Move &move, int &piece) const;


    // If the passed move moves a pawn, returns true and fills &piece with the
    // value of the piece (+-6).
    bool isPawnMove(Move &move, int &piece) const;


    // If the passed move moves a pawn two squares forward, returns true and
    // fills &piece with the value of the piece (+-6) and also fills
    // enPassantVal with the value of the square directly behind the pawn (the
    // square which can be taken by another pawn). If this function returns
    // false, enPassantVal is unchanged.
    bool isDoublePawnMove(Move &move, int &piece, int &enPassantVal) const;


    // Returns true if move takes one piece to another piece of the opposite 
    // colour
    bool isTake(Move &move) const;


    // Returns true if playerColour (white or black) is in check. Note that this
    // will return true if the king is in check from the enemy king, even though
    // this can never legally happen
    bool isInCheck(bool playerColour) const;


    // Returns true if playerColour (white or black) has won the game
    bool hasWon(bool playerColour) const;


    // Returns true if the board contains only the black and the white king
    bool isKingDraw() const;


    // Returns true if some piece of the passed player colour can legally move
    // (ie, returns false if stalemate)
    bool legalMoveExists(bool playerColour) const;


    // Returns true if the player of the passed colour can promote a pawn
    bool canPromotePawn(bool playerColour) const;


    // Will promote exactly one pawn of the passed colour, by replacing it with
    // the passed piece. Returns false if there are no pawns suitable to promote
    bool promotePawn(bool playerColour, int piece);


    // Prints a basic pictorial representation of the board to the console from
    // white's point of view
    void printToConsole();


    // Returns a basic pictorial representation of the board to from white's
    // point of view
    std::string getPictorial();


    // Returns a string object which represents the current state of the board
    // in Forsyth-Edwards notation (without any additional characters for
    // castling availablility or player turn).
    std::string getForsyth();


    // Returns a representation of the passed move as a string in short
    // algebraic notation (ignoring check or checkmate).  Note that this should
    // be called BEFORE the move has been made.
    std::string getSAN(Move &move);

private:

    // Returns a string representing the name of the file represented by the
    // passed int (eg 'a')
    static std::string xToStr(int x);


    // Returns a string representing the name of the rank represented by the
    // passed int (eg '1')
    static std::string yToStr(int y);


    // Returns a string representing the grid reference of the passed value in
    // algebraic notation (eg g5, b2 etc)
    static std::string squareToStr(int x, int y);


    // If the passed move could be made by another piece of the same type,
    // returns a string of characters (rank or file or both) which should be 
    // added to the string representing the move in algebraic notation.
    // Inputs:
    //     Move move:    should be a move which is NOT a pawn move
    std::string getClarificationStr(Move &move);


    // Places a piece of given type onto the board at given (x, y) position, 
    // and returns true if there was a piece there already.
    // Inputs :
    //     int x, y : Position of the square on which to place the piece
    //     int piece : Type of piece to place
    bool placePiece(int x, int y, int piece);


    // Removes any pieces from the board at given (x, y) position, and returns
    // true if there was a piece there.
    bool removePiece(int x, int y);


    // Returns true if the move is for a white piece, false if it is for a black
    // piece or is undefined. Note that this function should never be passed a
    // move which undefined (the starting square of the move does not contain a
    // piece).
    bool isWhiteMove(Move &move) const;


    // Calculates all available squares for a king at the given square to move 
    // to (excluding castling). Fills the passed array with ints 0 - 63
    // representing these squares.
    // 
    // Inputs:
    // int x, y : values of the square where the king is
    // bool colour : true if the king is white
    //
    // Outputs :
    // int* movePoints : array which will be filled with available moves
    //
    // Returns:
    // int:      count of the number of entries put into movePoints
    int getKingMoves(int x, int y, bool colour, int* movePoints) const;


    // Calculates all available squares for a queen at the given square to move 
    // to. Fills the passed array with ints 0 - 63 representing these squares.
    // Inputs:
    // int x, y : values of the square where the piece is
    // bool colour : true if the piece is white
    //
    // Outputs :
    // int* movePoints : array which will be filled with available moves
    //
    // Returns:
    // int:      count of the number of entries put into movePoints
    int getQueenMoves(int x, int y, bool isWhite, int* movePoints) const;


    // Calculates all available squares for a bishop at the given square to move
    // to. Fills the passed array with ints 0 - 63 representing these squares.
    // Inputs:
    // int x, y : values of the square where the piece is
    // bool colour : true if the piece is white
    //
    // Outputs :
    // int* movePoints : array which will be filled with available moves
    //
    // Returns:
    // int:      count of the number of entries put into movePoints
    int getBishopMoves(int x, int y, bool isWhite, int* movePoints) const;


    // Calculates all available squares for a knight at the given square to move 
    // to. Fills the passed array with ints 0 - 63 representing these squares.
    // Inputs:
    // int x, y : values of the square where the piece is
    // bool colour : true if the piece is white
    //
    // Outputs :
    // int* movePoints : array which will be filled with available moves
    //
    // Returns:
    // int:      count of the number of entries put into movePoints
    int getKnightMoves(int x, int y, bool isWhite, int* movePoints) const;


    // Calculates all available squares for a rook at the given square to move 
    // to. Fills the passed array with ints 0 - 63 representing these squares.
    // Inputs:
    // int x, y : values of the square where the piece is
    // bool colour : true if the piece is white
    //
    // Outputs :
    // int* movePoints : array which will be filled with available moves
    //
    // Returns:
    // int:      count of the number of entries put into movePoints
    int getRookMoves(int x, int y, bool isWhite, int* movePoints) const;


    // Calculates all available squares for a pawn at the given square to move 
    // to. Fills the passed array with ints 0 - 63 representing these squares.
    // Inputs:
    // int x, y : values of the square where the piece is
    // bool colour : true if the piece is white
    //
    // Outputs :
    // int* movePoints : array which will be filled with available moves
    //
    // Returns:
    // int:      count of the number of entries put into movePoints
    int getPawnMoves(int x, int y, bool isWhite, int* movePoints) const;


    // Given a starting location and a direction, moves along the board and 
    // outputs the first piece it finds, returning a count of empty squares 
    // covered.
    // 
    // Inputs:
    // int x, y:         location of piece (will not be included in search)
    // int upDown:       -1 if down or diagonally down; +1 if up or diagonally
    //                   up; 0 otherwise
    // int leftRight:    -1 if left or diagonally left; +1 if right or
    //                   diagonally right; 0 otherwise
    //
    // Outputs:
    // int &piece:       will be filled with value of first piece found, or 0 if
    //                   search reached edge of board without finding a piece
    //
    // Returns:
    // int count:        count of number of squares covered, EXCLUDING the one
    //                   where it found a piece
    //
    // If input square is invalid, or if both upDown and leftRight are 0, then 
    // it will return 0 and &piece will be given a value of 0.
    int searchDirection(int x, int y, int upDown, int leftRight, int &piece)
        const;


    // Given a piece's location and a direction, moves along the board and 
    // returns the first piece it finds, outputting a count of squares covered
    // and filling the passed array with ints 0-63 representing the possible 
    // legal moves.
    //
    // Inputs:
    // int x, y:         location of piece (will not be included in search)
    // int upDown:       -1 if down or diagonally down; +1 if up or diagonally 
    //                   up; 0 otherwise
    // int leftRight:    -1 if left or diagonally left; +1 if right or 
    //                   diagonally right; 0 otherwise
    // bool isWhite:     true if piece to be moved is white
    //
    // Outputs:
    // int * movePoints:   will be filled, starting from movePoints[count], with
    //                     ints 0-63 representing possible moves for the piece
    // int &count:         will be incremented by the number of moves put into
    //                     movePoints
    // 
    // Returns:
    // int piece:        value of first piece found, or 0 if search reached edge
    //                   of board without finding a piece
    // 
    // It will return 0, and give &piece a value of 0, if one of the following 
    // is true:
    //  - upDown == leftRight == 0
    //  - The input x, y index is not a valid square
    int searchDirection(int x, int y, int upDown, int leftRight,
        bool isWhitePiece, int *movePoints, int &count) const;


    // Applies the passed castling move to the board. Will do nothing if move is
    // not a castling move.
    void castle(Move &move);


    // Returns true if the square (NOT the piece) at grid[x][y] is white
    static bool isWhiteSquare(int x, int y);


    // Contains the state of the board. Each entry is either 0 for no pieces or
    // WHITE_KING, BLACK_QUEEN etc
    int grid[BOARD_SIZE][BOARD_SIZE];
};


#endif