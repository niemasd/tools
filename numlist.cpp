/* Niema Moshiri 2016
 *
 * Perform various basic tasks on a list of numbers passed in via STDIN.
 *
 * Only pass in a single argument.
 */

// include statements
#include <algorithm>
#include <cmath>
#include <cstring>
#include <iostream>
#include <list>
#include <stdlib.h>
#include <string>
#include <vector>
using namespace std;

// usage message
const string USAGE_MESSAGE =
"\nUSAGE: numlist -ARG\n"
"    -abs           Compute the absolute value of each number"
"    -add<NUM>      Add <NUM> to each number\n"
"    -avg           Compute the average of the list\n"
"    -csv           Print the list as comma-separated values\n"
"    -div<NUM>      Divide each number by <NUM>\n"
"    -dlm<STR>      Print the list, but delimited by <STR>\n"
"    -gt<NUM>       Print all numbers greater than <NUM>\n"
"    -gte<NUM>      Print all numbers greater than or equal to <NUM>\n"
"    -h             Print this help message\n"
"    -help          Print this help message\n"
"    -int           Cast each number as an integer\n"
"    -len           Print the length of the list\n"
"    -ln            Take the natural log of each number\n"
"    -log<NUM>      Take the log base-<NUM> of each number\n"
"    -lt<NUM>       Print all numbers less than <NUM>\n"
"    -lte<NUM>      Print all numbers less than or equal to <NUM>\n"
"    -max           Compute the maximum of the list\n"
"    -med           Compute the median of the list\n"
"    -min           Compute the minimum of the list\n"
"    -mul<NUM>      Multiply each number by <NUM>\n"
"    -neg           Multiply each number by -1\n"
"    -pow<NUM>      Raise each number to the power of <NUM>\n"
"    -quant<NUM>    Compute the <NUM>th quantile of the list (0 <= <NUM> <= 1)\n"
"    -quart1        Compute the first quartile of the list\n"
"    -quart3        Compute the third quartile of the list\n"
"    -recip         Compute the reciprocal of each number\n"
"    -rev           Reverse the list\n"
"    -sort          Print the list in ascending order\n"
"    -sortA         Print the list in ascending order\n"
"    -sortD         Print the list in descending order\n"
"    -sqrt          Compute the square root of each number\n"
"    -stats         Compute various statistics on the list\n"
"    -std           Compute the standard deviation of the list\n"
"    -sub<NUM>      Subtract <NUM> from each number\n"
"    -sum           Compute the sum of the list\n"
"    -tsv           Print the list as tab-separated values\n"
"    -var           Compute the variance of the list\n";

// compute the sum of a list of numers
double sum() {
    double out = 0.0;
    double num;
    while(cin >> num) {
        out += num;
    }
    return out;
}

// compute the length of a list of numbers
double len() {
    unsigned int n = 0;
    double num;
    while(cin >> num) {
        ++n;
    }
    return n;
}

// compute the average of a list of numbers
double avg() {
    double out = 0.0;
    unsigned int n = 0;
    double num;
    while(cin >> num) {
        out += num;
        ++n;
    }
    return (out/n);
}

// compute the variance of a list of numbers
double var() {
    double s = 0.0;
    double ss = 0.0;
    unsigned int n = 0;
    double num;
    while(cin >> num) {
        s += num;
        ss += num*num;
        ++n;
    }
    double mean = s/n;
    return ss/n - mean*mean;
}

// compute the standard deviation of a list of numbers
double stdev() {
    return pow(var(),0.5);
}

// delimit the numbers using delimiter
void dlm( const string & delimiter ) {
    double num;
    if(cin >> num) {
        cout << num;
    }
    else {
        return;
    }
    while(cin >> num) {
        cout << delimiter << num;
    }
    cout << endl;
}

// print the list of numbers as integers
void Int() {
    double num;
    while(cin >> num) {
        cout << (int)num << endl;
    }
}

