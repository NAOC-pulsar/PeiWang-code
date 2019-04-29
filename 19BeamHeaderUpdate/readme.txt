
包含
合并程序：combine_fits.py
python combine_fits.py [root] [fitslist.txt]
# How to use combine_fits.py to combine the subints from multi-datafiles
# By Wangpei 2018/07/11


Two inputs:
--------------------
1. [root] is the operational root for storing the output fits file, e.g. /wangpei/work2/test/new, which means that the newly combined fitsfile "new.fits" will be created under the root of "/wangpei/work2/test".

2. [fitslist.txt] is the name list of all the fits files you want to combine. Use "ls *.fits > fitsfile.txt".

*  Please copy and keep to run the program file "combine_fits.py" in the same folder as fits datafiles and fitslist.txt.
** If need, you can cut the frequency range first for the raw datafiles, and then run the combine_fits.py faster.


程序：update_Header-OFFSSUB.py 更新合并文件的OFFSSUB
用法：ls *.fits > fitslist.txt
     python update_Header-OFFSSUB.py fitslist.txt

程序：stt_offs_check.py 检查待合并文件的stt是否错误
用法：ls *.fits > filelist.txt
      python stt_offs_check.py


程序：update_Header-TBIN-OFFSSUB.py 
用法见usage.txt
