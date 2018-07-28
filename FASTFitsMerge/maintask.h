#ifndef MAINTASK_H
#define MAINTASK_H

#include <QObject>
#include <QString>
#include <QThread>
#include <QList>
#include <QElapsedTimer>
#include <QDebug>
#include <QTextStream>

#include "setting.h"
#include "filefilter.h"
#include "fileprovider.h"
#include "fileextractor.h"
#include "filemerger.h"
#include "filenamesystem.h"

// work bussiness
class MainTask : public QObject
{
    Q_OBJECT

public:
    explicit MainTask(QObject *parent = 0);
    explicit MainTask(Settings setting, QObject *parent = 0);

private:
    Settings setting;
    QThread fileCopyThread;
    QThread fileExtractThread;
    QThread fileMergeThread;

    FileMerger fm;
    FileProvider fp;
    FileExtractor fe;

    //int filesCount = 2; // the  number of files that be merged as a big file.
    QStringList files; // the list of files waiting to merge.
    long totalFiles=0;

    QList<FileFilter> filters;
    int currentFileFilterIndex;
    FileNameSystem nameSystem;

    QElapsedTimer timer;
    void GetFilters(QString directory,QStringList filters, QList<FileFilter> &filterList);

    //QTextStream consoleOut;

public slots:
    // file is extracted.
    void FitsExtracted(QString filename, bool isOk);

    // file is merged.
    void FitsMerged(QString filename, bool isOk);

    // when fileprovider is done, the copied file count will fire.
    void FileCounted(long count);

    void FileStoped();

    // to do work.
    void run();

signals:
    void DeleteFiles();

    // task finished
    void finished();
};

#endif // MAINTASK_H
