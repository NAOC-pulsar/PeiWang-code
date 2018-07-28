#ifndef FILEFILTER_H
#define FILEFILTER_H
#include <QString>
#include <QStringList>
#include <QList>

typedef enum {DRIFTING,TRACKING} ObserveType;

// e.g. FP20171111_0-1GHz_Dec-0941_drifting_0002.fits
typedef struct {
    int FilterNumber;       // number of this filter
    QStringList Filenames;  //file list
    QString PrecedingName; // file name not contain number and extension. FP20171111_0-1GHz_Dec-0941_drifting
    QString ExtensionName; // file extention: ".fits"
    int NumberLen=0;        // how many digitals is the file number.  4
    long MinNumber;         // minmum file number. 1
    bool IsForceDrifting;
    int FileMergedCount;    // how many files will to merge to a single file
    ObserveType Observe;
    bool IsLowFreq;
} FileFilter;

#endif // FILEFILTER_H
