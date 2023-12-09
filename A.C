#include<stdio.h>
#include<conio.h>
#define SnCount 12       //SN byte quantity
#define PowerNum_Count 8  //Power number quantity
unsigned long  LockID[3]={0x2D323639,0x53555311,0x002C0004};
unsigned long  TempLockID[3]={0x2D323639,0x53555311,0x002C0004};
unsigned char PowerNumArray[8];

void InitArray() //clear array 
{
	int i;
	for (i=0; i <8; i++){
	PowerNumArray[i]=0;	
	}
}

void PrintArray() //print out for test
{
	int i;
	printf(" PN Number:");
	for (i=0; i <8; i++){
	printf("%d ", PowerNumArray[i]);
	}
}


void test()
{									
	unsigned long i,j,k,m;
	//program 
    //***************************************************************
	//*approach to get power number:	 		  					* 
	//*Let all byte change to cause difference.   					*
	//*need payattention for data overflow will case data break.	*
    //*************************************************************** 
    	j =(LockID[2] + (LockID[2]>>8) + (LockID[2]>>16) + (LockID[2]>>24))&0x0000000FF ; // as the feedback of Shao, need to care about unknow which byte is change, add last 4 bytes
    	if (j==0){j=1;} //to avoid j=0, which will cause power number to be 00 after * operation.

    	k =(LockID[1] + (LockID[1]>>8) + (LockID[1]>>16) + (LockID[1]>>24))&0x000000FF ; // as the feedback of Shao, need to care about unknow which byte is change, add middle 4 bytes
    	if (k==0){k=1;}

    	m =(LockID[0] + (LockID[0]>>8) + (LockID[0]>>16) + (LockID[0]>>24))&0x000000FF ; // as the feedback of Shao, need to care about unknow which byte is change, add middle 4 bytes
    	if (m==0){m=1;}
    
    for (i=0; i <8; i++){ 
    	
    	//if (i%2==0&&PowerNumArray[i]!=9) {PowerNumArray[i]++;}  		
    	
    	LockID[0]=((LockID[0]>>4)+j*k*m);

    	LockID[1]=((LockID[1]>>4)+j*k*m);

    	LockID[2]=((LockID[2]>>4)+j*k*m);
    	PowerNumArray[i] = (LockID[0]+LockID[1]+LockID[2])%10;  //add 32bit serial to one 32bit data
	}	
}


int main(int argc, char *argv[])
{
    int x;
    int y;
    int z;

    sscanf(argv[1], "%x", &x);
    sscanf(argv[2], "%x", &y);
    sscanf(argv[3], "%x", &z);

    LockID[0]=x;
    LockID[1]=y;
    LockID[2]=z;

    TempLockID[0]=x;
    TempLockID[1]=y;
    TempLockID[2]=z;

	//int n=0;
	printf("input SN: %08llX,%08llX,%08llX, \n",LockID[0],LockID[1],LockID[2]);
	//for (n=0; n<1;n++){
	//	TempLockID[2]= TempLockID[2]; //+(n+1)*0x10;  // only for test to ensure any byte change will get different Power Number
		LockID[0]=TempLockID[0];
		LockID[1]=TempLockID[1];
		LockID[2]=TempLockID[2];

		InitArray();
		//printf("\n OrgiSN byte11 +1: ");
		test();	      // this one is core program
		PrintArray(); // only for test
	//}
	return 0;
}