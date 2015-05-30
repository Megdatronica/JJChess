#include "board.h"
#include <cmath>
#include <iostream>


void Board::setUp() {

    // Clear board
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            grid[i][j] = 0;
        }
    }

    // Place pieces
    for (int i = 0; i < BOARD_SIZE; i++) {
        grid[i][1] = BLACK_PAWN;
        grid[i][6] = WHITE_PAWN;
    }

    grid[0][0] = grid[7][0] = BLACK_ROOK;
    grid[1][0] = grid[6][0] = BLACK_KNIGHT;
    grid[2][0] = grid[5][0] = BLACK_BISHOP;
    grid[3][0] = BLACK_QUEEN;
    grid[4][0] = BLACK_KING;

    grid[0][7] = grid[7][7] = WHITE_ROOK;
    grid[1][7] = grid[6][7] = WHITE_KNIGHT;
    grid[2][7] = grid[5][7] = WHITE_BISHOP;
    grid[3][7] = WHITE_QUEEN;
    grid[4][7] = WHITE_KING;
}


void Board::makeMove(Move &move) {
    if (move.isCastle()) {
        castle(move);
        return;
    }

    int enPassantVal;
    if (isPassantMove(move, enPassantVal)) {
        int x = enPassantVal % BOARD_SIZE;
        int y = enPassantVal / BOARD_SIZE;
        removePiece(x, y);
    }

    int piece = getPiece(move.fromX, move.fromY);
    removePiece(move.fromX, move.fromY);
    placePiece(move.toX, move.toY, piece);
}


int Board::getPiece(int x, int y) const {
    if (x >= BOARD_SIZE || y >= BOARD_SIZE || x < 0 || y < 0) {
        return INVALID_SQUARE;
    }
    return grid[x][y];
}


int Board::getPiece(int squareValue) const {
    int x = squareValue % BOARD_SIZE;
    int y = squareValue / BOARD_SIZE;
    return getPiece(x, y);
}


bool Board::isPossibleMove(Move &move) const {
    bool playerColour;
    int castleInt;

    if (move.isCastle(playerColour, castleInt)) {
        return isPossibleCastleMove(playerColour, castleInt);
    }

    int pieceAtMove = getPiece(move.toX, move.toY);

    if (pieceAtMove == INVALID_SQUARE) {
        return false;
    }

    bool toWhite = pieceAtMove > 0;
    bool toBlack = pieceAtMove < 0;

    if (toWhite && isWhiteMove(move)) {
        return false;
    } else if (toBlack && !isWhiteMove(move)) {
        return false;
    }

    return true;
}


bool Board::isValidMove(Move &move) const {
    bool playerColour;
    int castleInt;

    if (move.isCastle(playerColour, castleInt)) {
        return isValidCastleMove(playerColour, castleInt);
    }

    int piece = getPiece(move.fromX, move.fromY);
    bool isWhite = piece > 0;

    Board newBoard = *this;
    newBoard.makeMove(move);

    if (newBoard.isInCheck(isWhite)) {
        return false;
    }

    return true;
}


bool Board::isPossibleCastleMove(bool playerColour, int side) const {
    int x, y;
    x = 4;   // Both kings are five squares from left on board
    playerColour ? y = 7 : y = 0;

    int correctNumEmptySquares;
    int direction;

    if (side == CASTLE_KINGS_SIDE) {
        direction = RIGHT;
        correctNumEmptySquares = 2;
    } else {
        direction = LEFT;
        correctNumEmptySquares = 3;
    }

    int foundPiece = 0;

    // Search to left, and make sure there's nothing in the three spaces to the
    // left of the king
    int emptySquares = searchDirection(x, y, 0, direction, foundPiece);
    if (emptySquares != correctNumEmptySquares) {
        return false;
    }

    // Check that the rook is in the correct position
    int rook;
    playerColour ? rook = WHITE_ROOK : rook = BLACK_ROOK;

    if (foundPiece != rook) {
        return false;
    }

    return true;
}