// find the max of a list of numbers
double max() {
    double out;
    double num;
    if(cin >> num) {
        out = num;
    }
    else {
        cerr << "ERROR: Can't find max of empty list" << endl;
        exit(-1);
    }
    while(cin >> num) {
        if(num > out) {
            out = num;
        }
    }
    return out;
}

// find the min of a list of numbers
double min() {
    double out;
    double num;
    if(cin >> num) {
        out = num;
    }
    else {
        cerr << "ERROR: Can't find min of empty list" << endl;
        exit(-1);
    }
    while(cin >> num) {
        if(num < out) {
            out = num;
        }
    }
    return out;
}

// find the median of a list of numbers
double med() {
    // read in numbers
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    // sort list
    unsigned int n = nums.size();
    vector<double> numsVec(n,0);
    unsigned int i = 0;
    for(list<double>::const_iterator it = nums.begin(), end = nums.end(); it != end; ++it, ++i) {
        numsVec[i] = *it;
    }
    sort(numsVec.begin(),numsVec.end());

    // odd number of elements, so return middle element
    if(n%2 == 1) {
        return numsVec[n/2];
    }

    // even number of elements, so return avg of middle elements
    else {
        unsigned int mid = n/2;
        return (numsVec[mid] + numsVec[mid-1]) / 2;
    }
}

// find the first quartile of a list of numbers
double q1() {
    // read in numbers
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    // sort list
    unsigned int n = nums.size();
    vector<double> numsVec(n,0);
    unsigned int i = 0;
    for(list<double>::const_iterator it = nums.begin(), end = nums.end(); it != end; ++it, ++i) {
        numsVec[i] = *it;
    }
    sort(numsVec.begin(),numsVec.end());

    // find first quartile
    unsigned int mid = n/2;
    unsigned int q1 = mid/2;
    if(n%2 == 1) {
        if(mid%2 == 1) {
            return numsVec[q1];
        }
        else {
            return (numsVec[q1] + numsVec[q1-1]) / 2;
        }
    }
    else {
        if(mid%2 == 1) {
            return numsVec[q1];
        }
        else {
            return (numsVec[q1] + numsVec[q1-1]) / 2;
        }
    }
}

// find the third quartile of a list of numbers
double q3() {
    // read in numbers
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    // sort list
    unsigned int n = nums.size();
    vector<double> numsVec(n,0);
    unsigned int i = 0;
    for(list<double>::const_iterator it = nums.begin(), end = nums.end(); it != end; ++it, ++i) {
        numsVec[i] = *it;
    }
    sort(numsVec.begin(),numsVec.end());

    // find first quartile
    unsigned int mid = n/2;
    unsigned int q3 = mid + mid/2;
    if(n%2 == 1) {
        if(mid%2 == 1) {
            return numsVec[q3+1];
        }
        else {
            return (numsVec[q3] + numsVec[q3+1]) / 2;
        }
    }
    else {
        if(mid%2 == 1) {
            return numsVec[q3];
        }
        else {
            return (numsVec[q3] + numsVec[q3-1]) / 2;
        }
    }
}

// compute the q-th quantile of list of numbers
double Lerp(double v0, double v1, double t)
{
    return (1 - t)*v0 + t*v1;
}
double quant( const float & q ) {
    // check for validity of q
    if(q < 0 || q > 1) {
        cerr << "ERROR: <NUM> must be between 0 and 1" << endl;
        exit(-1);
    }

    // read in numbers
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    // check for validity of list
    if(nums.size() <= 2)
    {
        cerr << "ERROR: Can't compute quantiles on a list of numbers with less than 2 elements." << endl;
        exit(-1);
    }

    // sort list
    unsigned int n = nums.size();
    vector<double> numsVec(n,0);
    unsigned int i = 0;
    for(list<double>::const_iterator it = nums.begin(), end = nums.end(); it != end; ++it, ++i) {
        numsVec[i] = *it;
    }
    sort(numsVec.begin(),numsVec.end());

    // compute quantile
    double center = Lerp(-0.5, numsVec.size() - 0.5, q);
    size_t left = std::max(int64_t(std::floor(center)), int64_t(0));
    size_t right = std::min(int64_t(std::ceil(center)), int64_t(numsVec.size() - 1));
    double datLeft = numsVec.at(left);
    double datRight = numsVec.at(right);
    return Lerp(datLeft, datRight, center - left);
}

