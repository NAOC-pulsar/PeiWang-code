#include "fileextractor.h"

#include <QFileInfo>
#include <QDebug>
#include <QElapsedTimer>
#include "fitsutility.h"

extern QTextStream *pConsoleOut;
extern QDebug *pConsoleDebug;

FileExtractor::FileExtractor(QObject *parent) : QObject(parent){
    polarNo=1;
}

void FileExtractor::SetPolarNo(int polNo){ this->polarNo=polNo;}

void FileExtractor::SetFrequencyChannelRange(float lowFrequencyChannelFreq, float highFrequencyChannelFreq, bool isChannelDataReverse){
    this->startFrequencyChannelFreq=lowFrequencyChannelFreq;
    this->endFrequencyChannelFreq=highFrequencyChannelFreq;
    isChannelReverse=isChannelDataReverse;
}

// set the directory where store the output fits files
void FileExtractor::SetFileDestinationDirectory(QString destinationDirectory, QString destSubDirectory){
    fileDestinationDirectory=destinationDirectory.replace("~",QDir::homePath());
    destDestDir.setPath(destinationDirectory);    
    if(!destDestDir.exists(destSubDirectory) && !destDestDir.mkdir(destSubDirectory)){
        if(pConsoleOut) *pConsoleOut<<"make directory "<</*destDestDir.absolutePath()<<QDir::separator()<<*/destSubDirectory<<" fail."<<endl;
        return;
    }
    destDestDir.cd(destSubDirectory);
}

// extract a fits file
void FileExtractor::FitsFileExtract(QString filename, bool isRemove){
    QElapsedTimer timer;
    timer.start();
    //SetFileDestinationDirectory(fileDestinationDirectory);
    counter++;
    QFileInfo fileInfo(filename);
    QString outFileName = destDestDir.absolutePath() + QDir::separator() + fileInfo.fileName();//.completeBaseName()/* + "_extracted.fits"*/;
    bool isOk=extractFits(filename.toStdString(), startFrequencyChannelFreq, endFrequencyChannelFreq, polarNo, outFileName.toStdString(),isChannelReverse);
    if(pConsoleDebug) *pConsoleDebug<<timer.elapsed()<<"ms: "<<fileInfo.fileName()<<" extract done."<<endl;
    emit Extracted(outFileName,isOk);
    if(isRemove) QFile::remove(filename);
    counter--;
}

void FileExtractor::DeleteFiles(){
    QDir(destDestDir.absolutePath()).removeRecursively();
    destDestDir.cdUp();
}