bool Board::isValidCastleMove(bool playerColour, int side) const {
    if (isInCheck(playerColour)) {
        return false;
    }

    int x, y;
    x = 4;   // Both kings are five squares from left on board
    playerColour ? y = 7 : y = 0;

    int correctNumEmptySquares;
    int direction;

    if (side == CASTLE_KINGS_SIDE) {
        direction = RIGHT;
        correctNumEmptySquares = 2;
    } else {
        direction = LEFT;
        correctNumEmptySquares = 3;
    }

    int* possibleCheckMoves = new int[correctNumEmptySquares];
    bool returnVal;
    int count = 0;

    // Search to left, and make sure king does not pass through check by 
    // castling Queen's Side
    searchDirection(x, y, 0, direction, playerColour, possibleCheckMoves, count);
    if (count == correctNumEmptySquares) {
        returnVal = true;
    } else {
        returnVal = false;
    }

    delete[] possibleCheckMoves;
    return returnVal;
}


bool Board::isPossibleValidMove(Move &move) const {
    return (isPossibleMove(move) && isValidMove(move));
}


bool Board::isPassantMove(Move &move, int &enPassantVal) 
    const 
{
    int piece = getPiece(move.fromSquare);

    if (abs(piece) != WHITE_PAWN) {
        return false;
    }

    bool diagonalMove = (move.toX - move.fromX) != 0;

    // If pawn is taking but there is no piece at the square it is moving to
    if (diagonalMove && getPiece(move.toSquare) == 0) {
        
        // If pawn A is taking pawn B en Passant, then pawn A and pawn B are on
        // the same rank, and pawn A is moving diagonally onto pawn B's file.
        // Hence pawn B's position is given by:
        //      y = pawn A's original y value (rank)
        //      x = pawn A's new x value (file)
        int x = move.toX;
        int y = move.fromY;
        enPassantVal = y*BOARD_SIZE + x;

        return true;
    }

    return false;
}


int Board::getPieceMoves(bool playerColour, int squareValue, int* movePoints) 
    const 
{
    int x = squareValue % BOARD_SIZE;
    int y = squareValue / BOARD_SIZE;
    int pieceToMove = getPiece(x, y);

    if (pieceToMove == 0) {
        return 0;
    }

    int count = 0;
    int type = abs(pieceToMove);

    if (type == WHITE_KING) {
        count = getKingMoves(x, y, playerColour, movePoints);
    } else if (type == WHITE_QUEEN) {
        count = getQueenMoves(x, y, playerColour, movePoints);
    } else if (type == WHITE_BISHOP) {
        count = getBishopMoves(x, y, playerColour, movePoints);
    } else if (type == WHITE_KNIGHT) {
        count = getKnightMoves(x, y, playerColour, movePoints);
    } else if (type == WHITE_ROOK) {
        count = getRookMoves(x, y, playerColour, movePoints);
    } else if (type == WHITE_PAWN) {
        count = getPawnMoves(x, y, playerColour, movePoints);
    }

    return count;
}


bool Board::isKingMove(Move &move, int &piece) const {
    bool isWhite;
    int side;

    if (move.isCastle(isWhite, side)) {
        if (isWhite) {
            piece = WHITE_KING;
        } else {
            piece = BLACK_KING;
        }
        return true;
    }
    
    piece = getPiece(move.fromX, move.fromY);

    if (abs(piece) == WHITE_KING) {
        return true;
    }

    return false;
}


bool Board::isRookMove(Move &move, int &piece) const {
    if (abs(getPiece(move.fromX, move.fromY)) == WHITE_ROOK) {
        piece = getPiece(move.fromX, move.fromY);
        return true;
    }

    return false;
}


bool Board::isPawnMove(Move &move, int &piece) const {
    if (abs(getPiece(move.fromX, move.fromY)) == WHITE_PAWN) {
        piece = getPiece(move.fromX, move.fromY);
        return true;
    }

    return false;
}


