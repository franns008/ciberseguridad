/* gcc version 4.4.3
gcc reto.c -w -O0 -std=c99 -fno-pie -fno-stack-protector -z norelro -z execstack -o reto
*/

#include <stdlib.h>
#include <stdio.h>

void win()
{
  puts("[+] Wow redireccionaste el flujo del programa!");  
  puts("[+] Te mereces una flag: IC{nottherealflag!}\n");
}

void vuln()
{
  char buffer[64];
  printf("[+] Pista: buffer comienza en: %p\n", &buffer);  
  puts("Ingrese su input:");
  fgets(buffer, sizeof(buffer), stdin);
  printf(buffer);	
}

int main(int argc, char **argv)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  vuln();
}



