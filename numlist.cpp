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
#include <stdlib.h>
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
"    -h:         Print this help message\n"
"    -help:      Print this help message\n"
"    -int:       Print the list as integers\n"
"    -lt<NUM>:   Print all numbers less than <NUM>\n"
"    -lte<NUM>:  Print all numbers less than or equal to <NUM>\n"
"    -max:       Compute maximum of list of numbers\n"
"    -med:       Compute median of list of numbers\n"
"    -min:       Compute minimum of list of numbers\n"
"    -mult<NUM>: Multiply all numbers by <NUM>\n"
"    -pow<NUM>:  Raise all numbers to the power of <NUM>\n"
"    -q1:        Compute first quartile of list of numbers\n"
"    -q3:        Compute third quartile of list of numbers\n"
"    -sortA:     Print the list in ascending order\n"
"    -sortD:     Print the list in descending order\n"
"    -stats:     Compute various statistics on list of numbers\n"
"    -std:       Compute standard deviation of list of numbers\n"
"    -sub<NUM>:  Subtract <NUM> from all numbers\n"
"    -sum:       Compute sum of list of numbers\n"
"    -tsv:       Print the list as tab-separated values\n"
"    -var:       Compute variance of list of numbers\n";

// compute the sum of a list of numers
double sum( const vector<double> & nums ) {
    double out = 0.0;
    for(unsigned int i = 0; i < nums.size(); ++i) {
        out += nums[i];
    }
    return out;
}

// compute the average of a list of numbers
double avg( const vector<double> & nums ) {
    return sum(nums) / nums.size();
}

// compute the variance of a list of numbers
double var( const vector<double> & nums ) {
    double s = 0.0;
    double ss = 0.0;
    for(unsigned int i = 0; i < nums.size(); ++i) {
        s += nums[i];
        ss += nums[i]*nums[i];
    }
    double mean = s / nums.size();
    return ss/nums.size() - mean*mean;
}

// compute the standard deviation of a list of numbers
double stdev( const vector<double> & nums ) {
    return pow(var(nums),0.5);
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
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << (int)nums[i] << endl;
    }
}

// find the max of a list of numbers
double max( const vector<double> & nums ) {
    double out = nums[0];
    for(unsigned int i = 0; i < nums.size(); ++i) {
        if(nums[i] > out) {
            out = nums[i];
        }
    }
    return out;
}

// find the min of a list of numbers
double min( const vector<double> & nums ) {
    double out = nums[0];
    for(unsigned int i = 0; i < nums.size(); ++i) {
        if(nums[i] < out) {
            out = nums[i];
        }
    }
    return out;
}

// find the median of a list of numbers
double med( vector<double> & nums ) {
    // sort list
    sort(nums.begin(),nums.end());

    // odd number of elements, so return middle element
    if(nums.size() % 2 == 1) {
        return nums[nums.size()/2];
    }

    // even number of elements, so return avg of middle elements
    else {
        unsigned int mid = nums.size()/2;
        return (nums[mid] + nums[mid-1]) / 2;
    }
}

// find the first quartile of a list of numbers
double q1( vector<double> & nums ) {
    // sort list
    sort(nums.begin(),nums.end());

    // find first quartile
    unsigned int mid = nums.size()/2;
    unsigned int q1 = mid/2;
    if(nums.size() % 2 == 1) {
        if(mid % 2 == 1) {
            return nums[q1];
        }
        else {
            return (nums[q1] + nums[q1-1]) / 2;
        }
    }
    else {
        if(mid % 2 == 1) {
            return nums[q1];
        }
        else {
            return (nums[q1] + nums[q1-1]) / 2;
        }
    }
}

// find the third quartile of a list of numbers
double q3( vector<double> & nums ) {
    // sort list
    sort(nums.begin(),nums.end());

    // find first quartile
    unsigned int mid = nums.size()/2;
    unsigned int q3 = mid + mid/2;
    if(nums.size() % 2 == 1) {
        if(mid % 2 == 1) {
            return nums[q3+1];
        }
        else {
            return (nums[q3] + nums[q3+1]) / 2;
        }
    }
    else {
        if(mid % 2 == 1) {
            return nums[q3];
        }
        else {
            return (nums[q3] + nums[q3-1]) / 2;
        }
    }
}

// output all numbers greater than the threshold
void gt( const vector<double> & nums, const double & thresh ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        if(nums[i] > thresh) {
            cout << nums[i] << endl;
        }
    }
}

// output all numbers greater than or equal to the threshold
void gte( const vector<double> & nums, const double & thresh ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        if(nums[i] >= thresh) {
            cout << nums[i] << endl;
        }
    }
}

// output all numbers less than the threshold
void lt( const vector<double> & nums, const double & thresh ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        if(nums[i] < thresh) {
            cout << nums[i] << endl;
        }
    }
}

// add num to all numbers
void add( const vector<double> & nums, const double & num ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << nums[i]+num << endl;
    }
}

// subtract num from all numbers
void sub( const vector<double> & nums, const double & num ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << nums[i]-num << endl;
    }
}

// divide all numbers by num
void div( const vector<double> & nums, const double & num ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << nums[i]/num << endl;
    }
}

// multiply all numbers by num
void mult( const vector<double> & nums, const double & num ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << nums[i]*num << endl;
    }
}

// output all numbers less than or equal to the threshold
void lte( const vector<double> & nums, const double & thresh ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        if(nums[i] <= thresh) {
            cout << nums[i] << endl;
        }
    }
}

// raise all numbers to the power of "exponent"
void power( const vector<double> & nums, const double & exponent ) {
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << pow(nums[i],exponent) << endl;
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

// print list in ascending order
void sortA( vector<double> & nums ) {
    sort(nums.begin(),nums.end());
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << nums[i] << endl;
    }
}

