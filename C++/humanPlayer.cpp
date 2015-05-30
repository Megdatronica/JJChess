#include "humanPlayer.h"
#include <cmath>
#include <iostream>


HumanPlayer::HumanPlayer(bool playerColour) : Player(playerColour, true) {}


Move HumanPlayer::getMove(GameState *gameState) {
    int numMoves;
    Move * moves = gameState->getPlayerMoves(playerColour, numMoves);

    int chosenMoveNum = rand() % numMoves;
    Move chosenMove = moves[chosenMoveNum];

    delete[] moves;

    return chosenMove;
    //return game->gameIO.getHumanMove(*game, playerColour);
}


int HumanPlayer::choosePromotion(GameState *gameState) {
    //return game->gameIO.getHumanPawnPromoteChoice(game->board, playerColour);
    if (playerColour) {
        return WHITE_QUEEN;
    } else {
        return BLACK_QUEEN;
    }
}