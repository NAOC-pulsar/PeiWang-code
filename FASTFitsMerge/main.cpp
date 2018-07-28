#include <QCoreApplication>
#include <QSharedPointer>
#include <QCommandLineParser>
#include <QTextStream>
#include <QTimer>
#include <QDir>
#include <QFile>

#include "maintask.h"

QDebug *pConsoleDebug=nullptr;
QTextStream *pConsoleOut=nullptr;

int main(int argc, char *argv[]){
    QCoreApplication app(argc, argv);
    QCoreApplication::setApplicationName("FAST Fits Extract and Merge");
    QCoreApplication::setApplicationVersion("0.01");

    pConsoleOut=new QTextStream(stdout);

    QCommandLineParser parser;

    parser.setApplicationDescription("FAST Fits Extract and Merge program handle the initial fits files and produce new fits files.");
    parser.addHelpOption();
    parser.addVersionOption();

    parser.addPositionalArgument("source_dir", QCoreApplication::translate("main", "Source directory that contains initial fits files."));
    parser.addPositionalArgument("dest_dir", QCoreApplication::translate("main", "Destination directory."));

    // A boolean option with multiple names (-d, --drifting)
    QCommandLineOption driftingOption(QStringList() << "d" << "drifting",
                                      QCoreApplication::translate("main", "Extract and merge drifting files."));
    parser.addOption(driftingOption);

    // A boolean option with multiple names (-t, --tracking)
    QCommandLineOption trackingOption(QStringList() << "t" << "tracking",
                                      QCoreApplication::translate("main", "Extract and merge all tracking files."));
    parser.addOption(trackingOption);

    // An option with a value
    QCommandLineOption fileNameFilterOption(QStringList() << "f" << "filename-filter",
                                                QCoreApplication::translate("main", "Only handle file with name <filenamefilter>. The default value is *.fits ."),
                                                QCoreApplication::translate("main", "filenamefilter"));
    //fileNameFilterOption.setDefaultValue("");
    parser.addOption(fileNameFilterOption);

    // An option with a value
    QCommandLineOption polarizationNumberOption(QStringList() << "p" << "polar-no",
                                                QCoreApplication::translate("main", "Only extract data that contains polorization <number>. The default value is 1."),
                                                QCoreApplication::translate("main", "number"));
    polarizationNumberOption.setDefaultValue("1");
    parser.addOption(polarizationNumberOption);

//    // An option with a value
//    QCommandLineOption beginChannelNoOption(QStringList() << "B" << "end-ch-no",
//                                            QCoreApplication::translate("main", "Only extract data that frequenct channel >= <number>. The default value is 1161."),
//                                            QCoreApplication::translate("main", "number"));
//    beginChannelNoOption.setDefaultValue("1161");
//    parser.addOption(beginChannelNoOption);

//    // An option with a value
//    QCommandLineOption endChannelNoOption(QStringList() << "E" << "begin-ch-no",
//                                          QCoreApplication::translate("main", "Only extract data that frequency channel <= <number>. The default value is 3208."),
//                                          QCoreApplication::translate("main", "number"));
//    endChannelNoOption.setDefaultValue("3208");
//    parser.addOption(endChannelNoOption);

    // An option with a value
    QCommandLineOption beginChannelFreqOption(QStringList() << "b" << "begin-ch-freq",
                                            QCoreApplication::translate("main", "Only extract data that channel frequence >= <number>. The default value is 290.0."),
                                            QCoreApplication::translate("main", "number"));
    beginChannelFreqOption.setDefaultValue("290.0");
    parser.addOption(beginChannelFreqOption);

    // An option with a value
    QCommandLineOption endChannelFreqOption(QStringList() << "e" << "end-ch-freq",
                                          QCoreApplication::translate("main", "Only extract data that channel frequence <= <number>. The default value is 802.0."),
                                          QCoreApplication::translate("main", "number"));
    endChannelFreqOption.setDefaultValue("802.0");
    parser.addOption(endChannelFreqOption);

    // An option with a value
    QCommandLineOption fileCountOption(QStringList() << "c" << "files-count",
                                       QCoreApplication::translate("main", "Every <number> files will be squencely merged to a file. The default value is 2."),
                                       QCoreApplication::translate("main", "number"));
    fileCountOption.setDefaultValue("2");
    parser.addOption(fileCountOption);

    // An option with a value
    QCommandLineOption maxTimeLenOption(QStringList() << "l" << "max-time-length",
                                       QCoreApplication::translate("main", "The maximum time length of a single merged fits file by minutes. The default value is -1 for unlimited time length."),
                                       QCoreApplication::translate("main", "number"));
    maxTimeLenOption.setDefaultValue("-1");
    parser.addOption(maxTimeLenOption);

    // A boolean option with multiple names (-f, --force-drifting)
    QCommandLineOption forceDriftingOption(QStringList() << "F" << "force-drifting",
                                      QCoreApplication::translate("main", "Treat all tracking files as drifting by force."));
    parser.addOption(forceDriftingOption);

    // A boolean option with multiple names (-f, --force-drifting)
    QCommandLineOption memoryOption(QStringList() << "m" << "memory-copyed",
                                      QCoreApplication::translate("main", "Copy the source fits file to memory before hanled."));
    parser.addOption(memoryOption);

    // A boolean option with multiple names (-f, --force-drifting)
    QCommandLineOption onlyFilterOption(QStringList() << "only-filter",
                                      QCoreApplication::translate("main", "Only produce file filters, not extract and merge."));
    parser.addOption(onlyFilterOption);

    // An option with a value
    QCommandLineOption specialFilterNoOption(QStringList() << "filter-number",
                                       QCoreApplication::translate("main", "Only extract and merge the files in filter <number>. "),
                                       QCoreApplication::translate("main", "number"));
    specialFilterNoOption.setDefaultValue("-1");
    parser.addOption(specialFilterNoOption);

    // A boolean option with multiple names (-f, --force-drifting)
    QCommandLineOption debugOption(QStringList() << "debug",
                                      QCoreApplication::translate("main", "Write debug info to log."));
    parser.addOption(debugOption);

    // Process the actual command line arguments given by the user
    parser.process(app);

    const QStringList args = parser.positionalArguments();
    // source is args.at(0), destination is args.at(1)

    Settings settings;
    try{
        if(args.length()<2){
            if(pConsoleOut) *pConsoleOut<<"The source and destination directory must not be empty.";
            return 0;
        }
        settings.SourceDir=args[0];
        settings.DestDir=args[1];
        if(settings.SourceDir.isEmpty() || settings.DestDir.isEmpty()){
            if(pConsoleOut) *pConsoleOut<<"The source and destination directory must not be null.";
            return 0;
        }
        QDir sDir(settings.SourceDir);
        if(!sDir.exists()) {
            if(pConsoleOut) *pConsoleOut<<"Cannot find the source directory.";
            return 0;
        }
        QDir dDir(settings.DestDir);
        if(!dDir.exists()) {
            if(pConsoleOut) *pConsoleOut<<"Cannot find the destination directory.";
            return 0;
        }
        settings.PolNo=parser.value(polarizationNumberOption).toInt();
        settings.BeginChannelFreq=parser.value(beginChannelFreqOption).toFloat();
        settings.EndChannelFreq=parser.value(endChannelFreqOption).toFloat();
        settings.IsForceDrifting=parser.isSet(forceDriftingOption);
        settings.FileCountToMerge=parser.value(fileCountOption).toInt();
        settings.IsHandleDrifting=parser.isSet(driftingOption);
        settings.IsHandleTracking=parser.isSet(trackingOption);
        settings.IsCopyFileToMem=parser.isSet(memoryOption);
        settings.MaxTimeLen=parser.value(maxTimeLenOption).toFloat();
        settings.OnlyFilt=parser.isSet(onlyFilterOption);
        settings.SpecialFilterNo=parser.value(specialFilterNoOption).toInt();
        settings.FileNameFilters=parser.values(fileNameFilterOption);
    }
    catch(...){
        if(pConsoleOut) *pConsoleOut<<"Some arguments are wrong.";
        return 0;
    }

    QFile fp;
    if(parser.isSet(debugOption)){
        fp.setFileName("log");
        fp.open(QIODevice::WriteOnly|QIODevice::Append);
        pConsoleDebug=new QDebug(&fp);
    }

    MainTask task(settings,&app);
    QObject::connect(&task, &MainTask::finished, &app, &QCoreApplication::quit);
    QTimer::singleShot(0, &task, &MainTask::run);

    return app.exec();

    if(fp.isOpen()) fp.close();
    if(pConsoleDebug) delete pConsoleDebug;
    if(pConsoleOut) delete pConsoleOut;
}