bool Board::isDoublePawnMove(Move &move, int &piece, int &enPassantVal) const {
    if (!isPawnMove(move, piece)) {
        return false;
    }

    if (abs(move.toY - move.fromY) != 2) {
        return false;
    }

    if (piece == WHITE_PAWN) {
        enPassantVal = move.toSquare + BOARD_SIZE;
    } else {
        enPassantVal = move.toSquare - BOARD_SIZE;
    }

    return true;
}


bool Board::isTake(Move &move) const {
    int fromPiece = getPiece(move.fromX, move.fromY);
    int toPiece = getPiece(move.toX, move.toY);

    bool whiteToBlack = (fromPiece > 0) && (toPiece < 0);
    bool blackToWhite = (fromPiece < 0) && (toPiece > 0);
    return(whiteToBlack || blackToWhite);
}


bool Board::isInCheck(bool playerColour) const {
    int king;
    int enemyKing, enemyQueen, enemyBishop, enemyKnight, enemyRook, enemyPawn;

    if (playerColour){
        king        = WHITE_KING;
        enemyKing   = BLACK_KING;
        enemyQueen  = BLACK_QUEEN;
        enemyBishop = BLACK_BISHOP;
        enemyKnight = BLACK_KNIGHT;
        enemyRook   = BLACK_ROOK;
        enemyPawn   = BLACK_PAWN;
    } else {
        king        = BLACK_KING;
        enemyKing   = WHITE_KING;
        enemyQueen  = WHITE_QUEEN;
        enemyBishop = WHITE_BISHOP;
        enemyKnight = WHITE_KNIGHT;
        enemyRook   = WHITE_ROOK;
        enemyPawn   = WHITE_PAWN;
    }

    int i, j;
    int x, y;   // Position of king
    bool kingFound = false;

    // Find King
    for (i = 0; i < BOARD_SIZE; i++) {
        for (j = 0; j < BOARD_SIZE; j++) {
            if (getPiece(i, j) == king) {
                x = i;
                y = j;
                kingFound = true;
                break;
            }
        }
    }

    if (!kingFound) {
        return false;
    }

    // Radiate outwards, look for enemy queen, bishops and rooks
    int piece[8];

    // Horizontally
    searchDirection(x, y, UP, 0, piece[0]);
    searchDirection(x, y, DOWN, 0, piece[1]);

    // Vertically
    searchDirection(x, y, 0, RIGHT, piece[2]);
    searchDirection(x, y, 0, LEFT, piece[3]);

    // Diagonally
    searchDirection(x, y, UP, RIGHT, piece[4]);
    searchDirection(x, y, DOWN, RIGHT, piece[5]);
    searchDirection(x, y, DOWN, LEFT, piece[6]);
    searchDirection(x, y, UP, LEFT, piece[7]);

    for (i = 0; i < 4; i++){
        if (piece[i] == enemyQueen || piece[i] == enemyRook) {
            return true;
        }
    }

    for (i = 4; i <= 7; i++){
        if (piece[i] == enemyQueen || piece[i] == enemyBishop) {
            return true;
        }
    }

    // Look for knights
    if (getPiece(x - 1, y + 2) == enemyKnight)     return true;
    if (getPiece(x - 1, y - 2) == enemyKnight)     return true;
    if (getPiece(x + 1, y + 2) == enemyKnight)     return true;
    if (getPiece(x + 1, y - 2) == enemyKnight)     return true;
    if (getPiece(x + 2, y - 1) == enemyKnight)     return true;
    if (getPiece(x - 2, y - 1) == enemyKnight)     return true;
    if (getPiece(x + 2, y + 1) == enemyKnight)     return true;
    if (getPiece(x - 2, y + 1) == enemyKnight)     return true;

    // Look for pawns
    if (playerColour){
        if (getPiece(x - 1, y - 1) == enemyPawn)   return true;
        if (getPiece(x + 1, y - 1) == enemyPawn)   return true;
    } else {
        if (getPiece(x - 1, y + 1) == enemyPawn)   return true;
        if (getPiece(x + 1, y + 1) == enemyPawn)   return true;
    }

    // And finally, the enemy king
    if (getPiece(x, y - 1) == enemyKing)     return true;
    if (getPiece(x, y + 1) == enemyKing)     return true;
    if (getPiece(x + 1, y) == enemyKing)     return true;
    if (getPiece(x - 1, y) == enemyKing)     return true;
    if (getPiece(x + 1, y - 1) == enemyKing)     return true;
    if (getPiece(x + 1, y + 1) == enemyKing)     return true;
    if (getPiece(x - 1, y + 1) == enemyKing)     return true;
    if (getPiece(x - 1, y - 1) == enemyKing)     return true;

    return false;
}


