#ifndef FILENAMESYSTEM_H
#define FILENAMESYSTEM_H
#include <QString>
#include <QStringList>
#include "filefilter.h"

// outfile name system
class FileNameSystem
{
private:
    QString allinoneName; //the all in one file name

public:
    FileNameSystem(QString allinoneName="");

    // give some hint for generate the file name
    void SetNameHint(FileFilter *filter);

    // get a file name with some hint
    QString GetAName(QStringList *files, FileFilter *filter);

    // get a file name
    QString GetAName();
};

#endif // FILENAMESYSTEM_H
