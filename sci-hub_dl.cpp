#include <iostream>
#include <string>
extern char binary_sci_hub_dl_py_end[];
extern int binary_sci_hub_dl_py_size;
extern char binary_sci_hub_dl_py_start[];
int main()
{
    FILE* fp;
    *binary_sci_hub_dl_py_end = '\0';
    fp = fopen("C:\\__sci-hub_dl__.py", "w");
    fprintf(fp, "%s", binary_sci_hub_dl_py_start);
    fflush(fp);
    fclose(fp);
	system("python C:\\__sci-hub_dl__.py");
}
