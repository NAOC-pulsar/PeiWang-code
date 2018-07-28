#include "fitsutility.h"
#include <iomanip>

// show error informatin on console
void printerror(int status){
    if (status)
    {
        fits_report_error(stderr, status); /* print error report */
        //exit( status );    /* terminate the program, returning error status */
    }
}

// show fits headers information
void readheader (const char *filename){
    fitsfile *fptr;       // pointer to the FITS file, defined in fitsio.h
    int status=0, nkeys, keypos, hdutype, ii, jj;
    char card[FLEN_CARD];   /* standard string lengths defined in fitsioc.h */

    if ( fits_open_file(&fptr, filename, READONLY, &status) )
        printerror( status );

    // attempt to move to next HDU, until we get an EOF error
    for (ii = 1; !(fits_movabs_hdu(fptr, ii, &hdutype, &status) ); ii++)
    {
        // get no. of keywords */
        if (fits_get_hdrpos(fptr, &nkeys, &keypos, &status) )
            printerror( status );

        printf("Header listing for HDU #%d:\n", ii);
        for (jj = 1; jj <= nkeys; jj++)  {
            if ( fits_read_record(fptr, jj, card, &status) )
                printerror( status );

            printf("%s\n", card); /* print the keyword card */
        }
        printf("END\n\n");  /* terminate listing with END */
    }

    if (status == END_OF_FILE)   /* status values are defined in fitsioc.h */
        status = 0;              /* got the expected EOF error; reset = 0  */
    else
        printerror( status );     /* got an unexpected error                */

//    fits_movabs_hdu(fptr, 2, &hdutype, &status) ;
//    double data[256],floatnull;
//    int anynull;
//    fits_read_col(fptr, TDOUBLE,1, 1, 1, sizeof(data)/sizeof(data[0]), &floatnull, data,
//                  &anynull, &status);
//    cout<<"col 1: "<<endl;
//    for(int i=0;i<sizeof(data)/sizeof(data[0]);i++) cout<<i+1<<":"<<data[i]<<endl;

//    fits_read_col(fptr, TDOUBLE, 2, 1, 1, sizeof(data)/sizeof(data[0]), &floatnull, data,
//                  &anynull, &status);
//    cout<<"col 2:"<<endl;
//    for(int i=0;i<sizeof(data)/sizeof(data[0]);i++) cout<<i+1<<":"<<data[i]<<endl;

    if ( fits_close_file(fptr, &status) )
        printerror( status );

    return;
}

// read fits info from fitsfile
bool readFASTFitsInfo(fitsfile *fptr,FASTFitsDataInfo &info){
    if(fptr==NULL) return false;
    int status=0;
    int hudtype;
    char buffer[80];
    const int cutCol=17; // the colomun number need to cut
    int hdutype;
    //move to primary hdu
    if(fits_movabs_hdu(fptr,1,&hdutype,&status)) return false;
    //hdu version
    if(fits_read_key(fptr,TFLOAT,"HDRVER",&info.ver,NULL,&status)) return false;
    //telescop name
    if(fits_read_key(fptr,TSTRING,"TELESCOP",buffer,NULL,&status)) return false;
    info.telescop=string(buffer);
    if(fits_read_key(fptr,TSTRING,"IBEAM",buffer,NULL,&status)) { info.beamID=0; status=0;}
    else info.beamID=stoi(buffer);

    //read the start time information
    if(fits_read_key(fptr,TLONGLONG,"STT_IMJD",&info.stt_imjd,NULL,&status)) { info.stt_imjd=0; status=0;}
    if(fits_read_key(fptr,TLONGLONG,"STT_SMJD",&info.stt_smjd,NULL,&status)) { info.stt_imjd=0; status=0;}
    if(fits_read_key(fptr,TDOUBLE,"STT_OFFS",&info.stt_offs,NULL,&status)) { info.stt_imjd=0; status=0;}

    // move to extension and read the hdu type
    if(fits_movabs_hdu(fptr,2,&hdutype,&status)) return false;
    info.hdutype=hdutype;
    // read bitpix
    if(fits_read_key(fptr,TINT,"BITPIX",&info.bitpix,NULL,&status)) return false;
    //read
    if(fits_read_key(fptr,TINT,"NAXIS",&info.nAxis,NULL,&status)) return false;
    //read
    if(fits_read_key(fptr,TLONGLONG,"NAXIS1",&info.colsSize,NULL,&status)) return false;
    //read
    if(fits_read_key(fptr,TLONGLONG,"NAXIS2",&info.nRows,NULL,&status)) return false;
    //read
    if(fits_read_key(fptr,TLONGLONG,"NSUBOFFS",&info.nSubIntOffs,NULL,&status)) return false;

    //read first row's start time
    if(fits_read_col(fptr,TDOUBLE,1,1,1,1,NULL,&info.subIntPeriod,NULL,&status)) {
        info.subIntPeriod=-1;
        status=0;
    }

    //read the first row, second column
    if(fits_read_col(fptr,TDOUBLE,2,1,1,1,NULL,&info.firstSubIntTimeOffset,NULL,&status)) {
        info.firstSubIntTimeOffset=0;
        status=0;
    }
    //info.firstSubIntTimeOffset+=info.stt_imjd*86400+info.stt_smjd+info.stt_offs;

    //read the leading bytes count for some colomns
    long repeat, width;
    long leading = 0;
    for(int col=1; col<=17; col++){
        fits_get_coltype(fptr, col, NULL, &repeat, &width, &status);
        switch (col) {
        case 13:
            info.leadingCol13Size=leading;
            info.col13ElementWidth=width;
            break;
        case 14:
            info.leadingCol14Size=leading;
            info.col14ElementWidth=width;
            break;
        case 15:
            info.leadingCol15Size=leading;
            info.col15ElementWidth=width;
            break;
        case 16:
            info.leadingCol16Size=leading;
            info.col16ElementWidth=width;
            break;
        case 17:
            info.leadingCol17Size=leading;
            break;
        default:
            break;
        }
        leading += repeat*width;
    }

    //read the tdim for colomn 17
    int naxis=0;
    long naxes[10];
    if(fits_read_tdim(fptr,cutCol,10,&naxis,naxes,&status)) return false;
    if(naxis<4) return false;
    info.nChannels=naxes[1];
    info.nPols=naxes[2];
    info.nSamples=naxes[3];

    int nKeys1,nKeys2;
    if(fits_movabs_hdu(fptr,1,&hdutype,&status)) return false;
    if(fits_get_hdrpos(fptr,&nKeys1,&hudtype,&status)) return false;
    if(fits_movabs_hdu(fptr,2,&hdutype,&status)) return false;
    if(fits_get_hdrpos(fptr,&nKeys2,&hudtype,&status)) return false;
    info.extensionHduDataOffset=(ceil((nKeys1*1.0)/36.0)+ceil((nKeys2*1.0)/36.0))*2880;

    //printFASTFitsInfo(info);

    return true;
}

