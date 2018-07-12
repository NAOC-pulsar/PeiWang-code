import pyfits
import numpy as np

def wirtreToFileForFast(fits, filename, i, outpath):
    dataformat = str(np.size(fits.float_data2) / int(fits.numSubint)) + 'B'

    dataformat2 = str(fits.chnum) + 'E'

    dataformat3 = str(fits.chnum * 2) + 'E'

    dimformat = '(1,' + str(fits.chnum) + ',' + str(fits.Npolae) + ',' + str(fits.nsblk) + ')'

    dataformatnsblk = str(fits.nsblk)

    column2_data = pyfits.Column(name='TSUBINT', format='1D', array=fits.float_tsubint, unit='s')

    column3_data = pyfits.Column(name='OFFS_SUB', format='1D', array=fits.float_offs_sub, unit='s')

    column4_data = pyfits.Column(name='LST_SUB', format='1D', array=fits.float_lst_sub, unit='s')

    column5_data = pyfits.Column(name='RA_SUB', format='1D', array=fits.float_ra_sub, unit='deg')

    column6_data = pyfits.Column(name='DEC_SUB', format='1D', array=fits.float_dec_sub, unit='deg')

    column7_data = pyfits.Column(name='GLON_SUB', format='1D', array=fits.float_glon_sub, unit='deg')

    column8_data = pyfits.Column(name='GLAT_SUB', format='1D', array=fits.float_glat_sub, unit='deg')

    column9_data = pyfits.Column(name='FD_ANG', format='1E', array=fits.float_fd_ang, unit='deg')

    column10_data = pyfits.Column(name='POS_ANG', format='1E', array=fits.float_pos_ang, unit='deg')

    column11_data = pyfits.Column(name='PAR_ANG', format='1E', array=fits.float_par_ang, unit='deg')

    column12_data = pyfits.Column(name='TEL_AZ', format='1E', array=fits.float_tel_az, unit='deg')

    column13_data = pyfits.Column(name='TEL_ZEN', format='1E', array=fits.float_tel_zen, unit='deg')

    column16_data = pyfits.Column(name='DAT_FREQ', format=dataformat2, array=fits.float_dat_freq, unit='deg')

    column17_data = pyfits.Column(name='DAT_WTS', format=dataformat2, array=fits.float_dat_wts, unit='deg')

    column18_data = pyfits.Column(name='DAT_OFFS', format=dataformat3, array=fits.float_dat_offs, unit='deg')

    column19_data = pyfits.Column(name='DAT_SCL', format=dataformat3, array=fits.float_dat_scl, unit='MHz')

    column20_data = pyfits.Column(name='DATA', format=dataformat, array=fits.float_data2, dim=dimformat, unit='Jy')

    table_hdu = pyfits.new_table(
        [column2_data, column3_data, column4_data, column5_data, column6_data, column7_data, column8_data,
         column9_data, column10_data, column11_data, column12_data, column13_data, column16_data, column17_data,
         column18_data, column19_data, column20_data])

    table_hdu.header.append(('INT_TYPE', 'TIME', 'Time axis (TIME, BINPHSPERI, BINLNGASC, etc)'))

    table_hdu.header.append(('INT_UNIT', 'SEC', 'Unit of time axis (SEC, PHS (0-1),DEG)'))

    table_hdu.header.append(('SCALE', 'FluxDec', 'Intensiy units (FluxDec/RefFlux/Jansky)'))

    table_hdu.header.append(('NPOL', fits.Npolae, 'Nr of polarisations'))

    table_hdu.header.append(('POL_TYPE', '', 'Polarisation identifier (e.g., AABBCRCI, AA+BB)'))

    table_hdu.header.append(('TBIN', fits.sampleTime, '[s] Time per bin or sample'))

    table_hdu.header.append(('NBIN', 1, 'Nr of bins (PSR/CAL mode; else 1)'))

    table_hdu.header.append(('NBIN_PRD', 0, 'Nr of bins/pulse period (for gated data)'))

    table_hdu.header.append(('PHS_OFFS', 0.0, 'Phase offset of bin 0 for gated data'))

    table_hdu.header.append(('NBITS', 8, 'Nr of bits/datum (SEARCH mode "X" data, else 1)'))

    table_hdu.header.append(('NSUBOFFS', fits.nsuboffs_a, 'Subint offset (Contiguous SEARCH-mode files)'))

    table_hdu.header.append(('NCHAN', fits.chnum, 'Number of channels/sub-bands in this file'))

    table_hdu.header.append(('CHAN_BW', fits.chanBW, '[MHz] Channel/sub-band width'))

    table_hdu.header.append(('NCHNOFFS', 0, 'Channel/sub-band offset for split files'))

    table_hdu.header.append(('NSBLK', dataformatnsblk, 'Samples/row (SEARCH mode, else 1)'))

    table_hdu.header.append(('EXTNAME', 'SUBINT  ', 'name of this binary table extension'))

    hdulist2 = pyfits.HDUList([fits.hdu0, table_hdu])

    hdulist2.writeto(outpath)
    print 'file' + outpath + '  write successfully'


