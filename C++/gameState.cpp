#include "gameState.h"
#include <iostream>
#include <fstream>


GameState::GameState(){
    initVariables();
}


int GameState::getPieceMoves(bool playerColour, int squareValue, int* movePoints)
    const
{
    int count = board.getPieceMoves(playerColour, squareValue, movePoints);

    int pieceToMove = board.getPiece(squareValue);

    int moveValue;
    if (canPassant(playerColour, squareValue, moveValue)) {
        movePoints[count] = moveValue;
        count++;
    }

    if (!(pieceToMove == WHITE_KING || pieceToMove == BLACK_KING)) {
        return count;
    }

    if (isLegalMove(Move(playerColour, CASTLE_KINGS_SIDE))) {
        movePoints[count] = CASTLE_KINGS_SIDE;
        count++;
    }

    if (isLegalMove(Move(playerColour, CASTLE_QUEENS_SIDE))) {
        movePoints[count] = CASTLE_QUEENS_SIDE;
        count++;
    }

    return count;
}


Move* GameState::getPlayerMoves(bool playerColour, int &numMoves) const {
    Move * moveList = new Move[MAX_AVAILABLE_MOVES];
    numMoves = 0;
    int * movePoints = new int[MAX_PIECE_MOVES];

    for (int square = 0; square < BOARD_SIZE*BOARD_SIZE; square++) {
        if ((board.getPiece(square) > 0) == playerColour) {
            int numPieceMoves = getPieceMoves(playerColour, square, movePoints);

            for (int i = 0; i < numPieceMoves; i++) {
                if (movePoints[i] >= CASTLE_KINGS_SIDE) {
                    moveList[numMoves] = Move(playerColour, movePoints[i]);
                } else {
                    moveList[numMoves] = Move(square, movePoints[i]);
                }
                numMoves++;
            }
        }
    }

    delete[] movePoints;

    return moveList;
}


void GameState::makeMove(Move &move) {
    updateCounts(move);
    board.makeMove(move);
}


void GameState::promotePawn(int piece) {
    board.promotePawn(isWhiteTurn, piece);
}


bool GameState::canPromotePawn() {
    return board.canPromotePawn(isWhiteTurn);
}


int GameState::getStatus() {
    int win, check;
    isWhiteTurn ? win = WHITE_WIN : win = BLACK_WIN;
    isWhiteTurn ? check = WHITE_CHECK : check = BLACK_CHECK;

    // Note that fiftyMoveRuleCount is effectively incremented twice for each
    // full move (once per player)
    if (fiftyMoveRuleCount == 100)        return FIFTY_MOVE_DRAW;
    if (board.isKingDraw())               return KING_DRAW;

    bool inCheck = board.isInCheck(!isWhiteTurn);
    bool legalMoveExists = board.legalMoveExists(!isWhiteTurn);

    // We could call board.hasWon, but this would mean running the
    // same checks twice
    if ((!legalMoveExists) && inCheck)    return win;
    if (!legalMoveExists)                 return STALEMATE;
    if (inCheck)                          return check;

    return 0;
}


void GameState::swapTurn() {
    isWhiteTurn = !isWhiteTurn;
}


std::string GameState::getSAN(Move &move) {
    return board.getSAN(move);
}


void GameState::initVariables() {
    isWhiteTurn = true;

    whiteCanCastleKSide = true;
    whiteCanCastleQSide = true;
    blackCanCastleKSide = true;
    blackCanCastleQSide = true;

    moveCount = 0;
    fiftyMoveRuleCount = 0;
    enPassantVal = -1;

    board.setUp();
}


void GameState::updateCounts(Move &move) {
    int piece;

    if (board.isKingMove(move, piece)) {
        if (piece == WHITE_KING) {
            whiteCanCastleKSide = false;
            whiteCanCastleQSide = false;
        } else if (piece == BLACK_KING) {
            blackCanCastleKSide = false;
            blackCanCastleQSide = false;
        }
    }

    if (board.isRookMove(move, piece)) {
        if (piece == WHITE_ROOK) {
            if (move.fromX == 0 && move.fromY == 7) {
                whiteCanCastleQSide = false;
            } else if (move.fromX == 7 && move.fromY == 7) {
                whiteCanCastleKSide = false;
            }
        } else if (piece == BLACK_ROOK) {
            if (move.fromX == 0 && move.fromY == 0) {
                blackCanCastleQSide = false;
            } else if (move.fromX == 7 && move.fromY == 0) {
                blackCanCastleKSide = false;
            }
        }
    }

    enPassantVal = -1;
    board.isDoublePawnMove(move, piece, enPassantVal);

    moveCount++;

    if (!board.isTake(move) && !board.isPawnMove(move, piece)) {
        fiftyMoveRuleCount++;
    } else {
        fiftyMoveRuleCount = 0;
    }
}


bool GameState::isInCheck(bool playerColour) const {
    return board.isInCheck(playerColour);
}


bool GameState::couldCastleKingsSide(bool playerColour) const {
    if (playerColour == WHITE) {
        if (!whiteCanCastleKSide) {
            return false;
        }
        if (board.getPiece(7, 7) != WHITE_ROOK) {
            return false;
        }
    } else {
        if (!blackCanCastleKSide) {
            return false;
        }
        if (board.getPiece(0, 7) != BLACK_ROOK) {
            return false;
        }
    }

    return true;
}


bool GameState::couldCastleQueensSide(bool playerColour) const {
    if (playerColour == WHITE) {
        if (!whiteCanCastleQSide) {
            return false;
        }
        if (board.getPiece(7, 0) != WHITE_ROOK) {
            return false;
        }
    } else {
        if (!blackCanCastleQSide) {
            return false;
        }
        if (board.getPiece(0, 0) != BLACK_ROOK) {
            return false;
        }
    }

    return true;
}


bool GameState::canPassant(bool playerColour, int squareValue, int &moveValue)
    const 
{
    int piece = board.getPiece(squareValue);

    if (abs(piece) != WHITE_PAWN || enPassantVal == -1) {
        return false;
    }

    int x = squareValue % BOARD_SIZE;
    int y = squareValue / BOARD_SIZE;

    int m;      // A multiplier, so that white pawns move up the board (in the
                // negative y direction) and black pawns move down it.

    playerColour ? m = -1: m = 1;

    int leftTake = (y + m*1)*BOARD_SIZE + x - 1;
    int rightTake = (y + m*1)*BOARD_SIZE + x + 1;

    // NB: We do not yet know if leftTake/rightTake are actually squares on the
    // board. Hence we pass board.getPiece the x and y values to make sure.
    if (board.getPiece(x - 1, y + m*1) == 0 && leftTake == enPassantVal) {
        moveValue = enPassantVal;
        return true;
    }

    if (board.getPiece(x + 1, y + m*1) == 0 && rightTake == enPassantVal) {
        moveValue = enPassantVal;
        return true;
    }

    return false;
}


bool GameState::isLegalMove(Move &move) const {
    bool playerColour;
    int castleSide;

    if (move.isCastle(playerColour, castleSide)) {
        if (castleSide = CASTLE_KINGS_SIDE) {
            if (!couldCastleKingsSide(playerColour)) {
                return false;
            }
        } else {
            if (!couldCastleQueensSide(playerColour)) {
                return false;
            }
        }
    }

    return board.isPossibleValidMove(move);
}