// show information in console.
void printFASTFitsInfo(FASTFitsDataInfo &info){
    cout<<"FAST fits info:"<<endl;
    cout<<"File name: "<<info.filename<<endl;
    cout<<" Telescop: "<<info.telescop<<endl;
    cout<<" Version: "<<info.ver<<endl;
    cout<<" Hdu type: "<<info.hdutype<<endl;
    cout<<" Bitpix: "<<info.bitpix<<endl;
    cout<<" nAxis: "<<info.nAxis<<endl;
    cout<<" ColsSize: "<<info.colsSize<<endl;
    cout<<" nRows: "<<info.nRows<<endl;
    cout<<" nPols: "<<info.nPols<<endl;
    cout<<" nChannels: "<<info.nChannels<<endl;
    cout<<" nSamples: "<<info.nSamples<<endl;
    cout<<" nSubOffs: "<<info.nSubIntOffs<<endl;
    cout<<setprecision(16);
    cout<<" subint start time(s): "<<info.stt_imjd*86400+info.stt_smjd+info.stt_offs<<endl;
    cout<<" first subint time offset referent to subint start time(s): "<<info.firstSubIntTimeOffset<<endl;
    cout<<" subint time length(s): "<<info.subIntPeriod<<endl;
    cout<<" leadingColsSize: "<<info.leadingCol17Size<<endl;
}

// check wheather two FAST fits can merge. Attension: bitpix
bool canMerge(FASTFitsDataInfo &info1,FASTFitsDataInfo &info2){
    if(info1.telescop!=info2.telescop) {
        cout<<"Telescop is inconsistent."<<endl;
        return false;
    }
    if(info1.beamID!=info2.beamID) {
        cout<<"The beam id is inconsistent."<<endl;
        return false;
    }
    if(info1.ver!=info2.ver) return false;
    if(info1.hdutype!=info2.hdutype || (info1.hdutype!=BINARY_TBL && info1.hdutype!=ASCII_TBL)) return false;
    if(info1.bitpix!=info2.bitpix) return false;
    if(info1.colsSize!=info2.colsSize) return false;
    if(info1.nPols!=info2.nPols) return false;
    if(info1.nChannels!=info2.nChannels) return false;
    if(info1.nSamples!=info2.nSamples) return false;
    //if((info1.nSubIntOffs+info1.nRows)!=info2.nSubIntOffs) return false;
    if((((info2.stt_imjd*86400+info2.stt_smjd+info2.stt_offs+info2.firstSubIntTimeOffset)-(info1.stt_imjd*86400+info1.stt_smjd+info1.stt_offs+info1.firstSubIntTimeOffset))
        -info1.subIntPeriod*info1.nRows) > 1e-5) {
        cout<<"the time is discontinous for two fits file."<<endl;
        return false;
    }

    //ATTENSION!
    if(info1.bitpix/8*8 != info1.bitpix) return false;

    return true;
}

