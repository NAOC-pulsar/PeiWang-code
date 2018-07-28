#include <maintask.h>
#include <QDebug>
#include <QString>
#include <QStringList>
#include <QDir>
#include <QDateTime>
#include <iostream>
#include <fstream>
#include <QCoreApplication>

#include "filefilter.h"
#include "fitsutility.h"


extern QTextStream *pConsoleOut;
extern QDebug *pConsoleDebug;

MainTask::MainTask(QObject *parent) : QObject(parent) {
    timer.start();
}

MainTask::MainTask(Settings setting, QObject *parent): QObject(parent){
    this->setting=setting;
}

void MainTask::FitsExtracted(QString filename,bool isOk){
    if(!isOk){
        emit fm.Merged(filename, false);
        return;
    }
    //timer.restart();
    if(filters[currentFileFilterIndex].IsForceDrifting){
         // merge fits file squencenly every filesCount files.
        files<<filename;
        if(files.count() >= filters[currentFileFilterIndex].FileMergedCount || totalFiles< filters[currentFileFilterIndex].FileMergedCount){ // there are enough files to merge
            emit fm.BeginMerge(files,nameSystem.GetAName(&files, &(filters[currentFileFilterIndex])));
            files.removeFirst();
        }
    }
    else{
        // merge many files to a single one.
        //qDebug()<<filename<<endl;
        QStringList file;
        file<<filename;
        emit fm.BeginMerge(file,nameSystem.GetAName());
    }
}

void MainTask::FileStoped(){
    fp.ResetCounter();
    if(currentFileFilterIndex==(filters.count()-1)){
        if(pConsoleOut) *pConsoleOut<<"-----------------------------------"<<endl;
        if(pConsoleOut) *pConsoleOut<<"End."<<endl;
        fileCopyThread.exit();
        fileExtractThread.exit();
        fileMergeThread.exit();
        fileCopyThread.wait();
        fileExtractThread.wait();
        fileMergeThread.wait();
        files.clear();
        emit finished();
    }
    else{
        if(pConsoleOut) *pConsoleOut<<"-----------------------------------"<<endl<<endl;
        fileCopyThread.exit();
        fileCopyThread.wait();
        files.clear();
        fp.SetFileFilter(filters[++currentFileFilterIndex]);
        nameSystem.SetNameHint(&(filters[currentFileFilterIndex]));
        fe.SetFileDestinationDirectory("/dev/shm",QString::number(QCoreApplication::applicationPid())+QString::number(timer.elapsed()));
        fileCopyThread.start();
    }
}

// file is merged.
void MainTask::FitsMerged(QString filename,bool isOk){    
    fp.DecreaseCounter();
    totalFiles--;
    if(!isOk) fp.Stop();
    if(isOk){
        if(pConsoleOut) *pConsoleOut<<((filters[currentFileFilterIndex].IsForceDrifting&&totalFiles>=1)?totalFiles-1:totalFiles)<<": "<<filename<<" merged."<<endl;
    }else{
        if(pConsoleOut) *pConsoleOut<<((filters[currentFileFilterIndex].IsForceDrifting&&totalFiles>=1)?totalFiles-1:totalFiles)<<": "<<filename<<" merging fail."<<endl;
    }

    // all files handled
    if(/*(!isOk && fp.Counter()==0) ||*/ totalFiles < filters[currentFileFilterIndex].FileMergedCount){
        emit DeleteFiles();
        fp.Stop();
        fp.ResetCounter();
    }
}

// when fileprovider is done, the copied file count will fire.
void MainTask::FileCounted(long count){
    totalFiles=count;
    if(pConsoleOut) *pConsoleOut<<"Filter "<<currentFileFilterIndex+1<<": "<<count<<" files."<<endl;
}

