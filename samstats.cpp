/* Niema Moshiri 2020
 *
 * Compute basic statistics on a SAM file passed in via STDIN
 */

// include statements
#include <iostream>
#include <stdio.h>
#include <string.h>
using namespace std;

// useful constants
const int TAB = '\t';
const int NEWLINE = '\n';
const int AT = '@';
const string USAGE_MESSAGE = "USAGE: samstats [output_format]";

// main function
int main( int argc, char* argv[] ) {
    // check arguments
    if(argc > 2) {
        cerr << "ERROR: Incorrect number of arguments" << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(1);
    }
    unsigned char out_format = 255; // 0 = none, 1 = FASTQ, 2 = FASTA, 3 = SAM
    if(argc == 1) {
        out_format = 0;
    } else if(strcmp(argv[1],"-h") == 0 || strcmp(argv[1],"-help") == 0 || strcmp(argv[1],"--help") == 0) {
        cout << USAGE_MESSAGE << endl;
        exit(0);
    } else {
        string tmp = argv[1];
        for(char & c : tmp) {
            c = tolower(c);
        }
        if(tmp == "none") {
            out_format = 0;
        } else if(tmp == "fastq") {
            out_format = 1;
        } else if(tmp == "fasta") {
            out_format = 2;
        } else if(tmp == "sam") {
            out_format = 3;
        } else {
            cerr << "ERROR: Invalid output format: " << out_format << endl;
            cerr << "Valid options: none, fastq, fasta, sam" << endl;
            exit(1);
        }
    }

    // stats to compute
    unsigned long long num_bases = 0;   // number of bases
    unsigned long long num_headers = 0; // number of header lines
    unsigned long long num_reads = 0;   // number of reads

    // parse SAM from stdin
    int c;                           // current character of file
    unsigned long long col = 1;      // column number (1-based indexing)
    unsigned long long col_pos = 0;  // position in the current column (1-based indexing)
    unsigned long long line_num = 1; // line number (1-based indexing)
    bool header = true;
    while((c = getchar_unlocked()) != EOF) {
        // if outputting SAM as well, just print this character
        if(out_format == 3) {
            cout << (char)c;
        }

        // newline, so increment line number and reset things
        if(c == NEWLINE) {
            ++line_num;
            col = 1;
            col_pos = 0;
            if(!header && out_format != 0 && out_format != 3) {
                cout << '\n';
            }
            continue;
        }

        // tab, so increment column
        else if(c == TAB) {
            ++col;
            col_pos = 0;
            continue;
        }

        // increment column position number
        ++col_pos;

        // 1st column (ID)
        if(col == 1) {
            // start of line
            if(col_pos == 1) {
                // start of header line
                if(c == AT) {
                    ++num_headers;
                }

                // start of non-header line
                else {
                    header = false;

                    // print ID start symbol if needed (> for FASTA, @ for FASTQ)
                    if(col_pos == 1) {
                        ++num_reads;
                        if(out_format == 1)  {       // FASTQ
                            cout << '@';
                        } else if(out_format == 2) { // FASTA
                            cout << '>';
                        }
                    }
                }
            }

            // output this character as part of the ID
            if(!header && (out_format == 1 || out_format == 2)) {
                cout << (char)c;
            }
        }

        // 10th column (sequence)
        else if(col == 10) {
            ++num_bases;

            // print nucleotide if FASTQ or FASTA
            if(out_format == 1 || out_format == 2) {
                if(col_pos == 1) {
                    cout << '\n';
                }
                cout << (char)c;
            }
        }

        // 11th column (quality)
        else if(col == 11) {
            // print qual if FASTQ
            if(out_format == 1) {
                if(col_pos == 1) {
                    cout << '\n' << '+' << '\n';
                }
                cout << (char)c;
            }
        }
    }
    cerr << "Number of Header Lines: " << num_headers << endl;
    cerr << "Number of Bases: " << num_bases << endl;
    cerr << "Number of Reads: " << num_reads << endl;
    cerr << "Average Read Length: " << (((long double)num_bases)/num_reads) << endl;
    return 0;
}
