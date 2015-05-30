#include "piece.h"
#include <cmath>
#include <iostream>

Piece::Piece(int type, int displaySize) : type(type), isWhite(type >= 0), displaySize(displaySize) {

	if (displaySize != 9){
		char displayChar;
		display = "";
		
		switch (type){
			case WHITE_KING:
				displayChar = 'K';
				break;
            case BLACK_KING:
                displayChar = 'k';
                break;
			case WHITE_QUEEN:
				displayChar = 'Q';
				break;
            case BLACK_QUEEN:
                displayChar = 'q';
                break;
			case WHITE_BISHOP:
				displayChar = 'B';
				break;
            case BLACK_BISHOP:
                displayChar = 'b';
                break;
			case WHITE_KNIGHT:
				displayChar = 'N';
				break;
            case BLACK_KNIGHT:
                displayChar = 'n';
                break;
			case WHITE_ROOK:
				displayChar = 'R';
				break;
            case BLACK_ROOK:
                displayChar = 'r';
                break;
			case WHITE_PAWN:
				displayChar = 'P';
				break;
            case BLACK_PAWN:
                displayChar = 'p';
                break;
			default:
				displayChar = ' ';
		}

		for (int i = 0; i < displaySize; i++){
			display += displayChar;
		}
	} else {
		// display size == 9

		switch (type){
		case WHITE_KING:
			display = "WHT   KNG";
			break;
		case BLACK_KING:
			display = "blk   kng";
			break;
		case WHITE_QUEEN:
			display = "WHT   QUE";
			break;
		case BLACK_QUEEN:
			display = "blk   que";
			break;
		case WHITE_BISHOP:
			display = "WHT   BSH";
			break;
		case BLACK_BISHOP:
			display = "blk   bsh";
			break;
		case WHITE_KNIGHT:
			display = "WHT   NHT";
			break;
		case BLACK_KNIGHT:
			display = "blk   nht";
			break;
		case WHITE_ROOK:
			display = "WHT   ROO";
			break;
		case BLACK_ROOK:
			display = "blk   roo";
			break;
		case WHITE_PAWN:
			display = "WHT   PWN";
			break;
		case BLACK_PAWN:
			display = "blk   pwn";
			break;
		default:
			display = "         ";
		}
	}
}