#ifndef PYTHON_AI_H
#define PYTHON_AI_H

#include "player.h"
#include "gameState.h"

// A very basic AI player which will make randomly selected legal moves.
class PythonAIPlayer : public Player {

public:

    // Sets the player colour equal to the passed bool and initialises python
    // AI based on the given file location
    // Inputs:
    //     playerColour:    true if this AI will be playing white
    //     fileDir:         location of file containing logic
    PythonAIPlayer (bool playerColour, std::string fileDir);


    // Returns a randomly selected legal move
    Move getMove(GameState *gameState);


    // Returns the queen of the corresponding colour
    int choosePromotion(GameState *gameState);

private:

	// String containing location of python script with AI logic
	std::string fileDir;

};

#endif