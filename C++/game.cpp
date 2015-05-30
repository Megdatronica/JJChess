#include "game.h"
#include <cmath>
#include <iostream>
#include <string>
#include <iostream>
#include <fstream>


Game::Game() {

    std::ofstream outputFile;
    outputFile.open(fileDir);
    outputFile.close();

    //int whitePlayerType = gameIO.getPlayerAssignment(WHITE, NUM_PLAYER_CHOICES);
    //int blackPlayerType = gameIO.getPlayerAssignment(BLACK, NUM_PLAYER_CHOICES);
    //assignPlayer(WHITE, whitePlayerType);
    //assignPlayer(BLACK, blackPlayerType);
}


Game::Game(int whitePlayerType, int blackPlayerType) {
    std::ofstream outputFile;
    outputFile.open(fileDir);
    outputFile.close();

    assignPlayer(WHITE, whitePlayerType);
    assignPlayer(BLACK, blackPlayerType);
}


Game::~Game() {
    delete whitePlayer;
    delete blackPlayer;
}


int Game::play() {
    while (true) {        
        int status = takeTurn();

        if (abs(status) > 1) {
            return status;
        }
    }
}


void Game::assignPlayer(bool playerColour, int playerType) {
    Player * playerPtr;

    if (playerType == HUMAN) {
        playerPtr = new HumanPlayer(playerColour);
    } else {
        playerPtr = new RandAIPlayer(playerColour);
    }

    playerColour ? whitePlayer = playerPtr: blackPlayer = playerPtr;
}


Player * Game::getCurrentPlayer() const {
    if (state.isWhiteTurn) {
        return whitePlayer;
    } else {
        return blackPlayer;
    }
}


Player * Game::getWaitingPlayer() const {
    if (state.isWhiteTurn) {
        return blackPlayer;
    } else {
        return whitePlayer;
    }
}


int Game::takeTurn() {
    Player * currentPlayer = getCurrentPlayer();

    Move move = currentPlayer->getMove(&state);
    std::string moveSAN = state.getSAN(move);

    state.makeMove(move);
    int promoteVal = promotePawn();

    int statusInt = state.getStatus();
    logMove(moveSAN, statusInt, promoteVal);

    std::ofstream outputFile;
    outputFile.open("boards.txt", std::ios::app);
    outputFile << state.board.getPictorial();
    outputFile.close();
    
    state.swapTurn();

    return statusInt;
}


int Game::promotePawn() {
    if (state.canPromotePawn()) {
        Player * currentPlayer = getCurrentPlayer();
        int piece = currentPlayer->choosePromotion(&state);

        state.promotePawn(piece);
        return piece;
    }

    return 0;
}


void Game::logMove(std::string moveSAN, int statusInt, int promoteVal) {
    std::ofstream outputFile;
    outputFile.open(fileDir, std::ios::app);

    std::string appendStr = "";

    int moveNumber = (state.moveCount + 1) / 2;
    // Note that state.moveCount is the number of HALF moves that have been made
    // INCLUDING this one.
    
    if (state.isWhiteTurn) {
        appendStr = std::to_string(moveNumber) + ". " + moveSAN;
    } else {
        appendStr = moveSAN;
    }

    switch (abs(promoteVal)) {
    case WHITE_QUEEN:
        appendStr += "=Q";
        break;
    case WHITE_KNIGHT:
        appendStr += "=N";
        break;
    case WHITE_BISHOP:
        appendStr += "=B";
        break;
    case WHITE_ROOK:
        appendStr += "=R";
        break;
    }

    switch (statusInt) {
    case WHITE_CHECK:
    case BLACK_CHECK:
        appendStr += "+ ";
        break;
    case WHITE_WIN:
        appendStr += "# 1-0";
        break;
    case BLACK_WIN:
        appendStr += "# 0-1";
        break;
    case KING_DRAW:
    case STALEMATE:
    case FIFTY_MOVE_DRAW:
        appendStr += " 1/2-1/2";
        break;
    default:
        appendStr += " ";
    }

    outputFile << appendStr;
    outputFile.close();
}