// output all numbers greater than the threshold
void gt( const double & thresh ) {
    double num;
    while(cin >> num) {
        if(num > thresh) {
            cout << num << endl;
        }
    }
}

// output all numbers greater than or equal to the threshold
void gte( const double & thresh ) {
    double num;
    while(cin >> num) {
        if(num >= thresh) {
            cout << num << endl;
        }
    }
}

// output all numbers less than the threshold
void lt( const double & thresh ) {
    double num;
    while(cin >> num) {
        if(num < thresh) {
            cout << num << endl;
        }
    }
}

// output all numbers less than or equal to the threshold
void lte( const double & thresh ) {
    double num;
    while(cin >> num) {
        if(num <= thresh) {
            cout << num << endl;
        }
    }
}

// add num to all numbers
void add( const double & i ) {
    double num;
    while(cin >> num) {
        cout << num+i << endl;
    }
}

// subtract num from all numbers
void sub( const double & i ) {
    double num;
    while(cin >> num) {
        cout << num-i << endl;
    }
}

// divide all numbers by num
void div( const double & i ) {
    double num;
    while(cin >> num) {
        cout << num/i << endl;
    }
}

// multiply all numbers by num
void mult( const double & i ) {
    double num;
    while(cin >> num) {
        cout << num*i << endl;
    }
}

// compute the reciprocal of each number
void reciprocal() {
    double num;
    while(cin >> num) {
        cout << 1.0/num << endl;
    }
}

// compute the absolute value of each number
void abs() {
    double num;
    while(cin >> num) {
        if(num == 0) { // change -0 to 0
            num = 0;
        }
        else if(num < 0) {
            num *= -1;
        }
        cout << num << endl;
    }
}

// raise all numbers to the power of "exponent"
void power( const double & exponent ) {
    double num;
    while(cin >> num) {
        cout << pow(num,exponent) << endl;
    }
}

// take the natural log of each number
void ln() {
    double num;
    while(cin >> num) {
        cout << log(num) << endl;
    }
}