bool Board::hasWon(bool playerColour) const {
    return (!legalMoveExists(!playerColour) && isInCheck(!playerColour));
}


bool Board::isKingDraw() const {
    for (int square = 0; square < BOARD_SIZE*BOARD_SIZE; square++) {
        if (getPiece(square) != 0 && abs(getPiece(square)) != WHITE_KING) {
            return false;
        }
    }

    return true;
}


bool Board::legalMoveExists(bool playerColour) const {
    int * movePoints = new int[MAX_AVAILABLE_MOVES];
    bool returnVal = false;

    for (int x = 0; x < BOARD_SIZE; x++) {
        for (int y = 0; y < BOARD_SIZE; y++) {
            if ((getPiece(x, y) > 0) == playerColour){
                int squareValue = y*BOARD_SIZE + x;
                if (getPieceMoves(playerColour, squareValue, movePoints) > 0) {
                    returnVal = true;
                    break;
                }
            }
        }
    }

    delete[] movePoints;
    return returnVal;
}


bool Board::canPromotePawn(bool playerColour) const {
    int x, y;
    if (playerColour) {
        y = 0;
    } else {
        y = 7;
    }
    
    for (x = 0; x < BOARD_SIZE; x++) {
        if (abs(getPiece(x, y)) == WHITE_PAWN) {
            return true;
        }
    }

    return false;
}


bool Board::promotePawn(bool playerColour, int piece) {
    int x, y;

    if (playerColour) {
        y = 0;
    } else {
        y = 7;
    }

    for (x = 0; x < BOARD_SIZE; x++) {
        if (abs(getPiece(x, y)) == WHITE_PAWN) {
            removePiece(x, y);
            placePiece(x, y, piece);
            return true;
        }
    }

    return false;
}


void Board::printToConsole() {
    std::cout << getPictorial();
}


std::string Board::getPictorial() {
    std::string str = "";

    str += "\n\n";
    str += "    -------------------\n";

    for (int row = 0; row < BOARD_SIZE; row++) {
        str += "    | ";
        for (int column = 0; column < BOARD_SIZE; column++) {
            int pieceVal = getPiece(column, row);

            if (pieceVal == 0) {
                str += "_ ";
            } else {
                Piece piece(pieceVal, 1);
                str += piece.display + " ";
            }
        }
        str += "|\n";
    }

    str += "    -------------------\n";
    str += "\n\n";

    return str;
}


std::string Board::getForsyth() {
    std::string forsyth = "";

    for (int row = 0; row < BOARD_SIZE; row++) {

        int column = 0;
        int pieceVal = getPiece(column, row);

        while (column < BOARD_SIZE) {
            if (pieceVal == 0) {
                int gap = searchDirection(column, row, 0, RIGHT, pieceVal);
                forsyth += std::to_string(gap + 1);
                column += gap + 1;
            } else {
                Piece piece(pieceVal, 1);
                forsyth += piece.display;
                int gap = searchDirection(column, row, 0, RIGHT, pieceVal);

                if (gap > 0) {
                    forsyth += std::to_string(gap);
                }

                column += gap + 1;
            }
        }

        if (row < BOARD_SIZE - 1) {
            forsyth += "/";
        }
    }

    forsyth += " ";
    return forsyth;
}


