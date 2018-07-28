#ifndef UTILITY_H
#define UTILITY_H

#include <sys/sysinfo.h>

class Utility{
public:
    // get the RAM usage information
    static void GetMemInfo(unsigned long *totalMemory_MB, unsigned long *freeMemory_MB){
        struct sysinfo myinfo;
        sysinfo(&myinfo);
        *totalMemory_MB = (myinfo.mem_unit * myinfo.totalram / 1024 / 1024);
        *freeMemory_MB = (myinfo.mem_unit * myinfo.freeram / 1024 / 1024);
    }
};



#endif // UTILITY_H
