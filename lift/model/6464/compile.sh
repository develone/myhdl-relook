#/bin/bash
gcc -c lifting.c 
gcc -c error.c
gcc -c pnmio.c
gcc t-rd.c pnmio.o error.o lifting.o -o t-rd