def wirtreToFileForParkes(fits, filename, i, outpath):
    dataformat = str(np.size(fits.float_data2) / int(fits.numSubint)) + 'X'

    dataformat2 = str(fits.chnum) + 'E'

    dataformat3 = str(fits.chnum * 2) + 'E'

    dimformat = '(1,' + str(fits.chnum) + ',' + str(fits.Npolae) + ',' + str(fits.nsblk) + ')'

    dataformatnsblk = str(fits.nsblk)

    column1_data = pyfits.Column(name='INDEXVAL', format='1D', array=fits.float_tsubint)

    column2_data = pyfits.Column(name='TSUBINT', format='1D', array=fits.float_tsubint, unit='s')

    column3_data = pyfits.Column(name='OFFS_SUB', format='1D', array=fits.float_offs_sub, unit='s')

    column4_data = pyfits.Column(name='LST_SUB', format='1D', array=fits.float_lst_sub, unit='s')

    column5_data = pyfits.Column(name='RA_SUB', format='1D', array=fits.float_ra_sub, unit='deg')

    column6_data = pyfits.Column(name='DEC_SUB', format='1D', array=fits.float_dec_sub, unit='deg')

    column7_data = pyfits.Column(name='GLON_SUB', format='1D', array=fits.float_glon_sub, unit='deg')

    column8_data = pyfits.Column(name='GLAT_SUB', format='1D', array=fits.float_glat_sub, unit='deg')

    column9_data = pyfits.Column(name='AUX_DM', format='1D', array=fits.float_aux_dm)

    column10_data = pyfits.Column(name='AUX_RM', format='1D', array=fits.float_aux_rm)

    column11_data = pyfits.Column(name='FD_ANG', format='1E', array=fits.float_fd_ang, unit='deg')

    column12_data = pyfits.Column(name='POS_ANG', format='1E', array=fits.float_pos_ang, unit='deg')

    column13_data = pyfits.Column(name='PAR_ANG', format='1E', array=fits.float_par_ang, unit='deg')

    column14_data = pyfits.Column(name='TEL_AZ', format='1E', array=fits.float_tel_az, unit='deg')

    column15_data = pyfits.Column(name='TEL_ZEN', format='1E', array=fits.float_tel_zen, unit='deg')

    column16_data = pyfits.Column(name='DAT_FREQ', format=dataformat2, array=fits.float_dat_freq, unit='deg')

    column17_data = pyfits.Column(name='DAT_WTS', format=dataformat2, array=fits.float_dat_wts, unit='deg')

    column18_data = pyfits.Column(name='DAT_OFFS', format=dataformat3, array=fits.float_dat_offs, unit='deg')

    column19_data = pyfits.Column(name='DAT_SCL', format=dataformat3, array=fits.float_dat_scl, unit='MHz')

    column20_data = pyfits.Column(name='DATA', format=dataformat, array=fits.float_data2, dim=dimformat, unit='Jy')

    table_hdu = pyfits.new_table(
        [column1_data, column2_data, column3_data, column4_data, column5_data, column6_data, column7_data,
         column8_data,
         column9_data, column10_data, column11_data, column12_data, column13_data, column14_data, column15_data,
         column16_data, column17_data,
         column18_data, column19_data, column20_data])

    table_hdu.header.append(('INT_TYPE', 'TIME', 'Time axis (TIME, BINPHSPERI, BINLNGASC, etc)'))

    table_hdu.header.append(('INT_UNIT', 'SEC', 'Unit of time axis (SEC, PHS (0-1),DEG)'))

    table_hdu.header.append(('SCALE', 'UNCAL', 'Intensiy units (FluxDec/RefFlux/Jansky)'))
    table_hdu.header.append(('POL_TYPE', "LIN", 'Polarisation identifier (e.g., AABBCRCI, AA+BB)'))

    table_hdu.header.append(('NPOL', int(fits.Npolae), 'Nr of polarisations'))

    table_hdu.header.append(('POL_TYPE', '', 'Polarisation identifier (e.g., AABBCRCI, AA+BB)'))

    table_hdu.header.append(('TBIN', fits.sampleTime, '[s] Time per bin or sample'))

    table_hdu.header.append(('NBIN', 1, 'Nr of bins (PSR/CAL mode; else 1)'))

    table_hdu.header.append(('NBIN_PRD', 0, 'Nr of bins/pulse period (for gated data)'))

    table_hdu.header.append(('PHS_OFFS', 0.0, 'Phase offset of bin 0 for gated data'))

    table_hdu.header.append(('NBITS', 1, 'Nr of bits/datum (SEARCH mode "X" data, else 1)'))

    table_hdu.header.append(('ZERO_OFF', 0, 'Zero offset for SEARCH-mode data'))

    table_hdu.header.append(('SIGNINT', '*', '1 for signed ints in SEARCH-mode data, else 0'))

    table_hdu.header.append(('NSUBOFFS', 0, 'Subint offset (Contiguous SEARCH-mode files)'))

    table_hdu.header.append(('NCHAN', fits.chnum, 'Number of channels/sub-bands in this file'))

    table_hdu.header.append(('CHAN_BW', float(fits.chanBW), '[MHz] Channel/sub-band width'))

    table_hdu.header.append(('DM', 0, '[cm-3 pc] DM for post-detection dedisperion'))
    table_hdu.header.append(('RM', 0, '[rad m-2] RM for post-detection deFaraday'))

    table_hdu.header.append(('NCHNOFFS', 0, 'Channel/sub-band offset for split files'))

    table_hdu.header.append(('NSBLK', dataformatnsblk, 'Samples/row (SEARCH mode, else 1)'))

    table_hdu.header.append(('EXTNAME', 'SUBINT  ', 'name of this binary table extension'))

    hdulist2 = pyfits.HDUList([fits.hdu0, table_hdu])

    hdulist2.writeto(outpath)
    print 'file' + outpath + '  write successfully'