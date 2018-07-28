#ifndef FILEEXTRACTOR_H
#define FILEEXTRACTOR_H

#include <QObject>
#include <QDir>
#include <QString>

// Extract data from initial fits file
class FileExtractor : public QObject
{
    Q_OBJECT

private:
    QString fileDestinationDirectory;
    //QString destSubDirectory; // this directory will be created under destDestDir.
    QDir destDestDir;
    long long counter = 0; // the count of fits file that waiting to extract
    ///////// extract parameters
    int polarNo;
    float startFrequencyChannelFreq, endFrequencyChannelFreq;
    bool isChannelReverse;
    ////////  parameters end

public:
    explicit FileExtractor(QObject *parent = nullptr);

    void SetPolarNo(int polNo);

    void SetFrequencyChannelRange(float lowFrequencyChannelFreq, float highFrequencyChannelFreq, bool isChannelDataReverse=false);

    // set the directory where store the output fits files
    void SetFileDestinationDirectory(QString destinationDirectory, QString subDirectory="extracted");

signals:
    // When a fits file has been extracted, this single will be fired.
    void Extracted(QString extractedFileName, bool isSuccess);

public slots:
    // extract a fits file
    void FitsFileExtract(QString filename, bool isRemove);

    // delete the extracted files in the destination deirectory
    void DeleteFiles();

};

#endif // FILEEXTRACTOR_H