// extract data to a new fits file which name is outFitsFilename.
// info: source fits file information
// the output fits will contain channel between channelNoFrom to channelNoTo and the polar is polNo.
// channelFromNo>=1, channelToNo>1, polNo>=1, channelNoFrom<=channelNoTo
bool extractFits(FASTFitsDataInfo &info, int channelNoFrom, int channelNoTo, int polNo, string outFitsFilename, float centerFreq){
    //TODO: check the channel number and the actual range of channel number.
    if(channelNoFrom>channelNoTo || polNo >info.nPols) return false;
    //ATTENSION!
    if(info.bitpix/8*8 != info.bitpix) {
        cout<<"Extract failure. The BITPIX should be multiple of 8!"<<endl;
        return false;
    }

    long sizePerChannelOfCol17 = info.bitpix/8;
    long sizePerPolOfCol17 = info.nChannels * sizePerChannelOfCol17;
    long sizePerSampleOfCol17 = info.nPols*sizePerPolOfCol17;

    //clock_t start, end;
    //start = clock();

    //open input and output file
    ifstream source(info.filename, ios::binary);
    if(!source){
        cout<<"Fail to open "<<info.filename<<"."<<endl;
        return false;
    }
    ofstream dest(outFitsFilename, ios::binary|ios::trunc);
    if(!dest){
        cout<<"Fail to create output fits file "<<outFitsFilename<<"."<<endl;
        source.close();
        return false;
    }

    //copy primary hdu and extension header
    size_t size=info.extensionHduDataOffset;// allocate memory for buffer
    char* buffer = new char[size];
    source.seekg(0);
    source.read(buffer, size);
    dest.write(buffer, size);

    // clean up
    delete[] buffer;
    source.close();
    dest.close();

    fitsfile *infp,*outfp=NULL;
    int status=0;
    int hdutype;
    //open fits file
    if(fits_open_file(&infp,info.filename.c_str(),READONLY,&status)) {printerror(status); return false;}
    if(fits_movabs_hdu(infp,2,&hdutype,&status)) {printerror(status); status=0; fits_close_file(infp,&status); return false;}
    if(fits_open_file(&outfp,outFitsFilename.c_str(),READWRITE,&status)) {printerror(status); return false;}
    if(fits_movabs_hdu(outfp,2,&hdutype,&status)) printerror(status);

    if(centerFreq<=0.0){ //calculate center frequency
        long repeat;
        fits_get_coltype(infp, 13, NULL, &repeat, NULL, &status);
        float *freq = new float[repeat];
        if(fits_read_col(infp,TFLOAT,13,1,1,repeat,NULL,freq,NULL,&status)){
            cout<<"failure to read frequency in "<<info.filename<<endl;
            delete[] freq;
            return false;
        }
        centerFreq=(freq[channelNoFrom-1]+freq[channelNoTo-1])/2.0;
        delete[] freq;
    }

    char comment[80]="changed",tempChars[80], value[80];
    long long newNumber;
    float channelBandWidth=0.0;
    if(fits_read_key(infp,TFLOAT,"CHAN_BW",&channelBandWidth,comment,&status)) {printerror(status); return false;}

    // update NAXIS1 NAXIS2
    newNumber = info.colsSize
            -(channelNoFrom-1 + info.nChannels-channelNoTo)*info.col13ElementWidth //col13
            -(channelNoFrom-1 + info.nChannels-channelNoTo)*info.col14ElementWidth  //col14
            -((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo))*info.col15ElementWidth   //col15
            -((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo))*info.col16ElementWidth   //col16
            -info.nSamples*( (info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo) )*sizePerChannelOfCol17;  //col17

    long long tempLL;
    //if(fits_read_key(fp1,TLONGLONG,"NAXIS2",&tempLL,comment,&status)) {printerror(status); return false;}
    //tempLL=0;
    //if(fits_update_key(outfp,TLONGLONG,"NAXIS2",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_read_key(infp,TLONGLONG,"NAXIS1",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"NAXIS1",&newNumber,comment,&status)) {printerror(status); return false;}

    stringstream sstr;
    string newNumberStr;
    //TODO update col 13  TFORM13
    newNumber = (info.leadingCol14Size-info.leadingCol13Size)/info.col13ElementWidth-(channelNoFrom-1 + info.nChannels-channelNoTo);
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM13",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM13",value,comment,&status)) {printerror(status); return false;}

    //TODO update col 14
    newNumber = (info.leadingCol15Size-info.leadingCol14Size)/info.col14ElementWidth-(channelNoFrom-1 + info.nChannels-channelNoTo);
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM14",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM14",value,comment,&status)) {printerror(status); return false;}

    //TODO update col 15
    newNumber = (info.leadingCol16Size-info.leadingCol15Size)/info.col15ElementWidth-((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo));
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM15",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM15",value,comment,&status)) {printerror(status); return false;}

    //TODO update col 16
    newNumber = (info.leadingCol17Size-info.leadingCol16Size)/info.col16ElementWidth-((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo));
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM16",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM16",value,comment,&status)) {printerror(status); return false;}

    //TODO update TFORM17
    newNumber = (info.colsSize-info.leadingCol17Size)/sizePerChannelOfCol17-info.nSamples*( (info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo) );
    sstr.str("");
    sstr << newNumber<<"B";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM17",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM17",value,comment,&status)) {printerror(status); return false;}

    //update TDIM17
    int naxis=0;
    long naxes[10];
    if(fits_read_tdim(infp,17,10,&naxis,naxes,&status)) {printerror(status); return false;}
    naxes[1]=channelNoTo-channelNoFrom+1;
    naxes[2]=1;
    //if(fits_write_tdim(outfp,17,naxis,naxes,&status)) printerror(status); //add keyword instead of update
    if(fits_read_key(infp,TSTRING,"TDIM17",tempChars,comment,&status)) {printerror(status); return false;}
    sstr.str("");
    for(int i=0;i<naxis;i++) {if(i==0) sstr<<"(";  sstr<<naxes[i];   if(i!=naxis-1) sstr<<","; else sstr<<")"; }
    newNumberStr=sstr.str();    strcpy(value,newNumberStr.c_str());
    if(fits_update_key(outfp,TSTRING,"TDIM17",value,comment,&status)) {printerror(status); return false;}

    //update NCHAN
    newNumber=channelNoTo-channelNoFrom+1;
    if(fits_read_key(infp,TLONGLONG,"NCHAN",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"NCHAN",&newNumber,comment,&status)) {printerror(status); return false;}

    //update NPOL
    newNumber=1;
    if(fits_read_key(infp,TLONGLONG,"NPOL",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"NPOL",&newNumber,comment,&status)) {printerror(status); return false;}


    if(fits_movabs_hdu(infp,1,&hdutype,&status)) printerror(status);
    if(fits_movabs_hdu(outfp,1,&hdutype,&status)) printerror(status);
    // update OBSFREQ
    float tempFloat;
    if(fits_read_key(infp,TFLOAT,"OBSFREQ",&tempFloat,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TFLOAT,"OBSFREQ",&centerFreq,comment,&status)) {printerror(status); return false;}

    // update OBSBW
    if(fits_read_key(infp,TFLOAT,"OBSBW",&tempFloat,comment,&status)) {printerror(status); return false;}
    tempFloat = (channelNoTo-channelNoFrom+1)*channelBandWidth;
    if(fits_update_key(outfp,TFLOAT,"OBSBW",&tempFloat,comment,&status)) {printerror(status); return false;}

    // update OBSNCHAN
    newNumber=channelNoTo-channelNoFrom+1;
    if(fits_read_key(infp,TLONGLONG,"OBSNCHAN",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"OBSNCHAN",&newNumber,comment,&status)) {printerror(status); return false;}

    //reopen the output fits file. => recreate the fits file extention data part.
    if(fits_close_file(outfp,&status)) {printerror(status); return false;}
    if(fits_open_file(&outfp,outFitsFilename.c_str(),READWRITE,&status)) {printerror(status); return false;}
    if(fits_movabs_hdu(outfp,2,&hdutype,&status)) { printerror(status); status=0; fits_close_file(outfp,&status); return false; }

    //TODO extract the data
    if(fits_movabs_hdu(infp,2,&hdutype,&status)) printerror(status);
    long long destOffset,sourceBufferOffset,len;
    u_char *sourceBuffer=new u_char[info.colsSize];
    for(long long row = 1; row <= info.nRows; row++){
        //read a row from source to sourceBuffer
        if(fits_read_tblbytes(infp,row,1,info.colsSize,sourceBuffer,&status)) printerror(status);

        //column before 13
        destOffset=1;
        sourceBufferOffset=0;
        len = info.leadingCol13Size;
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 13: DAT_FREQ   /NCHAN floats
        sourceBufferOffset = info.leadingCol13Size + info.col13ElementWidth*(channelNoFrom-1);
        len = info.col13ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 14: DAT_WTS    /NCHAN floats
        sourceBufferOffset = info.leadingCol14Size + info.col14ElementWidth*(channelNoFrom-1);
        len = info.col14ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 15: DAT_OFFS   /NCHAN*NPOL floats
        sourceBufferOffset = info.leadingCol15Size + ((polNo-1)*info.nChannels + channelNoFrom -1)*info.col15ElementWidth;
        len = info.col15ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 16: DAT_SCL   /NCHAN*NPOL floats
        sourceBufferOffset = info.leadingCol16Size + ((polNo-1)*info.nChannels + channelNoFrom -1)*info.col16ElementWidth;
        len = info.col16ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 17: DATA      /(NBITS or NBIN,NCHAN,NPOL,NSBLK)
        for(int iSample=0; iSample<info.nSamples; iSample++){
            sourceBufferOffset = info.leadingCol17Size + iSample*sizePerSampleOfCol17 + (polNo-1)*sizePerPolOfCol17 + (channelNoFrom -1)*sizePerChannelOfCol17;
            len = sizePerChannelOfCol17 * (channelNoTo-channelNoFrom+1);
            if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
            destOffset += len;
       }
    }

    // save out file
    delete[] sourceBuffer;
    fits_close_file(infp,&status);
    fits_close_file(outfp,&status);

    //end = clock();

    //cout << "CLOCKS_PER_SEC " << CLOCKS_PER_SEC << "\n";
    //cout << "CPU-TIME START " << start << "\n";
    //cout << "CPU-TIME END " << end << "\n";
    //cout << "CPU-TIME END - START " <<  end - start << "\n";
    //cout << "TIME(SEC) " << static_cast<double>(end - start) / CLOCKS_PER_SEC << "\n";

    return true;
}

