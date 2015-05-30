#include "player.h"
#include <cmath>
#include <iostream>


Player::Player() : playerColour(false), isHuman(true) {}


Player::Player(bool playerColour, bool isHuman) : playerColour(playerColour),
                                                  isHuman(isHuman) {
    numCapturedPieces = 0;
}


void Player::addCapturedPiece(int piece) {
    capturedPieces[numCapturedPieces] = piece;
    numCapturedPieces++;
}


int * Player::getCapturedPieces(int &count) {
    count = numCapturedPieces;
    return capturedPieces;
}
