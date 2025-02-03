#include <cstdio>

int cnt;

int main(void){
    char c , str[200005];
    freopen("tmp\\out_file" , "r" , stdin);
    printf("\033[0m");
    while(~scanf("%c" , &c))
        str[cnt++] = c;
    printf("%s" , str);
    fclose(stdin);
}