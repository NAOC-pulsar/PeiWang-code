#ifndef FILEPROVIDER_H
#define FILEPROVIDER_H

#include <QObject>
#include <QString>
#include <QStringList>
#include <QReadWriteLock>
#include "filefilter.h"

//Copy the fits file to other directory.
//Usually, this files should copy to memory, such as /dev/shm
class FileProvider : public QObject
{
    Q_OBJECT

public:
    explicit FileProvider(QObject *parent = nullptr);
    void SetSourceDirectory(QString source);
    void SetDestinationDirectory(QString destination);
    void SetFileFilter(FileFilter filter);
    void ClearFileFliter();

private:
    QString sourceDirectory; //will search all the directory and files in this directory    
    QString destinationDirectory; //the files will be stored to this directory
    QStringList fileList; // the files that will be handled.
    FileFilter fileFilter;
    bool willExit=false;

    long notHandledCounter=0; // file count waiting to handle (extract and merge).
    QReadWriteLock counterLocker; // locker for counter
    int MaxWaitingFiles=4;

public:
    // return the file count wating to handle.
    long Counter();

    void ResetCounter();

    // add one to the file counter
    void IncreaseCounter();

    // decrease one to the file counter
    void DecreaseCounter();

    // Read all the files contained in the the source directory.
    bool ReadAllFile();

signals:
    // When fits file is ready to extract, this signal will be fired.
    void FileReady(QString fullFilename,bool isRemove);

    // the count of files
    void FilesCounted(long count);

    // all file copying operations stoped.
    void Stoped();

public slots:
    // delete the files in destination files
    void DeleteFiles();

    void Stop(){
        willExit=true;
    }
};

#endif // FILEPROVIDER_H
