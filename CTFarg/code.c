/* 
gcc -fno-stack-protector -z execstack -no-pie reto.c -o reto -m32
*/

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  printf("Ingrese su input: \n");
  char buffer[64];  
  gets(buffer);
  printf("Hola, soy buffer y estoy en la direccion: %p\n",(void*)&buffer);
}