// print list in descending order
void sortD( vector<double> & nums ) {
    sort(nums.rbegin(), nums.rend());
    for(unsigned int i = 0; i < nums.size(); ++i) {
        cout << nums[i] << endl;
    }
}

// compute various stats on list of numbers
void stats( vector<double> & nums ) {
    // sort list
    sort(nums.begin(),nums.end());

    // compute stats
    double s = 0.0;
    double ss = 0.0;
    double outMax = nums[0];
    double outMin = nums[0];
    for(unsigned int i = 0; i < nums.size(); ++i) {
        s += nums[i];
        ss += nums[i]*nums[i];
        if(nums[i] > outMax) {
            outMax = nums[i];
        }
        if(nums[i] < outMin) {
            outMin = nums[i];
        }
    }
    double outMean = s / nums.size();
    double outVar = ss/nums.size() - outMean*outMean;
    double outMed;
    double outQ1;
    double outQ3;
    unsigned int mid = nums.size()/2;
    unsigned int q1 = mid/2;
    unsigned int q3 = mid + q1;
    if(nums.size() % 2 == 1) {
        outMed = nums[mid];
        if(mid % 2 == 1) {
            outQ1 = nums[q1];
            outQ3 = nums[q3+1];
        }
        else {
            outQ1 = (nums[q1] + nums[q1-1]) / 2;
            outQ3 = (nums[q3] + nums[q3+1]) / 2;
        }
    }
    else {
        outMed = (nums[mid] + nums[mid-1]) / 2;
        if(mid % 2 == 1) {
            outQ1 = nums[q1];
            outQ3 = nums[q3];
        }
        else {
            outQ1 = (nums[q1] + nums[q1-1]) / 2;
            outQ3 = (nums[q3] + nums[q3-1]) / 2;
        }
    }

    // output results
    cout << "minimum:   " << outMin << endl;
    cout << "quartile1: " << outQ1 << endl;
    cout << "median:    " << outMed << endl;
    cout << "quartile3: " << outQ3 << endl;
    cout << "maximum:   " << outMax << endl;
    cout << "average:   " << outMean << endl;
    cout << "variance:  " << outVar << endl;
    cout << "stdev:     " << pow(outVar,0.5) << endl;
}

// main function
int main( int argc, char* argv[] ) {
    // check arguments
    if(argc != 2) {
        cerr << "ERROR: Incorrect number of arguments" << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    else if(strcmp(argv[1],"-h") == 0 or strcmp(argv[1],"-help") == 0) {
        cout << USAGE_MESSAGE << endl;
        exit(0);
    }

    // read in numbers
    vector<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    // perform task
    if(argv[1][1] == 'a' && argv[1][2] == 'd' && argv[1][3] == 'd') {
        add(nums,strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
    }
    else if(strcmp(argv[1],"-avg") == 0) {
        cout << avg(nums) << endl;
    }
    else if(strcmp(argv[1],"-csv") == 0) {
        csv(nums);
    }
    else if(argv[1][1] == 'd') {
        if(argv[1][2] == 'i' && argv[1][3] == 'v') {
            div(nums, strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
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
         else {
             cerr << "ERROR: Invalid argument: " << argv[1] << endl;
             cerr << USAGE_MESSAGE << endl;
             exit(-1);
         }
    }
    else if(argv[1][1] == 'g' && argv[1][2] == 't') {
        if(argv[1][3] == 'e') {
            gte(nums, strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
        }
        else {
            gt(nums, strtod(((string)argv[1]).substr(3).c_str(),(char**)0));
        }
    }
    else if(strcmp(argv[1],"-int") == 0) {
        Int(nums);
    }
    else if(argv[1][1] == 'l' && argv[1][2] == 't') {
        if(argv[1][3] == 'e') {
            lte(nums, strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
        }
        else {
            lt(nums, strtod(((string)argv[1]).substr(3).c_str(),(char**)0));
        }
    }
    else if(strcmp(argv[1],"-max") == 0) {
        cout << max(nums) << endl;
    }
    else if(strcmp(argv[1],"-med") == 0) {
        cout << med(nums) << endl;
    }
    else if(strcmp(argv[1],"-min") == 0) {
        cout << min(nums) << endl;
    }
    else if(argv[1][1] == 'm' && argv[1][2] == 'u' && argv[1][3] == 'l' && argv[1][4] == 't') {
        mult(nums, strtod(((string)argv[1]).substr(5).c_str(),(char**)0));
    }
    else if(argv[1][1] == 'p' && argv[1][2] == 'o' && argv[1][3] == 'w') {
        power(nums,strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
    }
    else if(strcmp(argv[1],"-q1") == 0) {
        cout << q1(nums) << endl;
    }
    else if(strcmp(argv[1],"-q3") == 0) {
        cout << q3(nums) << endl;
    }
    else if(argv[1][1] == 's' && argv[1][2] == 'u' && argv[1][3] == 'b') {
        sub(nums,strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
    }
    else if(strcmp(argv[1],"-sortA") == 0) {
        sortA(nums);
    }
    else if(strcmp(argv[1],"-sortD") == 0) {
        sortD(nums);
    }
    else if(strcmp(argv[1],"-stats") == 0) {
        stats(nums);
    }
    else if(strcmp(argv[1],"-std") == 0) {
        cout << stdev(nums) << endl;
    }
    else if(strcmp(argv[1],"-sum") == 0) {
        cout << sum(nums) << endl;
    }
    else if(strcmp(argv[1],"-tsv") == 0) {
        tsv(nums);
    }
    else if(strcmp(argv[1],"-var") == 0) {
        cout << var(nums) << endl;
    }
    else {
        cerr << "ERROR: Invalid argument: " << argv[1] << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    return 0;
}
