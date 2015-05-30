#ifndef RANDAIPLAYER_H
#define RANDAIPLAYER_H

#include "player.h"
#include "gameState.h"
#include <Windows.h>

// A very basic AI player which will make randomly selected legal moves.
class RandAIPlayer : public Player {

public:

    // Purely a call to the superclass constructor - sets the player colour
    // equal to the passed bool.
    RandAIPlayer(bool playerColour);


    // Returns a randomly selected legal move
    Move getMove(GameState *gameState);


    // Returns the queen of the corresponding colour
    int choosePromotion(GameState *gameState);

};

#endif