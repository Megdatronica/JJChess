#include "gameState.h"
#include "player.h"
#include "constants.h"

// Represents a human player. Functions make calls to GameInputOutput in order
// to get the choices of the user.
class HumanPlayer : public Player {

public:

    // Purely a call to the superclass constructor - sets the player colour
    // equal to the passed bool.
    HumanPlayer(bool playerColour);


    // Displays the board and returns a legal move chosen by the user
    Move getMove(GameState *gameState);


    // Displays the board and returns the piece for pawn promotion chosen by the
    // user
    int choosePromotion(GameState *gameState);

};
