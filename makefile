sci-hub_dl.exe:sci-hub_dl.o script_binary.o
	g++.exe sci-hub_dl.o script_binary.o -o sci-hub_dl.exe
sci-hub_dl.o:sci-hub_dl.cpp
	g++.exe -c sci-hub_dl.cpp
script_binary.o:sci-hub_dl.py
	ld.exe -r -b binary -o script_binary.o sci-hub_dl.py
clean:
	del *.o *.exe
install:sci-hub_dl.exe
	copy sci-hub_dl.exe C:\Windows\
