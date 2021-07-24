#include<stdio.h>
#include<stdint.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<unistd.h>
#include<fcntl.h>
#include<stdlib.h>
#include<errno.h>
#define FU_TYPE 0x1f

void parse_nalu(uint8_t *all, int size, int *offset)
{
  int i = 0;
  int lastoffset = 0;
  int curoffset = 0;
  int curnalu_len = 0;
  while(*offset < size)
  {
	  if ( *(all + *offset) == 0x00 && *(all + *offset + 1) == 0x00 && *(all + *offset + 2) == 0x01)
	  {
                  curnalu_len = *offset - lastoffset;
		  printf("this is start code 2 offset = %d len = %d\n", *offset, curnalu_len);
		  (*offset)+=3;
		  lastoffset = *offset;
                  
	  }
	  else if ( *(all + *offset) == 0x00 && *(all + *offset + 1) == 0x00 && *(all + *offset + 2) == 0x00 && *(all + *offset + 3) == 0x01)
	  {
		  curnalu_len = *offset - lastoffset;
		  curoffset = (*offset);
		  printf("this is start code 3 offset = %d len = %d\n", *offset, curnalu_len);
		  (*offset)+=4;
		  lastoffset = *offset;
	  }
         else
         {
	  	  (*offset)++;
         }
//          printf("offset = %d\n", *offset);
	  
  }
}

int main(int argc, char **argv)
{
   struct stat attr;
   stat(argv[1], &attr) ;
   int fd = open(argv[1], O_RDONLY);
   if (fd < 0)
   {
      printf("open failed\n");
       return 0;
   }
   fstat(fd, &attr) ;
   uint8_t *ptr = calloc(attr.st_size, 1);
   int offset = 0;
   int read_size= 0;
   read_size = read(fd, ptr, attr.st_size);
   printf("%d\n", read_size);
   parse_nalu(ptr, attr.st_size, &offset);

}