std::string Board::getSAN(Move &move) {
    std::string returnStr;

    bool isWhiteMove;
    int side;

    if (move.isCastle(isWhiteMove, side)) {
        returnStr = "O-O";
        if (side == CASTLE_QUEENS_SIDE) {
            returnStr += "-O";
        }

        return returnStr;
    }

    int pieceType = abs(getPiece(move.fromSquare));

    if (pieceType != WHITE_PAWN) {
        Piece piece(pieceType, 1);
        returnStr += piece.display;

        returnStr += getClarificationStr(move);
    }

    if (isTake(move)) {
        if (pieceType == WHITE_PAWN) {
            returnStr += xToStr(move.fromX);
        }
        returnStr += "x";
    }

    returnStr += squareToStr(move.toX, move.toY);
    return returnStr;
}


std::string Board::xToStr(int x) {
    switch (x) {
    case 0:
        return "a";
    case 1:
        return "b";
    case 2:
        return "c";
    case 3:
        return "d";
    case 4:
        return "e";
    case 5:
        return "f";
    case 6:
        return "g";
    case 7:
        return "h";
    }
}


std::string Board::yToStr(int y) {
    return std::to_string(8 - y);
}


std::string Board::squareToStr(int x, int y) {
    std::string returnStr;
    returnStr = xToStr(x) + yToStr(y);
    return returnStr;
}


std::string Board::getClarificationStr(Move &move) {
    int piece = getPiece(move.fromSquare);
    bool pieceColour = piece > 0;

    std::string returnStr = "";

    bool needFile = false;
    bool needRank = false;

    // The maximum number of pieces of a given type a player could possibly have
    // is given by the original two pieces, plus 8 promoted pawns = 10. This
    // array is intended to hold the locations of all pieces, except the one
    // which has just moved, hence it is 10 - 1 = 9 addresses long.
    int pieces[9];
    int numOtherPieces = 0;

    for (int i = 0; i < BOARD_SIZE*BOARD_SIZE; i++) {
        if (getPiece(i) == piece && i != move.fromSquare) {
            pieces[numOtherPieces] = i;
            numOtherPieces++;
        }
    }

    if (numOtherPieces == 0) {
        return "";
    }

    int * movePoints = new int[MAX_PIECE_MOVES];

    // For each piece of the same type
    for (int i = 0; i < numOtherPieces; i++) {
        int numMoves = getPieceMoves(pieceColour, pieces[i], movePoints);

        for (int j = 0; j < numMoves; j++) {
            // If this piece could move to the same location
            if (movePoints[j] == move.toSquare) {

                // If the pieces do not come from the same file
                if ( (pieces[i] % BOARD_SIZE) != move.fromX) {
                    needFile = true;
                } else {
                    needRank = true;
                }
            }
        }
    }

    if (needFile) {
        returnStr += xToStr(move.fromX);
    }

    if (needRank) {
        returnStr += yToStr(move.fromY);
    }

    return returnStr;
}


bool Board::placePiece(int x, int y, int piece) {
    bool returnVal = (getPiece(x, y) != 0);
    grid[x][y] = piece;
    return returnVal;
}


bool Board::removePiece(int x, int y) {
    bool returnVal = (getPiece(x, y) != 0);
    grid[x][y] = 0;
    return returnVal;
}


bool Board::isWhiteMove(Move &move) const {
    return (getPiece(move.fromX, move.fromY) > 0);
}