// take the log base "base" of each number
void Log( const double & base) {
    const double convert = log10(base);
    double num;
    while(cin >> num) {
        cout << log10(num)/convert << endl;
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

// reverse the list of numbers
void reverse() {
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }
    for(list<double>::const_iterator it = nums.end(), beg = nums.begin(); it != beg;) {
        --it; cout << *it << endl;
    }
}

// print list in ascending order
void sortA() {
    // read in numbers
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    unsigned int n = nums.size();
    vector<double> numsVec(n,0);
    unsigned int i = 0;
    for(list<double>::const_iterator it = nums.begin(), end = nums.end(); it != end; ++it, ++i) {
        numsVec[i] = *it;
    }
    sort(numsVec.begin(),numsVec.end());
    for(unsigned int i = 0; i < n; ++i) {
        cout << numsVec[i] << endl;
    }
}

// print list in descending order
void sortD() {
    // read in numbers
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    unsigned int n = nums.size();
    vector<double> numsVec(n,0);
    unsigned int i = 0;
    for(list<double>::const_iterator it = nums.begin(), end = nums.end(); it != end; ++it, ++i) {
        numsVec[i] = *it;
    }
    sort(numsVec.rbegin(),numsVec.rend());
    for(unsigned int i = 0; i < n; ++i) {
        cout << numsVec[i] << endl;
    }
}

// compute various stats on list of numbers
void stats() {
    // read in numbers
    list<double> nums;
    double num;
    while(cin >> num) {
        nums.push_back(num);
    }

    // sort list
    unsigned int n = nums.size();
    vector<double> numsVec(n,0);
    unsigned int i = 0;
    for(list<double>::const_iterator it = nums.begin(), end = nums.end(); it != end; ++it, ++i) {
        numsVec[i] = *it;
    }
    sort(numsVec.begin(),numsVec.end());

    // compute stats
    double s = 0.0;
    double ss = 0.0;
    double outMax = numsVec[0];
    double outMin = numsVec[0];
    cerr << "sorted list: " << numsVec[0];
    for(unsigned int i = 0; i < n; ++i) {
        double num = numsVec[i];
        if(i != 0) {
            cerr << "," << num;
        }
        s += num;
        ss += num*num;
        if(num > outMax) {
            outMax = num;
        }
        if(num < outMin) {
            outMin = num;
        }
    }
    cout << endl << endl;
    double outMean = s/n;
    double outVar = ss/n - outMean*outMean;
    double outMed;
    double outQ1;
    double outQ3;
    unsigned int mid = n/2;
    unsigned int q1 = mid/2;
    unsigned int q3 = mid + q1;
    if(n % 2 == 1) {
        outMed = numsVec[mid];
        if(mid % 2 == 1) {
            outQ1 = numsVec[q1];
            outQ3 = numsVec[q3+1];
        }
        else {
            outQ1 = (numsVec[q1] + numsVec[q1-1]) / 2;
            outQ3 = (numsVec[q3] + numsVec[q3+1]) / 2;
        }
    }
    else {
        outMed = (numsVec[mid] + numsVec[mid-1]) / 2;
        if(mid % 2 == 1) {
            outQ1 = numsVec[q1];
            outQ3 = numsVec[q3];
        }
        else {
            outQ1 = (numsVec[q1] + numsVec[q1-1]) / 2;
            outQ3 = (numsVec[q3] + numsVec[q3-1]) / 2;
        }
    }

    // output results
    cout << "minimum:   " << outMin << endl;
    cout << "quartile1: " << outQ1 << endl;
    cout << "median:    " << outMed << endl;
    cout << "quartile3: " << outQ3 << endl;
    cout << "maximum:   " << outMax << endl << endl;

    cout << "length:    " << nums.size() << endl;
    cout << "sum:       " << s << endl;
    cout << "average:   " << outMean << endl;
    cout << "variance:  " << outVar << endl;
    cout << "stdev:     " << pow(outVar,0.5) << endl;
}

// check argument string for valid number (arg = argv[1], l = length of stuff before number)
double check_num( const string & arg, const unsigned int & l ) {
    if(arg.length() == l) {
        cerr << "ERROR: No number specified" << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    string numstr = arg.substr(l).c_str();
    char* p;
    double num = strtod(numstr.c_str(), &p);
    if(*p) {
        cerr << "ERROR: Invalid number specified: " << arg.substr(l).c_str() << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    else {
        return num;
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
    else if(strcmp(argv[1],"-h") == 0 || strcmp(argv[1],"-help") == 0 || strcmp(argv[1],"--help") == 0) {
        cout << USAGE_MESSAGE << endl;
        exit(0);
    }

    // perform task
    if(strcmp(argv[1],"-abs") == 0) {
        abs();
    }

    else if(argv[1][1] == 'a' && argv[1][2] == 'd' && argv[1][3] == 'd') {
        check_num(argv[1],4);
        add(strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
    }
    else if(strcmp(argv[1],"-avg") == 0) {
        cout << avg() << endl;
    }
    else if(strcmp(argv[1],"-csv") == 0) {
        dlm(",");
    }
    else if(argv[1][1] == 'd') {
        if(argv[1][2] == 'i' && argv[1][3] == 'v') {
            div(check_num(argv[1],4));
        }
        else if(argv[1][2] == 'l' && argv[1][3] == 'm') {
            string delimiter = argv[1];
            delimiter = delimiter.substr(4,delimiter.length()-4);
            replace(delimiter,"\\a","\a");
            replace(delimiter,"\\b","\b");
            replace(delimiter,"\\n","\n");
            replace(delimiter,"\\r","\r");
            replace(delimiter,"\\t","\t");
            dlm(delimiter);
         }
         else {
             cerr << "ERROR: Invalid argument: " << argv[1] << endl;
             cerr << USAGE_MESSAGE << endl;
             exit(-1);
         }
    }
    else if(argv[1][1] == 'g' && argv[1][2] == 't') {
        if(argv[1][3] == 'e') {
            gte(check_num(argv[1],4));
        }
        else {
            gt(check_num(argv[1],3));
        }
    }
    else if(strcmp(argv[1],"-int") == 0) {
        Int();
    }
    else if(strcmp(argv[1],"-len") == 0) {
        cout << len() << endl;
    }
    else if(strcmp(argv[1],"-ln") == 0) {
        ln();
    }
    else if(argv[1][1] == 'l') {
        if(argv[1][2] == 'o' && argv[1][3] == 'g') {
            Log(check_num(argv[1],4));
        }
        else if(argv[1][2] == 't') {
            if(argv[1][3] == 'e') {
                lte(check_num(argv[1],4));
            }
            else {
                lt(check_num(argv[1],3));
            }
        }
        else {
            cerr << "ERROR: Invalid argument: " << argv[1] << endl;
            cerr << USAGE_MESSAGE << endl;
            exit(-1);
        }
    }
    else if(strcmp(argv[1],"-max") == 0) {
        cout << max() << endl;
    }
    else if(strcmp(argv[1],"-med") == 0) {
        cout << med() << endl;
    }
    else if(strcmp(argv[1],"-min") == 0) {
        cout << min() << endl;
    }
    else if(argv[1][1] == 'm' && argv[1][2] == 'u' && argv[1][3] == 'l') {
        mult(check_num(argv[1],4));
    }
    else if(strcmp(argv[1],"-neg") == 0) {
        mult(-1);
    }
    else if(argv[1][1] == 'p' && argv[1][2] == 'o' && argv[1][3] == 'w') {
        power(check_num(argv[1],4));
    }
    else if(argv[1][1] == 'q' && argv[1][2] == 'u' && argv[1][3] == 'a' && argv[1][4] == 'n' && argv[1][5] == 't') {
        cout << quant(check_num(argv[1],6)) << endl;
    }
    else if(strcmp(argv[1],"-quart1") == 0) {
        cout << q1() << endl;
    }
    else if(strcmp(argv[1],"-quart3") == 0) {
        cout << q3() << endl;
    }
    else if(strcmp(argv[1],"-recip") == 0) {
        reciprocal();
    }
    else if(strcmp(argv[1],"-rev") == 0) {
        reverse();
    }
    else if(argv[1][1] == 's' && argv[1][2] == 'u' && argv[1][3] == 'b') {
        sub(check_num(argv[1],4));
    }
    else if(strcmp(argv[1],"-sortA") == 0 || strcmp(argv[1],"-sort") == 0) {
        sortA();
    }
    else if(strcmp(argv[1],"-sortD") == 0) {
        sortD();
    }
    else if(strcmp(argv[1],"-sqrt") == 0) {
        power(0.5);
    }
    else if(strcmp(argv[1],"-stats") == 0) {
        stats();
    }
    else if(strcmp(argv[1],"-std") == 0) {
        cout << stdev() << endl;
    }
    else if(strcmp(argv[1],"-sum") == 0) {
        cout << sum() << endl;
    }
    else if(strcmp(argv[1],"-tsv") == 0) {
        dlm("\t");
    }
    else if(strcmp(argv[1],"-var") == 0) {
        cout << var() << endl;
    }
    else {
        cerr << "ERROR: Invalid argument: " << argv[1] << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    return 0;
}
