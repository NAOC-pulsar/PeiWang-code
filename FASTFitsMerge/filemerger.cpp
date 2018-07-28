#include "filemerger.h"

#include <QDir>
#include <QFileInfo>
#include <QDebug>

#include "fitsutility.h"


extern QTextStream *pConsoleOut;
extern QDebug *pConsoleDebug;

FileMerger::FileMerger(QObject *parent) : QObject(parent){
    connect(this,&FileMerger::BeginMerge,this,&FileMerger::FileMerge);
}

// set the directory that copy the merged fits file to.
void FileMerger::SetOutputDirectory(QString dest){
    outputDirectory = dest.replace("~",QDir::homePath());
}


//Merge files to a single file.
void FileMerger::FileMerge(QStringList files, QString destinationFilename){
    if(files.count()==0) {
        //qDebug()<<"have not files. emit merged signal. ";
        emit Merged(destinationFilename,false);
        return;
    }

    if(!timer.isValid()) timer.start();
    timer.restart();

    int len=files.count();
    std::string *fns= new std::string[len];
    for(int i=0;i<len;++i)
        fns[i] = std::string(files[i].toStdString());

    //int index1 = destinationFilename.lastIndexOf(QDir::separator());
    //int index2 = destinationFilename.indexOf("_");
    //QString subDir;
    //if(index2>=0) subDir=destinationFilename.mid(index1+1,index2-index1-1);
    QFileInfo finfo(destinationFilename);
    QDir dir(outputDirectory);
    //if(!subDir.isEmpty() && !dir.exists(subDir)) dir.mkdir(subDir);
    QString temp = dir.absolutePath() + QDir::separator() + /*(subDir.isEmpty()?"":(subDir+QDir::separator())) + */finfo.fileName();
    std::string outfilename = temp.toStdString();

    //merge files
    bool isOk=mergeFitsFile(fns,len,outfilename);
    delete[] fns;

    if(pConsoleDebug){
        foreach (QString fn, files) {
            *pConsoleDebug<<fn<<" ";
        }
        *pConsoleDebug<<"merge to "<<finfo.fileName()<<endl;
        *pConsoleDebug<<timer.elapsed()<<"ms: "<<finfo.fileName()<<" merged."<<endl;
    }

    //remove source files partially
    for(int i=0;i<1;++i){
        QFile::remove(files[i]);
    }

    //qDebug()<<"emit merged signal. ";
    emit Merged(temp,isOk);
}

//Merge files to a single file.
void FileMerger::FileMerge1(QStringList files){
    if(files.count()==0) return;

    int len=files.count();
    std::string *fns= new std::string[len];
    for(int i=0;i<len;++i)
        fns[i] = std::string(files[i].toStdString());

    QFileInfo finfo(files[0]);
    QDir dir(outputDirectory);
    QString temp = dir.absolutePath() + QDir::separator() + finfo.fileName() + ".merge";
    std::string outfilename(temp.toStdString());

    //merge files
    bool isOk=mergeFitsFile(fns,len,outfilename);

    delete[] fns;

    //remove source files partially
    for(int i=0;i<1;++i){
        QFile::remove(files[i]);
    }

    emit Merged(temp,isOk);
}
