#ifndef FILEMERGER_H
#define FILEMERGER_H

#include <QObject>
#include <QString>
#include <QStringList>
#include <QElapsedTimer>

// merge two or more fits file as a big fits file.
// copy the merged file to another directory.
class FileMerger : public QObject
{
    Q_OBJECT

public:
    explicit FileMerger(QObject *parent = nullptr);

    // set the directory that copy the merged fits file to.
    void SetOutputDirectory(QString dest);

private:
    QString outputDirectory;
    QElapsedTimer timer;

signals:
    // the files have been merged
    void Merged(QString fileName, bool isSuccess);

    // begin to merge
    void BeginMerge(QStringList files, QString outfilename);

public slots:
    //Merge files to a single file.
    void FileMerge(QStringList files, QString destinationFilename);

    //Merge files to a single file.
    void FileMerge1(QStringList files);
};

#endif // FILEMERGER_H
