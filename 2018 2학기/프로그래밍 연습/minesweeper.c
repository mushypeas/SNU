#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define BOARD_SIZE		5
#define SQUARE_NUM		(BOARD_SIZE*BOARD_SIZE)
#define MINE_NUM		20
#define SHUFFLE_NUM		100000
#define true            1
#define false           0
void big_rigs();
void reset();
void input_nomines();
void input_mine();
void gameover();
int mine_board[BOARD_SIZE][BOARD_SIZE];
/* 0 : non-mined, 1 : mined */
int display_board[BOARD_SIZE][BOARD_SIZE];
/* -1 : no mines around, 0 : unknown, 1~8 : number of mines */
void init_board();
// initialize mine_board by randomly planting fixed number of mines
void show_interface();
// print display_board
int sweep(int, int);
/*
* sweep a square on (x, y). if there is no mines around square on (x, y), recursively sweep adjacent squares
* return : 1 if player sweeps mined square, else 0
*/

int check_game();
/*
* check if the player swept all non-mined squares
* return : 1 if player swept all non-mined squares, else 0
*/

int main()
{
	init_board();
	while (true)
	{
		show_interface();
		if (check_game() == 1)
		{
			big_rigs();
			return 0;
		}
		int det;
	CHOOSE:
		printf("Input Mine Coordinate: 0\nInput Non-mine Coordinate: 1\n"); 
		//Input Mine Coordinate: Mark a place that is estimated to have a mine
		//Input Non-mine Coordinate: Mark a place that is estimated to not have a mine
		scanf("%d", &det);
		if (det == 0)
			input_mine();
		else if (det == 1)
			input_nomines();
		else
		{
			printf("===================\n    WRONG INPUT\n===================\n");
			goto CHOOSE;
		}
	}
}
void big_rigs() // Over the roads racing
{
	printf("===================\n    YOURE WINNER\n===================\n");
	printf("Try once more?\nYes:1      No:anything but 1\n");
	int YN;
	scanf("%d", &YN);
	if (YN == 1)
	{
		reset();
		main();
	}
}
void gameover()
{
	show_interface();
	printf("===================\n      GAME OVER\n===================\n");
	printf("Try Again?\nYes:1      No:anything but 1\n");
	int YN;
	scanf("%d", &YN);
	if (YN == 1)
	{
		reset();
		main();
	}
	else
		exit(0);
}
void input_nomines()
{
	printf("Input X, Y coordinate: ");
	int X, Y;
	scanf("%d", &Y);
	scanf("%d", &X);
	if (mine_board[X - 1][Y - 1] == 1)
	{
		display_board[X - 1][Y - 1] = -1;
		gameover();
		return;
	}
	else
		sweep(X, Y);
}
void input_mine()
{
	printf("Input X, Y coordinate: ");
	int X, Y;
	scanf("%d", &Y);
	scanf("%d", &X);
	int x = X - 1, y = Y - 1;
	if (mine_board[x][y] == 1)
		display_board[x][y] = -1;
	else if(mine_board[x][y]==0)
		if((x >= 1) && (x <= BOARD_SIZE) && (y >= 1) && (y <= BOARD_SIZE))
			gameover(); // Game over when guessed wrong
	return;
}
void reset() // Restart the game
{
	int n;
	for (n = 0; n < SQUARE_NUM; n++)
	{
		mine_board[0][n] = 0;
		display_board[0][n] = 0;
	}
	return;
}
int sweep(int x, int y)
{
	int X = x - 1; // X, Y is the actual 
	int Y = y - 1; // array address
	if (display_board[X][Y] != 0)
		return 1;
	int minenum = 0;
	int i, j;
	if ((x >= 1) && (x <= BOARD_SIZE) && (y >= 1) && (y <= BOARD_SIZE))
	{

		for (i = -1; i < 2; i++)
		{
			if ((x+i >= 1) && (x+i <= BOARD_SIZE))
			{
				for (j = -1; j < 2; j++)
				{
					if ((y + j >= 1) && (y + j <= BOARD_SIZE))
					{
						if (mine_board[X + i][Y + j] == 1)
							minenum++;
					}
				}
			}
		}
		if (minenum > 0)
		{
			display_board[X][Y] = minenum;
			return 1;
		}
		else
		{
			display_board[X][Y] = -1;
			for (i = -1; i < 2; i++)
			{
				for (j = -1; j < 2; j++)
					sweep(x + i, y + j);
			}
		}
	}
	else
		return 0;
}
void init_board() // Spreads mines randomly
{
	int i;
	int shuffle[BOARD_SIZE * BOARD_SIZE];
	int temp;
	int r1, r2;

	srand(time(NULL)); // set seed

							// initialize shuffle array
	for (i = 0; i<SQUARE_NUM; i++)
		shuffle[i] = i;

	// shuffling
	for (i = 0; i<SHUFFLE_NUM; i++)
	{
		r1 = rand() % SQUARE_NUM;
		r2 = rand() % SQUARE_NUM;

		temp = shuffle[r1];
		shuffle[r1] = shuffle[r2];
		shuffle[r2] = temp;
	}

	// get mine coordinates from shuffled array
	for (i = 0; i<MINE_NUM; i++)
		mine_board[shuffle[i] / BOARD_SIZE][shuffle[i] % BOARD_SIZE] = 1;
}
void show_interface()
{
	int i, j;

	system("cls"); // clear the screen

					 // rest of this function just prints out display_board
	printf("    ");
	for (i = 0; i<BOARD_SIZE; i++)
		printf(" %2d ", i + 1);
	printf("-> X\n");

	for (i = 0; i<BOARD_SIZE; i++)
	{
		printf("\n %2d ", i + 1);

		for (j = 0; j<BOARD_SIZE; j++)
		{
			if (display_board[i][j] == -1)
			{
				if (mine_board[i][j] == 1)
					printf("  * ");
				else
					printf("  X ");
			}
			else if (display_board[i][j] == 0)
				printf("  - ");
			else
				printf("  %d ", display_board[i][j]);
		}
		printf("\n");
	}
	printf("\n  |\n  v\n\n  Y\n\n");
}
int check_game()
{
	int i, j;
	for (i = 0; i < BOARD_SIZE; i++)
	{
		for (j = 0; j < BOARD_SIZE; j++)
			if (display_board[i][j] == 0)
				if(mine_board[i][j] == 0) // Don't have to mark all mines
					return 0;
	}
	return 1; //Returns 1 if all sweeped
}
