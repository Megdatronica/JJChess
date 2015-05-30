#ifndef GAME_H
#define GAME_H


#include "constants.h"
#include "gameState.h"
#include "player.h"
#include "humanPlayer.h"
#include "randAIPlayer.h"

const std::string fileDir = "Pre-alpha-0.4.2.pgn";

// Creates and sets up the board, keeps count of the moves and the pieces 
// captured, and contains the main game loop.
class Game{

public:

    // Creates a game which will ask the user to choose the player types, and
    // will output the result to the console.
    Game();


    // Creates a game between the specified player types. If both players are AI
    // players, then play() will only return the result of the game and input or
    // output nothing else.
    Game(int whitePlayerType, int blackPlayerType);


    ~Game();

    // Sets up game, and contains the main loop for allocating turns and 
    // checking for victory/draw. Returns 1 if white has won, -1 if black has
    // won, and 0 if game has been drawn.
    int play();


    // Returns a pointer to the player whose turn it currently is
    Player * getCurrentPlayer() const;


    // Returns a pointer to the player NOT currently taking their turn
    Player * getWaitingPlayer() const;

private:

    // Sets either the blackPlayer or whitePlayer pointer to the player of the
    // specified type.
    // Inputs:
    // bool playerColour:    True if player being allocated is white
    // int playerType:       0 = human player, 1 = random AI player, etc
    // 
    // It is the caller's responsibility to delete the memory allocated for
    // the pointers whitePlayer and blackPlayer.
    void assignPlayer(bool playerColour, int playerType);


    // Gets a valid move from the current player, changes the state variable to
    // reflect the move being made (handling any pawn promotion), and finally
    // changes whose turn it is. Returns the result of gameState.getStatus()
    // after making the move.
    int takeTurn();


    // Searches the board for a pawn belonging to the current player that can be
    // promoted. If a pawn has been found and promoted, returns the value of the
    // piece it was promoted to. Otherwise returns 0.
    int promotePawn();


    // Adds the passed move to the list of moves in the file with name given by
    // the constant fileDir. Note that this should be called BEFORE 
    // state.swapTurn().
    // Inputs:
    //     string moveSAN:   a string representing the move made in SAN format,
    //                       without check/checkmate or promotion appended
    //     int statusInt:    the result of state.getStatus() after the move has
    //                       been made.
    //     int promoteVal:   the return value of promotePawn()
    void logMove(std::string moveSAN, int statusInt, int promoteVal);


    GameState state;
    Player *whitePlayer;
    Player *blackPlayer;
};


#endif