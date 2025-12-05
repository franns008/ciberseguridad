/*
gcc reto.c -w -O0 -std=c99 -fno-pie -fno-pic -fno-stack-protector -z norelro -o reto-fixed
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>

void win() {
  system("/bin/sh");
}

int main(int argc, char **argv) {

  setvbuf(stdout, NULL, _IONBF, 0);

  char buf[256];
  
  unsigned int address;
  unsigned int value;

  puts("Porque soy bueno, te dejare escribir 4 bytes en memoria. En que direccion quieres escribirlos?");
  scanf("%x", &address);

  sprintf(buf, "Ok, ahora dime los 4 bytes que quieres escribir en 0x%x", address);
  puts(buf);
  
  scanf("%x", &value);

  sprintf(buf, "Ok, escribiendo 0x%x en 0x%x", value, address);
  puts(buf);

  *(unsigned int *)address = value;

  puts("bye...\n");
  exit(1);
  
}