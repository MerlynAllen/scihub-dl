#include <iostream>
#include <string>
extern char binary_sci_hub_dl_py_end[];
extern int binary_sci_hub_dl_py_size;
extern char binary_sci_hub_dl_py_start[];
int main(int argc, char* argv[])
{
    FILE* fp;
    std::string command("python C:\\__sci-hub_dl__.py");
    for (int i = 1; i < argc; ++i)
    {
        command += " ";
        command += argv[i];
    }

    *binary_sci_hub_dl_py_end = '\0';
    fp = fopen("C:\\__sci-hub_dl__.py", "w");
    fprintf(fp, "%s", binary_sci_hub_dl_py_start);
    fflush(fp);
    fclose(fp);

	system(command.c_str());
}