int Board::getKingMoves(int x, int y, bool colour, int* movePoints) const {
    int count = 0;

    if (isPossibleValidMove(Move(x, y, x, y - 1))) {
        movePoints[count] = BOARD_SIZE*(y - 1) + x;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x, y + 1))) {
        movePoints[count] = BOARD_SIZE*(y + 1) + x;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x - 1, y))) {
        movePoints[count] = BOARD_SIZE*y + x - 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x - 1, y - 1))) {
        movePoints[count] = BOARD_SIZE*(y - 1) + x - 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x - 1, y + 1))) {
        movePoints[count] = BOARD_SIZE*(y + 1) + x - 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x + 1, y))) {
        movePoints[count] = BOARD_SIZE*y + x + 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x + 1, y - 1))) {
        movePoints[count] = BOARD_SIZE*(y - 1) + x + 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x + 1, y + 1))) {
        movePoints[count] = BOARD_SIZE*(y + 1) + x + 1;
        count++;
    }

    return count;
}


int Board::getQueenMoves(int x, int y, bool isWhite, int* movePoints) const {
    int count = 0;

    searchDirection(x, y, UP, 0, isWhite, movePoints, count);
    searchDirection(x, y, DOWN, 0, isWhite, movePoints, count);
    searchDirection(x, y, 0, LEFT, isWhite, movePoints, count);
    searchDirection(x, y, 0, RIGHT, isWhite, movePoints, count);
    searchDirection(x, y, UP, LEFT, isWhite, movePoints, count);
    searchDirection(x, y, DOWN, LEFT, isWhite, movePoints, count);
    searchDirection(x, y, UP, RIGHT, isWhite, movePoints, count);
    searchDirection(x, y, DOWN, RIGHT, isWhite, movePoints, count);

    return count;

}


int Board::getBishopMoves(int x, int y, bool isWhite, int* movePoints) const {
    int count = 0;

    searchDirection(x, y, UP, LEFT, isWhite, movePoints, count);
    searchDirection(x, y, DOWN, LEFT, isWhite, movePoints, count);
    searchDirection(x, y, UP, RIGHT, isWhite, movePoints, count);
    searchDirection(x, y, DOWN, RIGHT, isWhite, movePoints, count);

    return count;
}


int Board::getKnightMoves(int x, int y, bool isWhite, int* movePoints) const {
    int count = 0;

    if (isPossibleValidMove(Move(x, y, x - 1, y - 2))) {
        movePoints[count] = BOARD_SIZE*(y - 2) + x - 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x - 1, y + 2))) {
        movePoints[count] = BOARD_SIZE*(y + 2) + x - 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x + 1, y - 2))) {
        movePoints[count] = BOARD_SIZE*(y - 2) + x + 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x + 1, y + 2))) {
        movePoints[count] = BOARD_SIZE*(y + 2) + x + 1;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x - 2, y - 1))) {
        movePoints[count] = BOARD_SIZE*(y - 1) + x - 2;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x - 2, y + 1))) {
        movePoints[count] = BOARD_SIZE*(y + 1) + x - 2;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x + 2, y - 1))) {
        movePoints[count] = BOARD_SIZE*(y - 1) + x + 2;
        count++;
    }
    if (isPossibleValidMove(Move(x, y, x + 2, y + 1))) {
        movePoints[count] = BOARD_SIZE*(y + 1) + x + 2;
        count++;
    }

    return count;
}


int Board::getRookMoves(int x, int y, bool isWhite, int* movePoints) const {
    int count = 0;

    searchDirection(x, y, UP, 0, isWhite, movePoints, count);
    searchDirection(x, y, DOWN, 0, isWhite, movePoints, count);
    searchDirection(x, y, 0, LEFT, isWhite, movePoints, count);
    searchDirection(x, y, 0, RIGHT, isWhite, movePoints, count);

    return count;
}


