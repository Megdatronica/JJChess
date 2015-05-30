#ifndef PLAYER_H
#define PLAYER_H

#include "gameState.h"
#include "constants.h"
#include "move.h"


// Number of players (human, random AI, etc) currently implemented and playable.
const int NUM_PLAYER_CHOICES = 2;

const int HUMAN = 0;
const int RAND_AI = 1;


// Abstract class for handling how a player chooses their moves
class Player{

public:

    // Sets isHuman to true and playerColour to black
    Player();


    // Sets playerColour and isHuman equal to passed bools
    Player(bool playerColour, bool isHuman);


    // Displays the board if applicable, and returns the chosen move based on
    // the state of the game (This move will be verified to be a legal move)
    virtual Move getMove(GameState *gameState) = 0;


    // Displays the board if applicable, and returns an int representing the
    // piece chosen to promote a pawn to
    virtual int choosePromotion(GameState *gameState) = 0;


    // Adds a piece to the list of pieces captured by this player
    void addCapturedPiece(int piece);


    // Returns a pointer to an array of pieces captured by this player.
    // Outputs:
    //     &count:    will be set to the number of pieces in the returned array
    //
    // The caller should delete the memory allocated by this function with
    // delete[count].
    int * getCapturedPieces(int &numCapturedPieces);

    const bool playerColour;    // True if player is white
    const bool isHuman;

private:
    int capturedPieces[15];     // Holds list of pieces captured by this player
    int numCapturedPieces;      // Number of pieces captured by this player

};

#endif