// extract data to a new fits file which name is outFitsFilename.
// info: source fits file information
// the output fits will contain channel between channelNoFrom to channelNoTo and the polar is polNo.
// channelFromNo>=1, channelToNo>1, polNo>=1, channelNoFrom<=channelNoTo
bool extractFits(FASTFitsDataInfo &info, int channelNoFrom, int channelNoTo, int polNo, string outFitsFilename, float centerFreq, bool isReverse){
    //check the channel number and the actual range of channel number.
    if(channelNoFrom>channelNoTo || polNo >info.nPols) return false;
    //ATTENSION!
    if(info.bitpix/8*8 != info.bitpix) {
        cout<<"Extract failure. The BITPIX should be multiple of 8!"<<endl;
        return false;
    }

    long sizePerChannelOfCol17 = info.bitpix/8;
    long sizePerPolOfCol17 = info.nChannels * sizePerChannelOfCol17;
    long sizePerSampleOfCol17 = info.nPols*sizePerPolOfCol17;

    //clock_t start, end;
    //start = clock();

    //open input and output file
    ifstream source(info.filename, ios::binary);
    if(!source){
        cout<<"Fail to open "<<info.filename<<"."<<endl;
        return false;
    }
    ofstream dest(outFitsFilename, ios::binary|ios::trunc);
    if(!dest){
        cout<<"Fail to create output fits file "<<outFitsFilename<<"."<<endl;
        source.close();
        return false;
    }

    //copy primary hdu and extension header
    size_t size=info.extensionHduDataOffset;// allocate memory for buffer
    char* buffer = new char[size];
    source.seekg(0);
    source.read(buffer, size);
    dest.write(buffer, size);

    // clean up
    delete[] buffer;
    source.close();
    dest.close();

    fitsfile *infp,*outfp=NULL;
    int status=0;
    int hdutype;
    //open fits file
    if(fits_open_file(&infp,info.filename.c_str(),READONLY,&status)) {printerror(status); return false;}
    if(fits_movabs_hdu(infp,2,&hdutype,&status)) {printerror(status); status=0; fits_close_file(infp,&status); return false;}
    if(fits_open_file(&outfp,outFitsFilename.c_str(),READWRITE,&status)) {printerror(status); return false;}
    if(fits_movabs_hdu(outfp,2,&hdutype,&status)) printerror(status);

    if(centerFreq<=0.0){ //calculate center frequency
        long repeat;
        fits_get_coltype(infp, 13, NULL, &repeat, NULL, &status);
        float *freq = new float[repeat];
        if(fits_read_col(infp,TFLOAT,13,1,1,repeat,NULL,freq,NULL,&status)){
            cout<<"failure to read frequency in "<<info.filename<<endl;
            delete[] freq;
            return false;
        }
        centerFreq=(freq[channelNoFrom-1]+freq[channelNoTo-1])/2.0;
        delete[] freq;
    }

    char comment[80]="changed",tempChars[80], value[80];
    long long newNumber;
    float channelBandWidth=0.0;
    if(fits_read_key(infp,TFLOAT,"CHAN_BW",&channelBandWidth,comment,&status)) {printerror(status); return false;}

    // update NAXIS1 NAXIS2
    newNumber = info.colsSize
            -(channelNoFrom-1 + info.nChannels-channelNoTo)*info.col13ElementWidth //col13
            -(channelNoFrom-1 + info.nChannels-channelNoTo)*info.col14ElementWidth  //col14
            -((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo))*info.col15ElementWidth   //col15
            -((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo))*info.col16ElementWidth   //col16
            -info.nSamples*( (info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo) )*sizePerChannelOfCol17;  //col17

    long long tempLL;
    //if(fits_read_key(fp1,TLONGLONG,"NAXIS2",&tempLL,comment,&status)) {printerror(status); return false;}
    //tempLL=0;
    //if(fits_update_key(outfp,TLONGLONG,"NAXIS2",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_read_key(infp,TLONGLONG,"NAXIS1",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"NAXIS1",&newNumber,comment,&status)) {printerror(status); return false;}

    stringstream sstr;
    string newNumberStr;
    //TODO update col 13  TFORM13
    newNumber = (info.leadingCol14Size-info.leadingCol13Size)/info.col13ElementWidth-(channelNoFrom-1 + info.nChannels-channelNoTo);
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM13",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM13",value,comment,&status)) {printerror(status); return false;}

    //TODO update col 14
    newNumber = (info.leadingCol15Size-info.leadingCol14Size)/info.col14ElementWidth-(channelNoFrom-1 + info.nChannels-channelNoTo);
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM14",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM14",value,comment,&status)) {printerror(status); return false;}

    //TODO update col 15
    newNumber = (info.leadingCol16Size-info.leadingCol15Size)/info.col15ElementWidth-((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo));
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM15",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM15",value,comment,&status)) {printerror(status); return false;}

    //TODO update col 16
    newNumber = (info.leadingCol17Size-info.leadingCol16Size)/info.col16ElementWidth-((info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo));
    sstr.str("");
    sstr<<newNumber<<"E";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM16",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM16",value,comment,&status)) {printerror(status); return false;}

    //TODO update TFORM17
    newNumber = (info.colsSize-info.leadingCol17Size)/sizePerChannelOfCol17-info.nSamples*( (info.nPols -1)*info.nChannels + (channelNoFrom-1 + info.nChannels-channelNoTo) );
    sstr.str("");
    sstr << newNumber<<"B";
    newNumberStr = sstr.str();
    strcpy(value,newNumberStr.c_str());
    if(fits_read_key(infp,TSTRING,"TFORM17",tempChars,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TSTRING,"TFORM17",value,comment,&status)) {printerror(status); return false;}

    //update TDIM17
    int naxis=0;
    long naxes[10];
    if(fits_read_tdim(infp,17,10,&naxis,naxes,&status)) {printerror(status); return false;}
    naxes[1]=channelNoTo-channelNoFrom+1;
    naxes[2]=1;
    //if(fits_write_tdim(outfp,17,naxis,naxes,&status)) printerror(status); //add keyword instead of update
    if(fits_read_key(infp,TSTRING,"TDIM17",tempChars,comment,&status)) {printerror(status); return false;}
    sstr.str("");
    for(int i=0;i<naxis;i++) {if(i==0) sstr<<"(";  sstr<<naxes[i];   if(i!=naxis-1) sstr<<","; else sstr<<")"; }
    newNumberStr=sstr.str();    strcpy(value,newNumberStr.c_str());
    if(fits_update_key(outfp,TSTRING,"TDIM17",value,comment,&status)) {printerror(status); return false;}

    //update NCHAN
    newNumber=channelNoTo-channelNoFrom+1;
    if(fits_read_key(infp,TLONGLONG,"NCHAN",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"NCHAN",&newNumber,comment,&status)) {printerror(status); return false;}

    //update NPOL
    newNumber=1;
    if(fits_read_key(infp,TLONGLONG,"NPOL",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"NPOL",&newNumber,comment,&status)) {printerror(status); return false;}


    if(fits_movabs_hdu(infp,1,&hdutype,&status)) printerror(status);
    if(fits_movabs_hdu(outfp,1,&hdutype,&status)) printerror(status);
    // update OBSFREQ
    float tempFloat;
    if(fits_read_key(infp,TFLOAT,"OBSFREQ",&tempFloat,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TFLOAT,"OBSFREQ",&centerFreq,comment,&status)) {printerror(status); return false;}

    // update OBSBW
    if(fits_read_key(infp,TFLOAT,"OBSBW",&tempFloat,comment,&status)) {printerror(status); return false;}
    tempFloat = (channelNoTo-channelNoFrom+1)*channelBandWidth;
    if(fits_update_key(outfp,TFLOAT,"OBSBW",&tempFloat,comment,&status)) {printerror(status); return false;}

    // update OBSNCHAN
    newNumber=channelNoTo-channelNoFrom+1;
    if(fits_read_key(infp,TLONGLONG,"OBSNCHAN",&tempLL,comment,&status)) {printerror(status); return false;}
    if(fits_update_key(outfp,TLONGLONG,"OBSNCHAN",&newNumber,comment,&status)) {printerror(status); return false;}

    //reopen the output fits file. => recreate the fits file extention data part.
    if(fits_close_file(outfp,&status)) {printerror(status); return false;}
    if(fits_open_file(&outfp,outFitsFilename.c_str(),READWRITE,&status)) {printerror(status); return false;}
    if(fits_movabs_hdu(outfp,2,&hdutype,&status)) { printerror(status); status=0; fits_close_file(outfp,&status); return false; }

    //TODO extract the data
    if(fits_movabs_hdu(infp,2,&hdutype,&status)) printerror(status);
    long long destOffset,sourceBufferOffset,len;
    u_char *sourceBuffer=new u_char[info.colsSize];
    for(long long row = 1; row <= info.nRows; row++){
        //read a row from source to sourceBuffer
        if(fits_read_tblbytes(infp,row,1,info.colsSize,sourceBuffer,&status)) printerror(status);

        //column before 13
        destOffset=1;
        sourceBufferOffset=0;
        len = info.leadingCol13Size;
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 13: DAT_FREQ   /NCHAN floats
        sourceBufferOffset = info.leadingCol13Size + info.col13ElementWidth*(channelNoFrom-1);
        len = info.col13ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 14: DAT_WTS    /NCHAN floats
        sourceBufferOffset = info.leadingCol14Size + info.col14ElementWidth*(channelNoFrom-1);
        len = info.col14ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 15: DAT_OFFS   /NCHAN*NPOL floats
        sourceBufferOffset = info.leadingCol15Size + ((polNo-1)*info.nChannels + channelNoFrom -1)*info.col15ElementWidth;
        len = info.col15ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 16: DAT_SCL   /NCHAN*NPOL floats
        sourceBufferOffset = info.leadingCol16Size + ((polNo-1)*info.nChannels + channelNoFrom -1)*info.col16ElementWidth;
        len = info.col16ElementWidth * (channelNoTo-channelNoFrom+1);
        if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
        destOffset += len;

        //extract column 17: DATA      /(NBITS or NBIN,NCHAN,NPOL,NSBLK)
        u_char *tempPartialSampleBuffer=nullptr, *tempChannelBuffer=nullptr, *pSampleData;
        if(isReverse) {
            tempPartialSampleBuffer=new u_char[sizePerChannelOfCol17 * (channelNoTo-channelNoFrom+1)];
            tempChannelBuffer=new u_char[sizePerChannelOfCol17];
        }
        for(int iSample=0; iSample<info.nSamples; iSample++){
            len = sizePerChannelOfCol17 * (channelNoTo-channelNoFrom+1);

            if(isReverse){
                // point to the whole sample
                pSampleData = sourceBuffer + info.leadingCol17Size + iSample*sizePerSampleOfCol17 + (polNo-1)*sizePerPolOfCol17;
                // copy the partial sample data to temp buffer
                memcpy(tempPartialSampleBuffer, pSampleData+(info.nChannels - channelNoTo)*sizePerChannelOfCol17,len);
                //reverse tempPartialSampleBuffer
                for(int i=0;i<(channelNoTo-channelNoFrom+1)/2;i++) {
                    memcpy(tempChannelBuffer,tempPartialSampleBuffer+i*sizePerChannelOfCol17,sizePerChannelOfCol17);
                    memcpy(tempPartialSampleBuffer+i*sizePerChannelOfCol17,tempPartialSampleBuffer+(channelNoTo-channelNoFrom-i)*sizePerChannelOfCol17,sizePerChannelOfCol17);
                    memcpy(tempPartialSampleBuffer+(channelNoTo-channelNoFrom-i)*sizePerChannelOfCol17,tempChannelBuffer,sizePerChannelOfCol17);
                }
                //copy back to the right position
                memcpy(pSampleData+(channelNoFrom-1)*sizePerChannelOfCol17, tempPartialSampleBuffer, len);
            }

            sourceBufferOffset = info.leadingCol17Size + iSample*sizePerSampleOfCol17 + (polNo-1)*sizePerPolOfCol17 + (channelNoFrom -1)*sizePerChannelOfCol17;
            if(fits_write_tblbytes(outfp, row, destOffset, len, sourceBuffer + sourceBufferOffset, &status)) printerror(status);
            destOffset += len;
        }
        if(isReverse && tempPartialSampleBuffer) delete[] tempPartialSampleBuffer;
        if(isReverse && tempChannelBuffer) delete[] tempChannelBuffer;
    }

    // save out file
    delete[] sourceBuffer;
    fits_close_file(infp,&status);
    fits_close_file(outfp,&status);

    //end = clock();

    //cout << "CLOCKS_PER_SEC " << CLOCKS_PER_SEC << "\n";
    //cout << "CPU-TIME START " << start << "\n";
    //cout << "CPU-TIME END " << end << "\n";
    //cout << "CPU-TIME END - START " <<  end - start << "\n";
    //cout << "TIME(SEC) " << static_cast<double>(end - start) / CLOCKS_PER_SEC << "\n";

    return true;
}


