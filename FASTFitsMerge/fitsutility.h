#ifndef FITSUTILITY_H
#define FITSUTILITY_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <ctime>
#include <cstring>
#include <fitsio.h>

using namespace std;

// some information for FAST fits file
typedef struct {
    string filename; //fits file name
    string telescop; // telescop name
    int beamID; // id of beam
    long long nSubIntOffs; // subint offset, for continous search mode files
    float ver; //version. e.g. 3.4
    int hdutype; //ASCII_TBL, BINARY_TBL
    int bitpix;  //always 8
    int nAxis;   //always 2
    long long colsSize; //size of a row in table
    long long nRows; // row count in table. that is, the subint count
    int nPols; // how many polarization
    int nChannels; // how many channels
    int nSamples; // samples per channel in a subint

    long long stt_imjd;
    long long stt_smjd;
    double stt_offs;
    double subIntPeriod; // Length of subintegration, second
    double firstSubIntTimeOffset; // the first subint's time offset, second

    long long leadingCol13Size; // in a row, the leading bytes before column 13 DAT_FREQ
    long col13ElementWidth;  //the element width (unit: byte)
    long long leadingCol14Size; // in a row, the leading bytes before column 14 DAT_WTS
    long col14ElementWidth;  //the element width (unit: byte)
    long long leadingCol15Size; // in a row, the leading bytes before column 15 DAT_OFFS
    long col15ElementWidth;  //the element width (unit: byte)
    long long leadingCol16Size; // in a row, the leading bytes before column 16 DAT_SCL
    long col16ElementWidth;  //the element width (unit: byte)
    long long leadingCol17Size; // in a row, the leading bytes before column 17 DATA
    long long extensionHduDataOffset; //the data offset of the extenstion hdu. in byte.
} FASTFitsDataInfo;

// show error informatin on console
void printerror(int status);

// show fits headers information
void readheader (const char *filename);

// read fits info from fitsfile
bool readFASTFitsInfo(fitsfile *fptr,FASTFitsDataInfo &info);

// show information in console.
void printFASTFitsInfo(FASTFitsDataInfo &info);

// set the OFFS_SUB of second fits file identy as reference fits file.
// note: before calling this function, be sure to close the second fits file
// return fasle when error occured.
bool normalizeOFFS_SUB(const FASTFitsDataInfo& refFitsInfo, FASTFitsDataInfo& info);

// check wheather two FAST fits can merge. Attension: bitpix
bool canMerge(FASTFitsDataInfo &info1,FASTFitsDataInfo &info2);

// extract data to a new fits file which name is outFitsFilename.
// info: source fits file information
// the output fits will contain channel between channelNoFrom to channelNoTo and the polar is polNo.
// channelFromNo>=1, channelToNo>1, polNo>=1, channelNoFrom<=channelNoTo
bool extractFits(FASTFitsDataInfo &info, int channelNoFrom, int channelNoTo, int polNo, string outFitsFilename, float centerFreq=0.0);

// extract data to a new fits file which name is outFitsFilename.
// info: source fits file information
// the output fits will contain channel between channelNoFrom to channelNoTo and the polar is polNo.
// channelFromNo>=1, channelToNo>1, polNo>=1, channelNoFrom<=channelNoTo
bool extractFits(string filename, int channelNoFrom, int channelNoTo, int polNo, string outFitsFilename);

// extract data to a new fits file which name is outFitsFilename.
// info: source fits file information
// the output fits will contain channels which frequency is between channelFreqFrom to channelFreqTo and the polar is polNo.
bool extractFits(string filename, float channelFreqFrom, float channelFreqTo, int polNo, string outFitsFilename, bool isReverseChannel);

// append the second fits extension data to the first fits, and output to outFilename file.
bool mergeFitsFile(string inFilenames[], int nInFiles, string outFliename);

// read the time reletive parameter and store to row, samplesPerRow, timePerSample, allTimeLen.
// Unit: second.
bool getTimeLen(string filename, long *row, long *samplesPerRow, float *timePerSample, float *allTimeLen);

bool isDataIdent(string filename1,string filename2);

void dataView(string filename);

#endif // FITSUTILITY_H