bool compareQString(const QString &a, const QString &b){
    return a<b;
}
void MainTask::GetFilters(QString directory,QStringList filters, QList<FileFilter> &filterList){//QStringList &filterList){
    filterList.clear();
    QDir sourceDir(directory);
    sourceDir.setFilter(QDir::Files | QDir::NoSymLinks);
    sourceDir.setSorting(QDir::Name | QDir::IgnoreCase);

    QStringList fileList;
    if(filters.count()==0)
        fileList = sourceDir.entryList();
    else{
        QSet<QString> fileSet;
        //sourceDir.setNameFilters({filters[0]});
        //fileSet.unite(sourceDir.entryList().toSet());
        for(int i=0;i<filters.count();i++){
            sourceDir.setNameFilters({filters[i]});
            fileSet.unite(sourceDir.entryList().toSet());
        }
        fileList=fileSet.toList();
        /*qSort*/std::sort(fileList.begin(),fileList.end(),compareQString);
    }

    if(fileList.count()<=0) return;

    QString oldPrecedingString;
    long oldNumber=-1;

    int filterNumber=1;
    float timeLength=0.0, time;
    foreach (QString file_Name, fileList) {
        QFileInfo finfo(file_Name);
        QString filename=sourceDir.filePath((finfo.fileName()));
        finfo=QFileInfo(filename);
        int extensionIndex=filename.lastIndexOf(".");
        int sepratorIndex=filename.lastIndexOf("_");
        QString precedingString;
        QString strNumber;
        QString extensionName;
        long number;

        if(sepratorIndex>=0){
            precedingString=filename.left(sepratorIndex);
            strNumber=filename.mid(sepratorIndex+1,extensionIndex-sepratorIndex-1);
            number = strNumber.toLong();
            extensionName = filename.mid(extensionIndex);

            if(setting.MaxTimeLen>0 && filename.contains("tracking")){
                time=0;
                getTimeLen(finfo.absoluteFilePath().toStdString(),NULL,NULL,NULL,&time);
                timeLength += time;
            }

            if(oldPrecedingString!=precedingString || number != (oldNumber+1) || ((setting.MaxTimeLen>0 && filename.contains("tracking"))?(timeLength >= setting.MaxTimeLen*60.0):false)){ // should begin a new filter
                timeLength=time;
                FileFilter tempf;
                tempf.Filenames.append(finfo.absoluteFilePath());
                tempf.PrecedingName = precedingString;
                tempf.ExtensionName = extensionName;
                tempf.NumberLen = extensionIndex-sepratorIndex-1;
                tempf.MinNumber = number;
                tempf.FilterNumber = filterNumber++;
                tempf.Observe = filename.contains("tracking")?TRACKING:DRIFTING;
                if(tempf.Observe==TRACKING) tempf.IsForceDrifting=setting.IsForceDrifting;
                else tempf.IsForceDrifting=true;
                tempf.FileMergedCount= tempf.IsForceDrifting?setting.FileCountToMerge:1;
                tempf.IsLowFreq=setting.BeginChannelFreq<1024 && setting.EndChannelFreq<=1024;
                filterList.append(tempf);
            }else{
                filterList.last().Filenames.append(finfo.absoluteFilePath());
            }
            oldPrecedingString=precedingString;
            oldNumber = number;
        }
    }
}