// extract data to a new fits file which name is outFitsFilename.
// info: source fits file information
// the output fits will contain channel between channelNoFrom to channelNoTo and the polar is polNo.
// channelFromNo>=1, channelToNo>1, polNo>=1, channelNoFrom<=channelNoTo
bool extractFits(string filename, int channelNoFrom, int channelNoTo, int polNo, string outFitsFilename){
    FASTFitsDataInfo info;
    fitsfile *fptr;
    int status=0;
    if(fits_open_file(&fptr, filename.c_str(), READONLY, &status)){
        cout<<"failure to open "<<filename<<endl;
        return false;
    }
    info.filename=filename;
    bool isOk = readFASTFitsInfo(fptr,info);
    fits_close_file(fptr, &status);

    return (isOk?extractFits(info,channelNoFrom,channelNoTo,polNo,outFitsFilename):false);
}

// extract data to a new fits file which name is outFitsFilename.
// info: source fits file information
// the output fits will contain channel between channelNoFrom to channelNoTo and the polar is polNo.
// channelFromNo>=1, channelToNo>1, polNo>=1, channelNoFrom<=channelNoTo
bool extractFits(string filename, float channelFreqFrom, float channelFreqTo, int polNo, string outFitsFilename,bool isReverseChannel){
    int channelNoFrom=-1, channelNoTo=-1;
    int hdutype;
    FASTFitsDataInfo info;
    fitsfile *fptr;
    int status=0;
    if(fits_open_file(&fptr, filename.c_str(), READONLY, &status)){
        cout<<"failure to open "<<filename<<endl;
        return false;
    }
    info.filename=filename;
    bool isOk = readFASTFitsInfo(fptr,info);

    // calculate freq range
    //read the leading bytes count for some colomns
    long repeat;
    fits_movabs_hdu(fptr,2,&hdutype,&status);
    float subBandWidth;
    if(fits_read_key(fptr,TFLOAT,"CHAN_BW",&subBandWidth,NULL,&status)) return false;
    subBandWidth/=2;

    //int typecode;long width;
    fits_get_coltype(fptr, 13, NULL, &repeat, NULL, &status);
    float *freq = new float[repeat];
    if(freq==nullptr) return false;

    if(fits_read_col(fptr,TFLOAT,13,1,1,repeat,NULL,freq,NULL,&status)){
        cout<<"failure to read frequency in "<<filename<<endl;
        delete[] freq;
        return false;
    }
    for(int i=0;i<repeat;i++){
        if(channelFreqFrom>= freq[i]-subBandWidth && channelFreqFrom<freq[i]+subBandWidth){
            channelNoFrom=i+1;
            break;
        }
    }
    for(int i=0;i<repeat;i++){
        if(channelFreqTo> freq[i]-subBandWidth && channelFreqTo<=freq[i]+subBandWidth){
            channelNoTo=i+1;
            break;
        }
    }
    fits_close_file(fptr, &status);
    if(channelNoFrom<0) channelNoFrom=1;
    if(channelNoTo<channelNoFrom) {
        cout<<"Cannot find frequency data between "<<channelFreqFrom <<" and "<<channelFreqTo<<" MHz"<<endl;
        delete[] freq;
        return false;
    }
    float centerFreq=(freq[channelNoFrom-1]+freq[channelNoTo-1])/2.0;
    delete[] freq;

    return (isOk?extractFits(info,channelNoFrom,channelNoTo,polNo,outFitsFilename,centerFreq,isReverseChannel):false);
}

