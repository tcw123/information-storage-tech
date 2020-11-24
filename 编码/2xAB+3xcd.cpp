#include <stdio.h> 
unsigned char XTIME(unsigned char X);
unsigned char mutiply(unsigned char a,unsigned char b);

// 2×AB + 3 × cd = 2×A + 3 × c 拼接2×B + 3 × d
int main (){
	unsigned char Data_A = 0x41,Data_B = 0x42;
    unsigned char Data_c = 0x63,Data_d = 0x64;
	unsigned char Code_Ac,Code_Bd;
	short Code_2AB3cd;
	
	//encode 

	Code_Ac = mutiply(2, Data_A) ^ mutiply(3, Data_c);
	Code_Bd = mutiply(2, Data_B) ^ mutiply(3, Data_d);
    Code_2AB3cd = (Code_Ac << 8) ^ Code_Bd;

	printf("2xAB + 3xcd: 0x%x\n",Code_2AB3cd);
	  
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
