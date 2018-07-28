#ifndef SETTING_H
#define SETTING_H

// application configuration
typedef struct {
    // directory information
    QString SourceDir,DestDir;
    // polariazation
    int PolNo;
//    // channel number
//    int BeginChannelNo, EndChannelNo;
    // channel frequence
    float BeginChannelFreq, EndChannelFreq;
    // file count to merge to one
    int FileCountToMerge;
    // all tracking file to a single one
    bool IsForceDrifting;
    bool IsHandleDrifting,IsHandleTracking;

    //copy filt to memory
    bool IsCopyFileToMem;

    // the max time legth, by minutes
    float MaxTimeLen;

    // only filt files, not do other thing
    bool OnlyFilt;

    int SpecialFilterNo;

    QStringList FileNameFilters;
} Settings;


#endif // SETTING_H