// to do work.
void MainTask::run() {
    //show filters
    if(pConsoleOut) *pConsoleOut<<"Parameters:"<<endl;
    if(pConsoleOut) *pConsoleOut<<"      Source Directory:\t"<<setting.SourceDir<<endl;
    if(pConsoleOut) *pConsoleOut<<" Destination Directory:\t"<<setting.DestDir<<endl;
    if(pConsoleOut) *pConsoleOut<<"          Polarization:\t"<<setting.PolNo<<endl;
    if(pConsoleOut) *pConsoleOut<<"       Begin Frequency:\t"<<setting.BeginChannelFreq<<" MHz"<<endl;
    if(pConsoleOut) *pConsoleOut<<"         End Frequency:\t"<<setting.EndChannelFreq<<" MHz"<<endl;
    if(pConsoleOut) *pConsoleOut<<"           Merge Count:\t"<<setting.FileCountToMerge<<endl;
    if(pConsoleOut) *pConsoleOut<<"   Merge File Max Time:\t"<<(setting.MaxTimeLen<0?"infinite":QString::number(setting.MaxTimeLen))<<" minutes"<<endl;
    if(pConsoleOut) *pConsoleOut<<"    Is Handle Drifting:\t"<<(setting.IsHandleDrifting?"TRUE":"FALSE")<<endl;
    if(pConsoleOut) *pConsoleOut<<"    Is Handle Tracking:\t"<<(setting.IsHandleTracking?"TRUE":"FALSE")<<endl;
    if(pConsoleOut) *pConsoleOut<<"   Is Drifted by Force:\t"<<(setting.IsForceDrifting?"TRUE":"FALSE")<<endl;
    if(pConsoleOut) {
        *pConsoleOut<<"      File Name Filter:\t";
        foreach (QString item, setting.FileNameFilters) {
            *pConsoleOut<<item<<" ";
        }
        *pConsoleOut<<endl;
    }

    QStringList nameFilters(setting.FileNameFilters);
    if(pConsoleOut) *pConsoleOut<<endl<<"Genrates Filters... ";
    if(pConsoleOut) pConsoleOut->flush();
    if(nameFilters.count()==0){
        if(setting.IsHandleDrifting && setting.IsHandleTracking){
            nameFilters<<"*.fits";
        }
        else if(setting.IsHandleDrifting && !setting.IsHandleTracking){
            nameFilters<<"*drifting*.fits";
        }
        else if(!setting.IsHandleDrifting && setting.IsHandleTracking){
            nameFilters<<"*tracking*.fits";
        }
    }
    GetFilters(setting.SourceDir,nameFilters,filters);

    if(filters.count()==0){
        if(pConsoleOut) *pConsoleOut<<"No file to handle."<<endl;
        emit finished();
        return;
    }
    if(pConsoleOut) *pConsoleOut<<"Done."<<endl;

    if(pConsoleOut) *pConsoleOut<<endl<<"Group Number, Fits File Count in Group and the First Fits File Name:"<<endl;
    for(int i=0;i<filters.count();i++){
        if(pConsoleOut) *pConsoleOut<<"  "<<filters[i].FilterNumber<<"\t"<<filters[i].Filenames.count()<<"\t"<<filters[i].Filenames.first()<<endl;
    }
    cout<<endl;
    if(setting.OnlyFilt){
        emit finished();
        return;
    }

    if(setting.SpecialFilterNo>filters.length()){
        if(pConsoleOut) *pConsoleOut<<"The filter number is not valid."<<endl;
        emit finished();
        return;
    }

    QDir dir(setting.DestDir);
    if(!dir.exists()) {
        if(pConsoleOut) *pConsoleOut<<" directory "<<setting.DestDir<<" not exists"<<endl;
        emit finished();
        return;
    }

    // decide where to save the list file.
    QFileInfo fileInfo(filters.first().Filenames.first());
    QString destinationDir = fileInfo.fileName();
    destinationDir=destinationDir.left(destinationDir.indexOf("_"));
    //if(!dir.cd(destinationDir)) {
    //    dir.mkdir(destinationDir);
    //    dir.cd(destinationDir);
    //}
    QString fileInfoListFilename=dir.absolutePath()+QDir::separator()+destinationDir+".list";

    std::ofstream fs(fileInfoListFilename.toStdString(),std::ios::app);
    fs<<std::endl<<"---------------------"<<std::endl;
    fs<<"Time:\t"<<QDateTime::currentDateTime().toString().toStdString()<<std::endl;
    fs<<"Parameters:"<<std::endl;
    fs<<"      Source Directory:\t"<<setting.SourceDir.toStdString()<<std::endl;
    fs<<" Destination Directory:\t"<<setting.DestDir.toStdString()<<std::endl;
    fs<<"          Polarization:\t"<<setting.PolNo<<std::endl;
    fs<<"       Begin Frequency:\t"<<setting.BeginChannelFreq<<" MHz"<<std::endl;
    fs<<"         End Frequency:\t"<<setting.EndChannelFreq<<" MHz"<<std::endl;
    fs<<"           Merge Count:\t"<<setting.FileCountToMerge<<std::endl;
    fs<<"   Merge File Max Time:\t"<<setting.MaxTimeLen<<" minutes"<<std::endl;
    fs<<"    Is Handle Drifting:\t"<<(setting.IsHandleDrifting?"TRUE":"FALSE")<<std::endl;
    fs<<"    Is Handle Tracking:\t"<<(setting.IsHandleTracking?"TRUE":"FALSE")<<std::endl;
    fs<<"   Is Drifted by Force:\t"<<(setting.IsForceDrifting?"TRUE":"FALSE")<<std::endl;
    fs<<"      File Name Filter:\t";
    foreach (QString item, setting.FileNameFilters) {
        fs<<item.toStdString()<<" ";
    }
    fs<<std::endl;

    fs<<"Group Number, Fits File Count in Group and the First Fits File Name:"<<std::endl;
    for(int i=0;i<filters.count();i++){
        fs<<"  "<<filters[i].FilterNumber<<"\t"<<filters[i].Filenames.count()<<"\t"<<filters[i].Filenames.first().toStdString()<<std::endl;
    }
    fs<<std::endl<<"====================="<<std::endl;
    fs<<std::endl;
    fs.close();

    currentFileFilterIndex=0;

    connect(this,&MainTask::DeleteFiles,&fe,&FileExtractor::DeleteFiles,Qt::ConnectionType::QueuedConnection);
    connect(this,&MainTask::DeleteFiles,&fp,&FileProvider::DeleteFiles,Qt::ConnectionType::QueuedConnection);

    //files merging
    fm.SetOutputDirectory(setting.DestDir);
    connect(&fm,&FileMerger::Merged,this,&MainTask::FitsMerged,Qt::ConnectionType::QueuedConnection);
    fm.moveToThread(&fileMergeThread);
    fileMergeThread.start();

    //files extracting    
    fe.SetPolarNo(setting.PolNo);
    fe.SetFrequencyChannelRange(setting.BeginChannelFreq,setting.EndChannelFreq,false); //setting.BeginChannelFreq>=1024);
    fe.moveToThread(&fileExtractThread);
    connect(&fp,&FileProvider::FileReady,&fe,&FileExtractor::FitsFileExtract, Qt::ConnectionType::QueuedConnection);
    connect(&fe,&FileExtractor::Extracted,this,&MainTask::FitsExtracted,Qt::ConnectionType::QueuedConnection);
    fileExtractThread.start();

    //files copying
    if(setting.SpecialFilterNo>0){
        //move to the last
        if(pConsoleOut) *pConsoleOut<<"Only handle the file in filter "<<setting.SpecialFilterNo<<"."<<endl;
        filters.move(setting.SpecialFilterNo-1,filters.length()-1);
        currentFileFilterIndex=filters.length()-1;
    }
    fp.SetFileFilter(filters[currentFileFilterIndex]);
    fp.SetDestinationDirectory(setting.IsCopyFileToMem?"/dev/shm":"");
    fp.moveToThread(&fileCopyThread);
    connect(&fileCopyThread,&QThread::started,&fp,&FileProvider::ReadAllFile,Qt::ConnectionType::QueuedConnection);
    connect(&fp,&FileProvider::FilesCounted, this, &MainTask::FileCounted, Qt::ConnectionType::QueuedConnection);
    connect(&fp,&FileProvider::Stoped,this,&MainTask::FileStoped,Qt::ConnectionType::QueuedConnection);
    nameSystem.SetNameHint(&(filters[currentFileFilterIndex]));
    if(!timer.isValid()) timer.start();
    fe.SetFileDestinationDirectory("/dev/shm",QString::number(QCoreApplication::applicationPid())+QString::number(timer.elapsed()));
    fileCopyThread.start();
}
