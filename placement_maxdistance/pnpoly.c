#include<stdio.h>
int main(){

int pnpoly(int nvert, float vertx[], float verty[], float testx, float testy)
{
  int i, j, c = 0;
  for (i = 0, j = nvert-1; i < nvert; j = i++) {
  printf("i = %d, j = %d\n", i, j);
    if ( ((verty[i]>testy) != (verty[j]>testy)) &&
	 (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) )
       c = !c;
  }
  return c;
};
_Bool a = 1;
float b[4] = {0.0, 0.0, 100.0, 100.0};
float c[4] = {0.0, 100.0, 100.0, 0.0};
a = pnpoly(4, b, c, 0.0, -0.0010);
printf("%d\n", a);
}