int Board::getPawnMoves(int x, int y, bool isWhite, int* movePoints) const {
    int count = 0;
    int m;      // A multiplier, so that white pawns move up the board (in the
                // negative y direction) and black pawns move down it.

    if (isWhite) {
        m = -1;
    } else {
        m = 1;
    }

    bool notYetMoved = ((isWhite && y == 6) || (!isWhite && y == 1));

    Move oneForward(x, y, x, y + m*1);
    Move twoForward(x, y, x, y + m*2);
    Move leftTake(x, y, x - 1, y + m*1);
    Move rightTake(x, y, x + 1, y + m*1);

    if (isPossibleMove(oneForward) && !isTake(oneForward)) {
        if (isPossibleValidMove(oneForward)) {
            movePoints[count] = oneForward.toSquare;
            count++;
        }
        if (isPossibleValidMove(twoForward) && !isTake(twoForward) && notYetMoved) {
            movePoints[count] = twoForward.toSquare;
            count++;
        }
    }
    if (isTake(leftTake) && isPossibleValidMove(leftTake)){
        movePoints[count] = leftTake.toSquare;
        count++;
    }
    if (isTake(rightTake) && isPossibleValidMove(rightTake)){
        movePoints[count] = rightTake.toSquare;
        count++;
    }

    return count;
}


int Board::searchDirection(int x, int y, int upDown, int leftRight, int &piece)
    const
{
    piece = 0;

    if (upDown == 0 && leftRight == 0){
        return 0;
    }

    // Ensure that upDown and leftRight are -1, 0, or 1
    if (abs(upDown) != 0) {
        upDown = upDown / abs(upDown);
    }
    if (abs(leftRight) != 0) {
        leftRight = leftRight / abs(leftRight);
    }

    int i = x + leftRight;
    int j = y + upDown;
    int count = 0;

    while (i >= 0 && j >= 0 && i < BOARD_SIZE && j < BOARD_SIZE) {
        if (getPiece(i, j) != 0) {
            piece = getPiece(i, j);
            return count;
        }

        i += leftRight;
        j += upDown;
        count++;
    }

    return count;
}


int Board::searchDirection(int x, int y, int upDown, int leftRight,
                           bool isWhitePiece, int *movePoints, int &count) const
{
    if (upDown == 0 && leftRight == 0) {
        return 0;
    }

    // Ensure that upDown and leftRight are -1, 0, or 1
    if (abs(upDown) != 0) {
        upDown = upDown / abs(upDown);
    }
    if (abs(leftRight) != 0) {
        leftRight = leftRight / abs(leftRight);
    }

    int i = x + leftRight;
    int j = y + upDown;

    while (i >= 0 && j >= 0 && i < BOARD_SIZE && j < BOARD_SIZE) {
        Move move(x, y, i, j);

//        if (!isPossibleMove(move)) {
//            return 0;
//        }
// By my reckoning this should be removed...not sure if that will break something though

        bool moveAllowed = isValidMove(move);
        int pieceAtMove = getPiece(i, j);

        if (pieceAtMove == 0) {
            if (moveAllowed) {
                movePoints[count] = move.toSquare;
                count++;
            }
        } else {
            if (isTake(move) && moveAllowed){
                movePoints[count] = move.toSquare;
                count++;
            }
            return pieceAtMove;
        }

        i += leftRight;
        j += upDown;
    }

    return 0;
}


void Board::castle(Move &move) {
    bool isWhite;
    int side;

    if (!move.isCastle(isWhite, side)) { 
        return;
    }

    int kingX, rookX;
    int kingToX, rookToX;
    kingX = 4;

    if (side == CASTLE_KINGS_SIDE) {
        kingToX = 6;
        rookX = 7;
        rookToX = 5;
    } else {
        kingToX = 2;
        rookX = 0;
        rookToX = 3;
    }

    int y;
    isWhite ? y = 7 : y = 0;

    makeMove(Move(kingX, y, kingToX, y));
    makeMove(Move(rookX, y, rookToX, y));
}


bool Board::isWhiteSquare(int x, int y) {
    return (((x + y) % 2) == 0);
}