// set the OFFS_SUB of second fits file identy as reference fits file.
// note: before calling this function, be sure to close the second fits file
bool normalizeOFFS_SUB(const FASTFitsDataInfo& refFitsInfo, FASTFitsDataInfo& info){
    // whether need normalize or not?
    double diff=(info.stt_imjd*86400+info.stt_smjd+info.stt_offs)-(refFitsInfo.stt_imjd*86400+refFitsInfo.stt_smjd+refFitsInfo.stt_offs);
    if((diff>0?diff:-diff)<1e-7) return true; // not need

    // need normalization
    fitsfile *fptr;       // pointer to the FITS file, defined in fitsio.h
    int status=0, hdutype;

    if (fits_open_file(&fptr, info.filename.c_str(), READWRITE, &status)){
        printerror(status);
        return false;
    }

    if(fits_movabs_hdu(fptr, 2, &hdutype, &status)){
        printerror(status);
        status=0;
        fits_close_file(fptr, &status);
        return false;
    }
    double *data=new double[info.nRows],floatnull;
    int anynull;
    if(fits_read_col(fptr, TDOUBLE, 2, 1, 1, info.nRows, &floatnull, data, &anynull, &status)){
        printerror(status);
        delete[] data;
        status=0;
        fits_close_file(fptr, &status);
        return false;
    }

    for(size_t i=0;i<info.nRows;i++)  data[i]+=diff;
    if(fits_write_col_dbl(fptr, 2, 1, 1, info.nRows, data, &status)){
        printerror(status);
        delete[] data;
        status=0;
        fits_close_file(fptr, &status);
        return false;
    }

    info.stt_imjd=refFitsInfo.stt_imjd;
    info.stt_smjd=refFitsInfo.stt_smjd;
    info.stt_offs=refFitsInfo.stt_offs;

    if (fits_close_file(fptr, &status)){
        printerror(status);
        return false;
    }

    return true;
}

