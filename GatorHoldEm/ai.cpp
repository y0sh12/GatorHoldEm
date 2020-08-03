#include <cstdint>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <algorithm>
#include <unistd.h>

using namespace std;

extern "C"
{
    int InitTheEvaluator();
    void DoSomeWork();
    int GetHandValue(int * pCards);
    double HandStrength(int* ourcards, int holesize, int* boardcards, int boardsize, int numOpponents);
    void generate(int usedCards[], int usedSize, int fullHand[], bool found, int temp, int index);
    
}


int HR[32487834];


int InitTheEvaluator() {
    memset(HR, 0, sizeof(HR));
    FILE * fin = fopen("res/HandRanks.dat", "rb");
    // Load the HANDRANKS.DAT file data into the HR array
    size_t bytesread = fread(HR, sizeof(HR), 1, fin);
    fclose(fin);
    return 0;
}

void DoSomeWork()
{
    int myCards[] = {5, 9, 13, 17, 26, 30, 34 };
    int handInfo = 0;
    handInfo = GetHandValue(myCards);
    int handCategory = handInfo >> 12;
    int rankWithinCategory = handInfo & 0x00000FFF;
    int ourcards[] = {51, 52};
    int boardcards[] = {3, 51, 31};
    int holesize = sizeof(ourcards)/sizeof(int);
    int boardsize = sizeof(boardcards)/sizeof(int);
    boardsize = 0;
    HandStrength(ourcards, holesize, boardcards, boardsize, 5);
}

void generate(int usedCards[], int usedSize, int fullHand[], bool found, int temp, int index) {
    while(true) {
        temp = rand() % 52 + 1; 
        for(int k = 0; k < usedSize; k++) {
            if(temp == usedCards[k]) {
                found = true;
                break;
            }
        }
            if(!found) {
                usedCards[index] = temp;
                fullHand[index] = temp;
                break;
            }
        found = false;
            }
}

double HandStrength(int* ourcards, int holesize, int* boardcards, int boardsize, const int numOpponents) {
    float ahead = 0;
    float tied = 0; 
    float behind = 0;

    int * fullHand = new int[holesize + 5];
    copy(ourcards, ourcards + holesize, fullHand);
    copy(boardcards, boardcards + boardsize, fullHand + holesize);

    cout << "boardsize" << boardsize << endl;
    cout << "holesize" << holesize << endl;


    int usedSize = holesize + 5 + (numOpponents * 2);

    

    int * usedCards = new int[usedSize];

    for(int i = 0; i < holesize + 5; i++) {
        if(i >= holesize + boardsize) {
            fullHand[i] = 0;
        }
    }

    for(int i = 0; i < usedSize; i++) {
        if(i < holesize + boardsize) {
            usedCards[i] = fullHand[i];
        } else {
            usedCards[i] = 0;
        }
    }


    srand(time(NULL));
    int temp = -1;

    int oppHands[5][2];

    bool found = false;

    //alg start

    int handInfo[5];
    int handCategory[5];
    int rankWithinCategory[5];

    

    int ourHandInfo = GetHandValue(fullHand);
    int ourHandCategory = ourHandInfo >> 12;
    int ourRankWithinCategory = ourHandInfo & 0x00000FFF;


    for(int c = 0; c < 1000000; c++) {


        for(int i = 0; i < usedSize; i++) {
            if(i < holesize + boardsize) {
                usedCards[i] = fullHand[i];
            } else {
                usedCards[i] = 0;
            }
        }

        if (boardsize == 0) {
            generate(usedCards, usedSize, fullHand, found, temp, 2);
            generate(usedCards, usedSize, fullHand, found, temp, 3);
            generate(usedCards, usedSize, fullHand, found, temp, 4);
            generate(usedCards, usedSize, fullHand, found, temp, 5);
            generate(usedCards, usedSize, fullHand, found, temp, 6);
        }
        
        if(boardsize == 3) {
            generate(usedCards, usedSize, fullHand, found, temp, 5);
            generate(usedCards, usedSize, fullHand, found, temp, 6);
        }


        if (boardsize == 4) {
            generate(usedCards, usedSize, fullHand, found, temp, 6);
        }

        ourHandInfo = GetHandValue(fullHand);
        ourHandCategory = ourHandInfo >> 12;
        ourRankWithinCategory = ourHandInfo & 0x00000FFF;




        for(int i = 0; i < 5; i++) {
            handInfo[i] = 0;
            handCategory[i] = 0;
            rankWithinCategory[i] = 0;
        }
        // for(int i = 0; i < usedSize; i++) {
        //     if(i < holesize + boardsize) {
        //         usedCards[i] = fullHand[i];
        //     } else {
        //         usedCards[i] = 0;
        //     }
        // }
        //

        int index = 7;
        for(int i = 0; i < numOpponents; i++) {
            while(true) {
                temp = rand() % 52 + 1; 
                for(int k = 0; k < usedSize; k++) {
                    if(temp == usedCards[k]) {
                        found = true;
                        break;
                    }
                }
                if(!found) {
                    oppHands[i][0] = temp;
                    usedCards[index] = temp;
                    index++;
                    break;
                }
                found = false;
            }
            while(true) {
                temp = rand() % 52 + 1; 
                for(int k = 0; k < usedSize; k++) {
                    if(temp == usedCards[k]) {
                        found = true;
                        break;
                    }
                }
                if(!found) {
                    oppHands[i][1] = temp;
                    usedCards[index] = temp;
                    index++;
                    break;
                }
                found = false;
            }
        }

        for (int i = 0; i < numOpponents; i++) {
            int theirCards[] = {fullHand[2], fullHand[3], fullHand[4], fullHand[5], fullHand[6], oppHands[i][0], oppHands[i][1]};
            handInfo[i] = GetHandValue(theirCards);
            handCategory[i] = handInfo[i] >> 12;
            rankWithinCategory[i] = handInfo[i] & 0x00000FFF;
        }
        
        int maxCategory = 0;
        int maxRank = 0;
        int bestHandIndex = -1;
        for(int i = 0; i < numOpponents; i++) {
            maxCategory = max(maxCategory, handCategory[i]);
        }
        for(int i = 0; i < numOpponents; i++) {
            if(handCategory[i] == maxCategory) {
                int temp = maxRank;
                maxRank = max(maxRank, rankWithinCategory[i]);
                if(temp != maxRank) {
                    bestHandIndex = i;
                }
            }
        }



        
        if(ourHandCategory < maxCategory) {
            behind++;
        } else if(ourHandCategory > maxCategory) {
            ahead++;
        } else if(ourHandCategory == maxCategory) {
            if(ourRankWithinCategory > maxRank) {
                ahead++;
            } else if(ourRankWithinCategory == maxRank) {
                tied++;
            } else {
                behind++;
            }
        }
    }
    cout << "Ahead: " << ahead << endl;
    cout << "Behind: " << behind << endl;
    cout << "Tied: " << tied << endl;

    double handStrength = (ahead + tied / 2) / (ahead + tied + behind);
    cout << "Hand Strength: " << handStrength * 100 << "%" << endl;
    return handStrength;


}

int GetHandValue(int* pCards)
{
    int p = HR[53 + *pCards++];
    p = HR[p + *pCards++];
    p = HR[p + *pCards++];
    p = HR[p + *pCards++];
    p = HR[p + *pCards++];
    p = HR[p + *pCards++];
    return HR[p + *pCards++];
}

