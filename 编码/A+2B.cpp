#include <stdio.h> 
unsigned char XTIME(unsigned char X);
unsigned char mutiply(unsigned char a,unsigned char b);

int main (){
	unsigned char Data_A = 0x41,Data_B = 0x42;
	unsigned char Code_A2B;
	
	//encode 

	Code_A2B = Data_A ^ mutiply(Data_B,2);
	
	printf("A+2B : 0x%x\n",Code_A2B);
	  
	return 0;
}

//有限域乘法 
unsigned char mutiply(unsigned char a,unsigned char b)
{
	unsigned char temp[8] = { a };
	unsigned char result = 0;
	int i = 0;
	for (i = 1;i < 8;i++){
		temp[i] = XTIME(temp[i-1]) ;
	}
	
	result = a * (b & 0x01);
	for(i = 1;i < 8;i++){
		result ^= (((b >> i)&0x01 ) * temp[i]);
	}
	return result;
}

unsigned char XTIME(unsigned char x)
{
	return ( (x << 1) ^ ( (x&0x80) ? 0x1b : 0x00) );
}
