#include "fileprovider.h"
#include <QDir>
#include <QStorageInfo>
#include <QDebug>
#include <QThread>
#include <QElapsedTimer>
#include "utility.h"
#include "fitsutility.h"

extern QTextStream *pConsoleOut;
extern QDebug *pConsoleDebug;

FileProvider::FileProvider(QObject *parent) : QObject(parent){

}

void FileProvider::SetSourceDirectory(QString source){
    sourceDirectory=source.replace("~",QDir::homePath());
}

void FileProvider::SetDestinationDirectory(QString destination) {
    destinationDirectory=destination.replace("~",QDir::homePath());
}

void FileProvider::SetFileFilter(FileFilter filter){
    fileFilter=filter;
}

void FileProvider::ClearFileFliter(){
    fileFilter=FileFilter();
}

void FileProvider::ResetCounter(){
    counterLocker.lockForWrite();
    notHandledCounter=0;
    counterLocker.unlock();
}

// return the file count waiting to handle.
long FileProvider::Counter(){
    long temp;
    counterLocker.lockForRead();
    temp=notHandledCounter;
    counterLocker.unlock();
    return temp;
}

// add one to the file counter
void FileProvider::IncreaseCounter(){
    counterLocker.lockForWrite();
    notHandledCounter++;
    counterLocker.unlock();
}

// decrease one to the file counter
void FileProvider::DecreaseCounter(){
    counterLocker.lockForWrite();
    notHandledCounter--;
    counterLocker.unlock();
}

// Read all the files contained in the filter. NOT the source directory.
bool FileProvider::ReadAllFile(){
    notHandledCounter=0;
    willExit=false;
    if(fileFilter.Filenames.count()==0) return true;

    if(destinationDirectory.isEmpty() || destinationDirectory.isNull()){
        emit FilesCounted(fileFilter.Filenames.count());

        //copy file to subdeirector
        for(int i=0;(i<fileFilter.Filenames.count())&&(!willExit); ++i){ // for every file
            if(pConsoleDebug){
                //*pConsoleOut<<"Details: "<<fileFilter.Filenames[i]<<endl;
                //readheader(fileFilter.Filenames[i].toStdString().data());
            }
            bool isDone=false;
            while(!isDone && !willExit){ // is copying done?
                if(Counter()<MaxWaitingFiles){
                    IncreaseCounter();
                    isDone=true;
                    emit FileReady(fileFilter.Filenames[i],false);
                }else{
                    //qDebug()<<"File provider wait to copy file.";
                    QThread::usleep(0.5*1000000);
                }
            }
        }
        while(Counter()!=0) QThread::usleep(0.5*1000000);

        emit Stoped();
    }
    else{
        QDir destDir(destinationDirectory);
        if(!destDir.exists()){
            if(pConsoleOut) *pConsoleOut<<destinationDirectory<<" does not exists."<<endl;
            return false;
        }
        //create a destination subdirectory
        QFileInfo fileInfo(fileFilter.Filenames.first());
        QString destSubDirectory = fileInfo.dir().dirName();
        if(!destDir.exists(destSubDirectory) && !destDir.mkdir(destSubDirectory)){
            if(pConsoleOut) *pConsoleOut<<"make directory "<</*destDir.absolutePath()<<QDir::separator()<<*/destSubDirectory<<" fail."<<endl;
            return false;
        }

        emit FilesCounted(fileFilter.Filenames.count());

        QElapsedTimer timer;
        timer.start();
        qint64 time;
        //copy file to subdeirector
        QStorageInfo destDirInfo(destDir.absolutePath());
        for(int i=0;(i<fileFilter.Filenames.count())&&(!willExit); ++i){ // for every file
            if(pConsoleDebug){
                //*pConsoleOut<<"Details: "<<fileFilter.Filenames[i]<<endl;
                //readheader(fileFilter.Filenames[i].toStdString().data());
            }
            fileInfo=QFileInfo(fileFilter.Filenames[i]);
            QString sourceFilename=fileFilter.Filenames[i];
            QString destinationFilename=destDir.absolutePath()+QDir::separator()+destSubDirectory+QDir::separator()+fileInfo.fileName();
            bool isDone=false;
            while(!isDone && !willExit){ // is copying done?
                destDirInfo.refresh();
                //qDebug()<<destDirInfo.bytesFree()<<"   "<<2*list[i].size();
                if(Counter()<MaxWaitingFiles && destDirInfo.bytesFree()>2*fileInfo.size()){ // the file waiting to handle isnot too more and free memory size >double of file size
                    //qDebug()<<"File provider is copying file "<<sourceFilename;
                    IncreaseCounter();
                    time = timer.elapsed();
                    QFile::copy(sourceFilename,destinationFilename);
                    time = timer.elapsed() - time;
                    if(pConsoleDebug) *pConsoleDebug<<time<<"ms: copy file "<<fileInfo.fileName()<<endl;
                    isDone=true;
                    emit FileReady(destinationFilename,true);
                }else{
                    //qDebug()<<"File provider wait to copy file.";
                    QThread::usleep(0.5*1000000);
                }
            }
        }
        while(Counter()!=0) QThread::usleep(0.5*1000000);
        emit Stoped();
    }
    return true;
}

void FileProvider::DeleteFiles(){
    if(!destinationDirectory.isEmpty()){
        QDir sourceDir(sourceDirectory);
        QDir destDir(destinationDirectory);
        QDir(destDir.absolutePath()+QDir::separator()+sourceDir.dirName()).removeRecursively();
    }
}
