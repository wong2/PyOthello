#include <stdio.h>
#define INFINITY 99999
#define BLANK 0
#define BLACK 1
#define WHITE 2
#define MAXDEPTH 6

struct Pos{
    int row, col;
}bestPos;
char nowplaying;
int ppp = 0;
int pattern[81] = { 0, -70, 70, 20, -65, 75, -20, -75, 65, -50, -90, 60, -10, -100, 60,
      -120, -150, -60, 50, -60, 90, 120, 60, 150, 10, -60, 100, 190, 230,
      220, 200, 250, 240, 185, 225, 180, 220, 270, 260, 235, 300, 275, 210,
      280, 250, 200, 265, 195, 185, 240, 183, 210, 250, 230, -190, -220, 230,
      -185, -180, -225, -200, -240, -250, -200, -195, -265, -210, -230, -250,
      -185, -183, -240, -220, -260, -270, -210, -250, -280, -235, -275, -300 };

char getAvlbMoves(char* board, char color, char* moves)
{
    char i, j, k, n=0;
    char unColor = 3 - color;

    for(i=0; i<8; i++)
        for(j=0; j<8; j++){
            if(board[i*8+j] == color){
                /* Search in the up direction */
                if(i > 1){
                    k = 1;
                    while(i-k>=0 && board[(i-k)*8+j]==unColor)
                        k++;
                    if(k>1 && i-k>=0 && board[(i-k)*8+j]==0){
                        moves[n++] = (i-k)*8+j;
                    }
                }
                /* Search in the down direction */
                if(i < 6){
                    k = 1;
                    while(i+k<=7 && board[(i+k)*8+j]==unColor)
                        k++;
                    if(k>1 && i+k<=7 && board[(i+k)*8+j]==0){
                        moves[n++] = (i+k)*8+j;
                    }
                }
                /* Search in the left direction */
                if(j > 1){
                    k = 1;
                    while(j-k>=0 && board[i*8+j-k]==unColor)
                        k++;
                    if(k>1 && j-k>=0 && board[i*8+j-k]==0){
                        moves[n++] = i*8+j-k;
                    }
                }
                /* Search in the right direction */
                if(j < 6){
                    k = 1;
                    while(j+k<=7 && board[i*8+j+k]==unColor)
                        k++;
                    if(k>1 && j+k<=7 && board[i*8+j+k]==0){
                        moves[n++] = i*8+j+k;
                    }
                }
                /* Search in the northwest direction */
                if(i > 1 && j > 1){
                    k = 1;
                    while(i-k>=0 && j-k>=0 && board[(i-k)*8+j-k]==unColor)
                        k++;
                    if(k>1 && i-k>=0 && j-k>=0 && board[(i-k)*8+j-k]==0){
                        moves[n++] = (i-k)*8+j-k;
                    }
                }
                /* Search in the northeast direction */
                if(i > 1 && j < 6){
                    k = 1;
                    while(i-k>=0 && j+k<=7 && board[(i-k)*8+j+k]==unColor)
                        k++;
                    if(k>1 && i-k>=0 && j+k<=7 && board[(i-k)*8+j+k]==0){
                        moves[n++] = (i-k)*8+j+k;
                    }
                }
                /* Search in the southwest direction */
                if(i < 6 && j > 1){
                    k = 1;
                    while(i+k<=7 && j-k>=0 && board[(i+k)*8+j-k]==unColor)
                        k++;
                    if(k>1 && i+k<=7 && j-k>=0 && board[(i+k)*8+j-k]==0){
                        moves[n++] = (i+k)*8+j-k;
                    }
                }
                /* Search in the southeast direction */
                if(i < 6 && j < 6){
                    k = 1;
                    while(i+k<=7 && j+k<=7 && board[(i+k)*8+j+k]==unColor)
                        k++;
                    if(k>1 && i+k<=7 && j+k<=7 && board[(i+k)*8+j+k]==0){
                        moves[n++] = (i+k)*8+j+k;
                    }
                }
            }
        }
        moves[n] = -1;
        return n;
}