// append the fits extension data to the outFilename file. If doesn't exist, it will be created.
// the old outFilename file will be appended.
bool mergeFitsFile(string inFilenames[], int nInFiles, string outFilename){
    if(inFilenames==NULL || nInFiles<=0) return false;
    int status=0;
    fstream *pdest;
    ifstream *psource;
    FASTFitsDataInfo info1, info2;
    int firstFileNo=0;
    long long nRows=0;

//    clock_t start, end;
//    start = clock();

    fitsfile *fitsfp;
    bool isOK=false;
    //fits file outFilename exists.
    if(!outFilename.empty() && !fits_open_file(&fitsfp,outFilename.c_str(),READONLY,&status)){
        info1.filename=outFilename;
        isOK=readFASTFitsInfo(fitsfp,info1);
        fits_close_file(fitsfp,&status);
        if(isOK){
            pdest= new fstream(outFilename, ios::binary|ios::out|ios::in);
            if(!pdest && !(*pdest)) {
                cout<<"Create file "<<outFilename<<" fail."<<endl;
                return false;
            }
            long long sourceLength=info1.extensionHduDataOffset+info1.nRows*info1.colsSize;
            pdest->seekp(sourceLength);
            nRows += info1.nRows;

            //cout<<outFilename<<": will be appended."<<endl;
        }
    }

    size_t bufferSize=512*1024*1024;
    char *buffer= new char[bufferSize];

    // outFilename fits file not exists.
    if(!isOK){
        //find the first valid fits file and copy it to output fits file.
        while(!isOK && firstFileNo<nInFiles){
            status=0;
            if(!fits_open_file(&fitsfp,inFilenames[firstFileNo].c_str(),READONLY,&status)){
                info1.filename=inFilenames[firstFileNo];
                isOK=readFASTFitsInfo(fitsfp,info1);
                fits_close_file(fitsfp,&status);
                if(isOK){
                    pdest= new fstream(outFilename, ios::binary|ios::trunc|ios::out);
                    if(!pdest && !(*pdest)) {
                        cout<<"Create file "<<outFilename<<" fail."<<endl;
                        return false;
                    }
                    psource = new ifstream(inFilenames[firstFileNo],ios::binary);
                    if(!psource && !(*psource)) {
                        isOK=false;
                    }
                    else{ // copy current file to destination file.
                        //*pdest << psource->rdbuf();
                        long long sourceLength=info1.extensionHduDataOffset+info1.nRows*info1.colsSize;
                        long long sourceOffset=0;
                        long long len;
                        while(sourceOffset<sourceLength){
                            len= sourceLength-sourceOffset; // remain length to read
                            len = (len<bufferSize)?len:bufferSize; // read once now
                            psource->read(buffer, len);
                            pdest->write(buffer,len);
                            sourceOffset+=len;
                        }
                        psource->close();
                        delete psource;
                        nRows += info1.nRows;

                        //cout<<outFilename<<": "<<inFilenames[firstFileNo]<<" appended."<<endl;
                    }
                }
            }
            if(!isOK) cout<<"Read file "<<inFilenames[firstFileNo]<<" fail."<<endl;
            firstFileNo++;
        }
    }

    if(!isOK) {
        delete[] buffer;
        return false; // there is not a file can open as a source.
    }

    // check and append other fits file to output fits file.
    for(int fileNo=firstFileNo; fileNo<nInFiles; fileNo++){
            if(fits_open_file(&fitsfp,inFilenames[fileNo].c_str(),READONLY,&status)){
                printerror(status);
                status=0;
                cout<<outFilename<<": "<<inFilenames[fileNo]<<" not appended. Open failure."<<endl;
            }else{
                info2.filename=inFilenames[fileNo];
                isOK=readFASTFitsInfo(fitsfp,info2);
                fits_close_file(fitsfp,&status);
                // merge files
                if(isOK && canMerge(info1,info2)){
                    normalizeOFFS_SUB(info1,info2);
                    psource = new ifstream(inFilenames[fileNo],ios::binary);
                    if(psource && *psource) {
                        psource->seekg(info2.extensionHduDataOffset);
                        long long sourceLength=info2.nRows*info1.colsSize;
                        long long sourceOffset=0;
                        long long len;
                        while(sourceOffset<sourceLength){
                            len= sourceLength-sourceOffset; // remain length to read
                            len = (len<bufferSize)?len:bufferSize; // read once now
                            psource->read(buffer, len);
                            pdest->write(buffer,len);
                            sourceOffset+=len;
                        }
                        psource->close();
                        delete psource;
                        nRows += info2.nRows;

                        //cout<<outFilename<<": "<<inFilenames[fileNo]<<" appended."<<endl;
                    }
                }else{
                    cout<<outFilename<<": "<<inFilenames[fileNo]<<" not appended. file discompatable."<<endl;
                }
            }
    }

    delete[] buffer;

    // close the output fits file
    if(pdest && *pdest){
        pdest->flush();
        pdest->close();
        delete pdest;
    }

    // change NAXIS2
    char comment[80]="changed";
    long long tempLL;
    if(!fits_open_file(&fitsfp,outFilename.c_str(),READWRITE,&status)){
        if(fits_movabs_hdu(fitsfp,2,NULL,&status)) {printerror(status); status=0;}
        if(fits_read_key(fitsfp,TLONGLONG,"NAXIS2",&tempLL,comment,&status)) {printerror(status); status=0; }
        if(fits_update_key(fitsfp,TLONGLONG,"NAXIS2",&nRows,comment,&status)) {printerror(status); status=0;}
        fits_close_file(fitsfp,&status);
    }

//    cout<<outFliename<<": Saved."<<endl;

//    end = clock();

//    cout << "CLOCKS_PER_SEC " << CLOCKS_PER_SEC << "\n";
//    cout << "CPU-TIME START " << start << "\n";
//    cout << "CPU-TIME END " << end << "\n";
//    cout << "CPU-TIME END - START " <<  end - start << "\n";
//    cout << "TIME(SEC) " << static_cast<double>(end - start) / CLOCKS_PER_SEC << "\n";

    return true;
}

// read the time reletive parameter and store to row, samplesPerRow, timePerSample, allTimeLen.
// Unit: second.
bool getTimeLen(string filename, long *row, long *samplesPerRow, float *timePerSample, float *allTimeLen){
    fitsfile *fptr;       // pointer to the FITS file, defined in fitsio.h
    int status=0, hdutype;

    if ( fits_open_file(&fptr, filename.c_str(), READONLY, &status) ){
        printerror( status );
        return false;
    }

    long _row, _samplesPerRow;
    float _timePerSample;

    if(fits_movabs_hdu(fptr,2,&hdutype,&status)) return false;
    if(fits_read_key(fptr,TLONG,"NAXIS2",&_row,NULL,&status)) return false;
    if(fits_read_key(fptr,TFLOAT,"TBIN",&_timePerSample,NULL,&status)) return false;
    if(fits_read_key(fptr,TLONG,"NSBLK",&_samplesPerRow,NULL,&status)) return false;

    fits_close_file(fptr,&status);

    if(row!=nullptr) *row=_row;
    if(samplesPerRow!=nullptr) *samplesPerRow=_samplesPerRow;
    if(timePerSample!=nullptr) *timePerSample=_timePerSample;
    if(allTimeLen!=nullptr) *allTimeLen=_row*_samplesPerRow*_timePerSample;

    return true;
}


