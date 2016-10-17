/* Niema Moshiri 2016
 *
 * Perform various basic tasks on a list of numbers passed in via STDIN.
 *
 * Only pass in a single argument.
 */

// include statements
#include <cmath>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// usage message
const string USAGE_MESSAGE =
"\nUSAGE: numlist -ARG\n"
"    -add<NUM>:  Add <NUM> to all numbers\n"
"    -avg:       Compute average of list of numbers\n"
"    -csv:       Print the list as comma-separated values\n"
"    -div<NUM>:  Divide all numbers by <NUM>\n"
"    -dlm<STR>:  Print the list, but delimited by <STR>\n"
"    -gt<NUM>:   Print all numbers greater than <NUM>\n"
"    -gte<NUM>:  Print all numbers greater than or equal to <NUM>\n"
"    -int:       Print the list as integers\n"
"    -lt<NUM>:   Print all numbers less than <NUM>\n"
"    -lte<NUM>:  Print all numbers less than or equal to <NUM>\n"
"    -max:       Compute maximum of list of numbers\n"
"    -min:       Compute minimum of list of numbers\n"
"    -mult<NUM>: Multiply all numbers by <NUM>\n"
"    -pow<NUM>:  Raise all numbers to the power of <NUM>\n"
"    -sub<NUM>:  Subtract <NUM> from all numbers\n"
"    -sum:       Compute sum of list of numbers\n"
"    -tsv:       Print the list as tab-separated values\n";

// compute the sum of a list of numers
double sum( const vector<double> & nums ) {
    double out = 0;
    for(auto i : nums) {
        out += i;
    }
    return out;
}

// compute the average of a list of numbers
double avg( const vector<double> & nums ) {
    return sum(nums) / nums.size();
}

// delimit the numbers using delimiter
void dlm( const vector<double> & nums, const string & delimiter) {
    cout << nums[0];
    for(unsigned int i = 1; i < nums.size(); ++i) {
        cout << delimiter << nums[i];
    }
    cout << endl;
}

// print the list of numbers as comma-separated
void csv( const vector<double> & nums ) {
    dlm(nums,",");
}

// print the list of numbers as tab-separated
void tsv( const vector<double> & nums ) {
    dlm(nums,"\t");
}

// print the list of numbers as integers
void Int( const vector<double> & nums ) {
    for(auto i : nums) {
        cout << (int)i << endl;
    }
}

// find the max of a list of numbers
double max( const vector<double> & nums ) {
    double out = nums[0];
    for(auto i : nums) {
        if(i > out) {
            out = i;
        }
    }
    return out;
}

// find the min of a list of numbers
double min( const vector<double> & nums ) {
    double out = nums[0];
    for(auto i : nums) {
        if(i < out) {
            out = i;
        }
    }
    return out;
}

// output all numbers greater than the threshold
void gt( const vector<double> & nums, const double & thresh ) {
    for(auto i : nums) {
        if(i > thresh) {
            cout << i << endl;
        }
    }
}

// output all numbers greater than or equal to the threshold
void gte( const vector<double> & nums, const double & thresh ) {
    for(auto i : nums) {
        if(i >= thresh) {
            cout << i << endl;
        }
    }
}

// output all numbers less than the threshold
void lt( const vector<double> & nums, const double & thresh ) {
    for(auto i : nums) {
        if(i < thresh) {
            cout << i << endl;
        }
    }
}

// add num to all numbers
void add( const vector<double> & nums, const double & num ) {
    for(auto i : nums) {
        cout << i+num << endl;
    }
}

// subtract num from all numbers
void sub( const vector<double> & nums, const double & num ) {
    for(auto i : nums) {
        cout << i-num << endl;
    }
}

// divide all numbers by num
void div( const vector<double> & nums, const double & num ) {
    for(auto i : nums) {
        cout << i/num << endl;
    }
}

// multiply all numbers by num
void mult( const vector<double> & nums, const double & num ) {
    for(auto i : nums) {
        cout << i*num << endl;
    }
}

// output all numbers less than or equal to the threshold
void lte( const vector<double> & nums, const double & thresh ) {
    for(auto i : nums) {
        if(i <= thresh) {
            cout << i << endl;
        }
    }
}

// raise all numbers to the power of "exponent"
void power( const vector<double> & nums, const double & exponent ) {
    for(auto i : nums) {
        cout << pow(i,exponent) << endl;
    }
}

// replace all instances of "search" with "replace" in "subject"
void replace(string & subject, const string & search, const string & replace) {
    size_t pos = 0;
    while((pos = subject.find(search, pos)) != string::npos) {
         subject.replace(pos, search.length(), replace);
         pos += replace.length();
    }
}

// main function
int main( int argc, char* argv[] ) {
    // check arguments
    if(argc != 2) {
        cerr << "ERROR: Incorrect number of arguments" << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }

    // read in numbers
    vector<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    // perform task
    if(argv[1][1] == 'a' && argv[1][2] == 'd' && argv[1][3] == 'd') {
        add(nums,stod(((string)argv[1]).substr(4)));
    }
    else if(strcmp(argv[1],"-avg") == 0) {
        cout << avg(nums) << endl;
    }
    else if(strcmp(argv[1],"-csv") == 0) {
        csv(nums);
    }
    else if(argv[1][1] == 'd') {
        if(argv[1][2] == 'i' && argv[1][3] == 'v') {
            div(nums, stod(((string)argv[1]).substr(4)));
        }
        else if(argv[1][2] == 'l' && argv[1][3] == 'm') {
            string delimiter = argv[1];
            delimiter = delimiter.substr(4,delimiter.length()-4);
            replace(delimiter,"\\a","\a");
            replace(delimiter,"\\b","\b");
            replace(delimiter,"\\n","\n");
            replace(delimiter,"\\r","\r");
            replace(delimiter,"\\t","\t");
            dlm(nums,delimiter);
         }
    }
    else if(argv[1][1] == 'g' && argv[1][2] == 't') {
        if(argv[1][3] == 'e') {
            gte(nums, stod(((string)argv[1]).substr(4)));
        }
        else {
            gt(nums, stod(((string)argv[1]).substr(3)));
        }
    }
    else if(strcmp(argv[1],"-int") == 0) {
        Int(nums);
    }
    else if(argv[1][1] == 'l' && argv[1][2] == 't') {
        if(argv[1][3] == 'e') {
            lte(nums, stod(((string)argv[1]).substr(4)));
        }
        else {
            lt(nums, stod(((string)argv[1]).substr(3)));
        }
    }
    else if(strcmp(argv[1],"-max") == 0) {
        cout << max(nums) << endl;
    }
    else if(strcmp(argv[1],"-min") == 0) {
        cout << min(nums) << endl;
    }
    else if(argv[1][1] == 'm' && argv[1][2] == 'u' && argv[1][3] == 'l' && argv[1][4] == 't') {
        mult(nums, stod(((string)argv[1]).substr(5)));
    }
    else if(argv[1][1] == 'p' && argv[1][2] == 'o' && argv[1][3] == 'w') {
        power(nums,stod(((string)argv[1]).substr(4)));
    }
    else if(argv[1][1] == 's' && argv[1][2] == 'u' && argv[1][3] == 'b') {
        sub(nums,stod(((string)argv[1]).substr(4)));
    }
    else if(strcmp(argv[1],"-sum") == 0) {
        cout << sum(nums) << endl;
    }
    else if(strcmp(argv[1],"-tsv") == 0) {
        tsv(nums);
    }
    else {
        cerr << "ERROR: Invalid argument: " << argv[1] << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    return 0;
}