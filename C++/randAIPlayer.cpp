#include "randAIPlayer.h"
#include <cmath>
#include <iostream>


RandAIPlayer::RandAIPlayer(bool playerColour) : Player(playerColour, false) {
    srand(GetTickCount());
}


Move RandAIPlayer::getMove(GameState *gameState) {
    int numMoves;
    Move * moves = gameState->getPlayerMoves(playerColour, numMoves);

    int chosenMoveNum = rand() % numMoves;
    Move chosenMove = moves[chosenMoveNum];

    delete[] moves;

    return chosenMove;
}


int RandAIPlayer::choosePromotion(GameState *gameState) {
    if (playerColour) {
        return WHITE_QUEEN;
    } else {
        return BLACK_QUEEN;
    }
}
