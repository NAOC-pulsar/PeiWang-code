#include "filenamesystem.h"
#include <QFileInfo>
#include <QDir>

FileNameSystem::FileNameSystem(QString allinoneName)
{
    this->allinoneName=allinoneName;
}

void FileNameSystem::SetNameHint(FileFilter *filter){
    //approach: filename append "merge"
    //int index3 = hint.lastIndexOf(".");
    //allinoneName = hint.left(index3)+"_merge"+hint.mid(index3);
    // another approach:
    if(filter == nullptr || filter->Filenames.count()==0){
        allinoneName = "unkonwnname";
        return;
    }

    QString number;
    number.setNum(filter->FilterNumber,16);
    QFileInfo finfo(filter->Filenames.first());
    QString oldFilename=finfo.fileName();
    int index0 = oldFilename.indexOf("_");
    int index1 = oldFilename.lastIndexOf("_");
    int index2 = oldFilename.lastIndexOf(".");

    allinoneName = oldFilename.left(index0+1)
            + oldFilename.mid(index1+1,index2-index1-1).leftJustified(4,'0')
            + /*QString::number(filter->FilterNumber)*/ number + (filter->IsLowFreq?"L":"H") + filter->ExtensionName;
}

QString FileNameSystem::GetAName(){
    return allinoneName;
}

QString FileNameSystem::GetAName(QStringList *files, FileFilter *filter){
    if(files==nullptr || files->count()==0 || filter==nullptr) return "unkonwnname";

    QString number;
    number.setNum(filter->FilterNumber,16);
    QFileInfo finfo(files->at(0));
    QString oldFilename=finfo.fileName();
    int index0 = oldFilename.indexOf("_");
    int index1 = oldFilename.lastIndexOf("_");
    int index2 = oldFilename.lastIndexOf(".");

    return oldFilename.left(index0+1)
            + oldFilename.mid(index1+1,index2-index1-1).leftJustified(4,'0')
            + /*QString::number(filter->FilterNumber)*/ number + (filter->IsLowFreq?"L":"H") + filter->ExtensionName;
}
