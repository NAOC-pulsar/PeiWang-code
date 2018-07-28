# FASTFitsMerge

Usage: ./FASTFitsMerge [options] source_dir dest_dir
FAST Fits Extract and Merge program handle the initial fits files and produce new fits files.

Options:
  -h, --help                    Displays this help.
  -v, --version                 Displays version information.
  -f, --force-drifting          Treat all tracking files as drifting by force.
  -d, --drifting                Extract and merge drifting files.
  -t, --tracking                Extract and merge all tracking files.
  -p, --polar-no <number>       Only extract data that contains polorization
                                <number>. The default value is 1.
  -b, --end-ch-freq <number>    Only extract data that channel frequence >=
                                <number>. The default value is 290.0.
  -e, --begin-ch-freq <number>  Only extract data that channel frequence <=
                                <number>. The default value is 802.0.
  -c, --files-count <number>    Every <number> files will be squencely merged
                                to a file. The default value is 2.

Arguments:
  source_dir                    Source directory that contains initial fits
                                files.
  dest_dir                      Destination directory.

