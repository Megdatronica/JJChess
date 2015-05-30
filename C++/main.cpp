#include "Game.h"
#include <windows.h>
#include <iostream>
#include <time.h>

int main() {
    clock_t t1, t2;
    t1 = clock();

    const int numGames = 1;

    int gameResults[numGames];
    int blackWins = 0;
    int whiteWins = 0;
    int draws = 0;


    for (int i = 0; i < numGames; i++) {
        std::cout << "Playing game " << i << std::endl;

        Game game(1, 1);
        int result = game.play();

        switch (result) {

        case WHITE_WIN:
            std::cout << "    End game: White wins\n";
            whiteWins++;
            break;
        case BLACK_WIN:
            std::cout << "    End game: Black wins\n";
            blackWins++;
            break;
        case STALEMATE:
            std::cout << "    End game: Stalemate\n";
            draws++;
            break;
        case FIFTY_MOVE_DRAW:
            std::cout << "    End game: Fifty move rule\n";
            draws++;
            break;
        case KING_DRAW:
            std::cout << "    End game: King Draw\n";
            draws++;
            break;
        }

        gameResults[i] = result;
    }

    std::cout << std::endl;
    std::cout << numGames << " games played.\n";
    std::cout << "White wins: " << whiteWins << "\n";
    std::cout << "Black wins:" << blackWins << "\n";
    std::cout << "Draws: " << draws << "\n\n";

    t2 = clock();
    float diff((float)t2 - (float)t1);
    std::cout << "Time taken: " << diff << " milliseconds." << std::endl;

    return 0;
}