void updateBoard(char board[], char pos, char color, char * updated)
{
    char k, p, n, row, col, tmp;
    char unColor = 3 - color;
    row = pos / 8;
    col = pos % 8;
    n = 0;
    board[pos] = color;
    /* Search in the up direction */
    if(row > 1)
    {
        k = 1;
        while(row-k>=0 && board[(row-k)*8+col]==unColor)
            k++;
        if(k>1 && row-k>=0 && board[(row-k)*8+col]==color){
            for(p=1; p<k; p++){
                tmp = (row-p)*8+col;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }
    /* Search in the down direction */
    if(row < 6)
    {
        k = 1;
        while(row+k<=7 && board[(row+k)*8+col]==unColor)
            k++;
        if(k>1 && row+k<=7 && board[(row+k)*8+col]==color){
            for(p=1; p<k; p++){
                tmp = (row+p)*8+col;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }

    /* Search in the left direction */
    if(col > 1)
    {
        k = 1;
        while(col-k>=0 && board[row*8+col-k]==unColor)
            k++;
        if(k>1 && col-k>=0 && board[row*8+col-k]==color){
            for(p=1; p<k; p++){
                tmp = row*8+col-p;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }

    /* Search in the right direction */
    if(col < 6)
    {
        k = 1;
        while(col+k<=7 && board[row*8+col+k]==unColor)
            k++;
        if(k>1 && col+k<=7 && board[row*8+col+k]==color){
            for(p=1; p<k; p++){
                tmp = row*8+col+p;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }
    /* Search in the northwest direction */
    if(row > 1 && col > 1)
    {
        k = 1;
        while(row-k>=0 && col-k>=0 && board[(row-k)*8+col-k]==unColor)
            k++;
        if(k>1 && row-k>=0 && col-k>=0 && board[(row-k)*8+col-k]==color){
            for(p=1; p<k; p++){
                tmp = (row-p)*8+col-p;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }
    /* Search in the northeast direction */
    if(row > 1 && col < 6)
    {
        k = 1;
        while(row-k>=0 && col+k<=7 && board[(row-k)*8+col+k]==unColor)
            k++;
        if(k>1 && row-k>=0 && col+k<=7 && board[(row-k)*8+col+k]==color){
            for(p=1; p<k; p++){
                tmp = (row-p)*8+col+p;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }
    /* Search in the southwest direction */
    if(row < 6 && col > 1)
    {
        k = 1;
        while(row+k<=7 && col-k>=0 && board[(row+k)*8+col-k]==unColor)
            k++;
        if(k>1 && row+k<=7 && col-k>=0 && board[(row+k)*8+col-k]==color){
            for(p=1; p<k; p++){
                tmp = (row+p)*8+col-p;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }
    /* Search in the southeast direction */
    if(row < 6 && col < 6)
    {
        k = 1;
        while(row+k<=7 && col+k<=7 && board[(row+k)*8+col+k]==unColor)
            k++;
        if(k>1 && row+k<=7 && col+k<=7 && board[(row+k)*8+col+k]==color){
            for(p=1; p<k; p++){
                tmp = (row+p)*8+col+p;
                board[tmp] = color;
                updated[n++] = tmp;
            }
        }
    }

    updated[n] = -1;
}

double evaluation(char* board, char color)
{
    char mobilityB, mobilityW, pMobB, pMobW, pos, moves[40], i, j, sign;
    int patternValue;
    sign = (color==nowplaying?1:-1);
    mobilityB = getAvlbMoves(board,BLACK, moves);
    mobilityW = getAvlbMoves(board, WHITE, moves);
    pMobB = pMobW = 0;
    for(i=9; i<15; i++)
        for(j=0; j<6; j++){
            pos = i + j*8;
            if(board[pos] == BLACK){
                pos = pos + pos % 8;
                if(!board[pos-9] || !board[pos-8] || !board[pos-7] || !board[pos-1] || !board[pos+8] || !board[pos+7] || !board[pos+9] || !board[pos+1])
                    pMobB++;
            }
            else if(board[pos] == WHITE){
                pos = pos + pos % 8;
                if(!board[pos-9] || !board[pos-8] || !board[pos-7] || !board[pos-1] || !board[pos+8] || !board[pos+7] || !board[pos+9] || !board[pos+1])
                    pMobW++;
            }
        }
    patternValue =   pattern[27*board[0]+9*board[8]+3*board[16]+board[9]]+
                     pattern[27*board[0]+9*board[1]+3*board[2]+board[9]]+
                     pattern[27*board[7]+9*board[6]+3*board[5]+board[14]]+
                     pattern[27*board[7]+9*board[15]+3*board[23]+board[14]]+
                     pattern[27*board[56]+9*board[48]+3*board[40]+board[49]]+
                     pattern[27*board[56]+9*board[57]+3*board[58]+board[49]]+
                     pattern[27*board[63]+9*board[62]+3*board[61]+board[54]]+
                     pattern[27*board[63]+9*board[55]+3*board[47]+board[54]];
/*(mobilityB-mobilityW)*10 + (pMobW - pMobB)*12*/
    //printf("%lf\n", (double)patternValue*10);
    return  (double)sign*(patternValue*10+(mobilityB-mobilityW)*10+(pMobW - pMobB)*12);
}

double endEval(char board[], char color)
{
	char b, w, e, i, sign = 0;
	sign = (color==nowplaying?1:-1);
	for(i=0; i<64; i++)
		if(board[i]==BLACK)
			b++;
		else if(board[i]==WHITE)
			w++;
		else
			e++;
	return (double)sign*((b-w)*100+evaluation(board, color));
}

double alphaBeta(char board[], char depth, double alpha, double beta, char color)
{
    char moves[40], updated[40];
    char i, j, n, no, pos;
    double  value, bestValue=-INFINITY;

    no = getAvlbMoves(board, 3-color, moves);
    n = getAvlbMoves(board, color, moves);

	if(no==0 && n==0)
		return endEval(board, color);

    if(depth == 0)
        return evaluation(board, color);

    /*orderMoves(moves, n);*/
    for(i=0; i<n; i++){
        pos=moves[i];
        //printf("\nrow: %d, col: %d\n", row, col);
        ppp++;
        board[pos] = color;
        updateBoard(board, pos, color, updated);
        value = -alphaBeta(board, depth-1, -beta, -(alpha>bestValue?alpha:bestValue), 3-color);

        board[pos] = BLANK;
        j = 0;
        while(updated[j] != -1){
            board[updated[j]] = 3-color;
            j++;
        }

        if(value >= bestValue)
        {
            if(depth == MAXDEPTH){
                bestPos.row = pos / 8;
                bestPos.col = pos % 8;
            }
            bestValue = value;
        }

        if(bestValue >= beta)
            break;
    }
    return bestValue;
}

int giveNextMove(char *pieces, char color)
{
    char board[64], moves[30], i, n;
    for(i=0; i<64; i++)
            board[i] = pieces[i];
    nowplaying = color;
    n = getAvlbMoves(board, color, moves);
    if(!n)
        return -1;
    if(n==1)
    {
        bestPos.row = moves[0]/8;
        bestPos.col = moves[0]%8;
    }
    else
        alphaBeta(board, MAXDEPTH, -INFINITY, INFINITY, color);
    return bestPos.row * 10 + bestPos.col;
}

int main()
{
    char moves[30], updated[30];
    char board[64];
    char i, j;
    for(i=0; i<64; i++)
        board[i] = 0;

    board[27] = board[36] = 2;
    board[28] = board[35] = 1;
	nowplaying = BLACK;
    bestPos.row = -1;
    bestPos.col = -1;
    //printf("%d", giveNextMove(board, BLACK));
    alphaBeta(board, MAXDEPTH, -INFINITY, INFINITY, BLACK);
    //negaMax(board, MAXDEPTH, BLACK);
    //printf("%lf", (float)i);
    printf("Best: %d \n ppp: %d ", bestPos.row*8+bestPos.col, ppp);
    //printf("%lf", evaluation(board));
    return 0;
}