// Create a new outfilename file and append the all following fits extensions data to the first fits, and output to outFilename file.
// the old outfilename file will be overwrite.
bool mergeFitsFile1(string inFilenames[], int nInFiles, string outFliename){
    if(inFilenames==NULL || nInFiles<=0) return false;
    int status=0;
    ofstream *pdest;
    ifstream *psource;
    FASTFitsDataInfo info1, info2;
    int firstFileNo=0;
    long long nRows=0;

//    clock_t start, end;
//    start = clock();

    //char buffer[512*1024*1024];
    size_t bufferSize=512*1024*1024;
    char *buffer= new char[bufferSize];

    fitsfile *fitsfp;
    bool isOK=false;
    //find the first valid fits file and copy it to output fits file.
    while(!isOK && firstFileNo<nInFiles){
        status=0;
        if(!fits_open_file(&fitsfp,inFilenames[firstFileNo].c_str(),READONLY,&status)){
            info1.filename=inFilenames[firstFileNo];
            isOK=readFASTFitsInfo(fitsfp,info1);
            fits_close_file(fitsfp,&status);
            if(isOK){
                pdest= new ofstream(outFliename, ios::binary|ios::trunc);
                if(!pdest && !(*pdest)) {
                    cout<<"Create file "<<outFliename<<" fail."<<endl;
                    return false;
                }
                psource = new ifstream(inFilenames[firstFileNo],ios::binary);
                if(!psource && !(*psource)) {
                    isOK=false;
                }
                else{
                    //*pdest << psource->rdbuf();
                    long long sourceLength=info1.extensionHduDataOffset+info1.nRows*info1.colsSize;
                    long long sourceOffset=0;
                    long long len;
                    while(sourceOffset<sourceLength){
                        len= sourceLength-sourceOffset; // remain length to read
                        len = (len<bufferSize)?len:bufferSize; // read once now
                        psource->read(buffer, len);
                        pdest->write(buffer,len);
                        sourceOffset+=len;
                    }
                    psource->close();
                    delete psource;
                    nRows += info1.nRows;

                    //cout<<outFliename<<": "<<inFilenames[firstFileNo]<<" appended."<<endl;
                }
            }
        }
        if(!isOK) cout<<"Read file "<<inFilenames[firstFileNo]<<" fail."<<endl;
        firstFileNo++;
    }

    delete[] buffer;
    if(!isOK) return false; // there is not a file can open as a source.

    // check and append other fits file to output fits file.
    for(int fileNo=firstFileNo; fileNo<nInFiles; fileNo++){
            if(fits_open_file(&fitsfp,inFilenames[fileNo].c_str(),READONLY,&status)){
                printerror(status);
                status=0;
                cout<<outFliename<<": "<<inFilenames[fileNo]<<" not appended. Open failure."<<endl;
            }else{
                info2.filename=inFilenames[fileNo];
                isOK=readFASTFitsInfo(fitsfp,info2);
                fits_close_file(fitsfp,&status);
                if(isOK && canMerge(info1,info2)){
                    psource = new ifstream(inFilenames[fileNo],ios::binary);
                    if(psource && *psource) {
                        psource->seekg(info2.extensionHduDataOffset);
                        long long sourceLength=info2.nRows*info1.colsSize;
                        long long sourceOffset=0;
                        long long len;
                        while(sourceOffset<sourceLength){
                            len= sourceLength-sourceOffset; // remain length to read
                            len = (len<bufferSize)?len:bufferSize; // read once now
                            psource->read(buffer, len);
                            pdest->write(buffer,len);
                            sourceOffset+=len;
                        }
                        psource->close();
                        delete psource;
                        nRows += info2.nRows;

                        //cout<<outFliename<<": "<<inFilenames[fileNo]<<" appended."<<endl;
                    }
                }else{
                    cout<<outFliename<<": "<<inFilenames[fileNo]<<" not appended. file discompatable."<<endl;
                }
            }
    }

    // close the output fits file
    if(pdest && *pdest){
        pdest->flush();
        pdest->close();
        delete pdest;
    }

    // change NAXIS2
    char comment[80]="changed";
    long long tempLL;
    if(!fits_open_file(&fitsfp,outFliename.c_str(),READWRITE,&status)){
        if(fits_movabs_hdu(fitsfp,2,NULL,&status)) {printerror(status); status=0;}
        if(fits_read_key(fitsfp,TLONGLONG,"NAXIS2",&tempLL,comment,&status)) {printerror(status); status=0; }
        if(fits_update_key(fitsfp,TLONGLONG,"NAXIS2",&nRows,comment,&status)) {printerror(status); status=0;}
        fits_close_file(fitsfp,&status);
    }

//    cout<<outFliename<<": Saved."<<endl;

//    end = clock();

//    cout << "CLOCKS_PER_SEC " << CLOCKS_PER_SEC << "\n";
//    cout << "CPU-TIME START " << start << "\n";
//    cout << "CPU-TIME END " << end << "\n";
//    cout << "CPU-TIME END - START " <<  end - start << "\n";
//    cout << "TIME(SEC) " << static_cast<double>(end - start) / CLOCKS_PER_SEC << "\n";

    return true;
}

bool isDataIdent(string filename1,string filename2){
    fitsfile *fp1,*fp2;
    int status=0,hdutype;
    if ( fits_open_file(&fp1, filename1.c_str(), READONLY, &status) )
        printerror( status );
    if ( fits_open_file(&fp2, filename2.c_str(), READONLY, &status) )
        printerror( status );

    FASTFitsDataInfo info1,info2;
    info1.filename=filename1;
    info2.filename=filename2;
    readFASTFitsInfo(fp1,info1);
    readFASTFitsInfo(fp2,info2);

    fits_movabs_hdu(fp1, 2, &hdutype, &status) ;
    fits_movabs_hdu(fp2, 2, &hdutype, &status) ;

    long long size1=info1.colsSize-info1.leadingCol17Size;
    long long size2=info2.colsSize-info2.leadingCol17Size;

    cout<<"Item            Fits 1          Fits 2"<<endl;
    cout<<"col17 size      "<<size1<<"         "<<size2<<endl;
    cout<<"nRows      "<<info1.nRows<<"         "<<info2.nRows<<endl;
    u_char floatnull;
    int anynull;
    u_char *data1=new u_char[size1];
    u_char *data2=new u_char[size2];
    long long nRows=info1.nRows<info2.nRows?info1.nRows:info2.nRows;
    bool isI=true;
    for(long row=1;row<=nRows;row++){
        fits_read_col(fp1, TBYTE, 17, row, 1, size1, &floatnull, data1, &anynull, &status);
        fits_read_col(fp2, TBYTE, 17, row, 1, size2, &floatnull, data2, &anynull, &status);
        isI=true;
        for(int i=0;i<size1;i++)
            if(data1[i]!=data2[i]){
                isI=false;
                break;
            }
        cout<<"Row "<<row<<": "<<(isI?"OK":"Diff")<<endl;
    }

    delete[] data1;
    delete[] data2;

    if ( fits_close_file(fp1, &status) )
        printerror( status );
    if ( fits_close_file(fp2, &status) )
        printerror( status );

    return isI;
}

void dataView(string filename){
    fitsfile *fp1;//,*fp2;
    int status=0,hdutype;
    if ( fits_open_file(&fp1, filename.c_str(), READONLY, &status) )
        printerror( status );

    FASTFitsDataInfo info;
    readFASTFitsInfo(fp1,info);



    fits_movabs_hdu(fp1, 2, &hdutype, &status) ;


    double floatnull;
    int anynull;
    double *data1=new double[info.nRows];
    //u_char *data2=new u_char[info.nRows];
    long long nRows=info.nRows;
    fits_read_col(fp1, TDOUBLE, 2, 1, 1, info.nRows, &floatnull, data1, &anynull, &status);
    for(long row=0;row<nRows;row++){
        cout<<"Row "<<row<<": "<<data1[row]<<endl;
    }

    if ( fits_close_file(fp1, &status) )
        printerror( status );

}
