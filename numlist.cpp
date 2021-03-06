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
#include <limits>
#include <list>
#include <sstream>
#include <stdlib.h>
#include <string>
#include <vector>
using namespace std;

// usage message
const string USAGE_MESSAGE =
"\nUSAGE: numlist -ARG\n"
"    -abs           Compute the absolute value of each number\n"
"    -add<NUM>      Add <NUM> to each number\n"
"    -avg           Compute the average of the list\n"
"    -ceil          Compute the ceiling of each number\n"
"    -cma           Compute the cumulative moving average of the list\n"
"    -csv           Print the list as comma-separated values\n"
"    -div<NUM>      Divide each number by <NUM>\n"
"    -dlm<STR>      Print the list, but delimited by <STR>\n"
"    -exp           Compute e to the power of each number\n"
"    -fact          Compute the factorial of each number\n"
"    -floor         Compute the floor of each number\n"
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
"    -mod<NUM>      Mod each number by <NUM>\n"
"    -mul<NUM>      Multiply each number by <NUM>\n"
"    -nCk           For each line of '<n> <k>' input, compute nCk\n"
"    -neg           Multiply each number by -1\n"
"    -nPk           For each line of '<n> <k>' input, compute nPk\n"
"    -pow<NUM>      Raise each number to the power of <NUM>\n"
"    -prod          Compute the product of the list\n"
"    -quant<NUM>    Compute the <NUM>th quantile of the list (0 <= <NUM> <= 1)\n"
"    -quart1        Compute the first quartile of the list\n"
"    -quart3        Compute the third quartile of the list\n"
"    -rand          Generate a single random number from the uniform distribution between 0 and 1\n"
"    -rand<NUM>     Generate <NUM> random numbers from the uniform distribution between 0 and 1\n"
"    -recip         Compute the reciprocal of each number\n"
"    -rev           Reverse the list\n"
"    -sort          Print the list in ascending order\n"
"    -sortA         Print the list in ascending order\n"
"    -sortD         Print the list in descending order\n"
"    -sorted        Print 1 if the list is sorted in ascending order, otherwise 0\n"
"    -sortedA       Print 1 if the list is sorted in ascending order, otherwise 0\n"
"    -sortedD       Print 1 if the list is sorted in descending order, otherwise 0\n"
"    -sqrt          Compute the square root of each number\n"
"    -stats         Compute various statistics on the list\n"
"    -std           Compute the standard deviation of the list\n"
"    -sub<NUM>      Subtract <NUM> from each number\n"
"    -sum           Compute the sum of the list\n"
"    -tsv           Print the list as tab-separated values\n"
"    -var           Compute the variance of the list\n";

// compute the sum of a list of numbers
double sum() {
    double out = 0.0;
    double num;
    while(cin >> num) {
        out += num;
    }
    return out;
}

// compute the product of a list of numbers
double prod() {
    double out = 1.0;
    double num;
    while(cin >> num) {
        out *= num;
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

// take the ceiling of all numbers
void ceil() {
    double num;
    while(cin >> num) {
        cout << ceil(num) << endl;
    }
}

// take the floor of all numbers
void floor() {
    double num;
    while(cin >> num) {
        cout << floor(num) << endl;
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

// mod all numbers by num
void mod( const int & i ) {
    int num;
    while(cin >> num) {
        cout << num%i << endl;
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

// compute the cumulative moving average of the list
void cma() {
    double num; double tot = 0; int n = 0;
    while(cin >> num) {
        tot += num; ++n; cout << (tot/n) << endl;
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

// raise e to the power of each number
void Exp() {
    double num;
    while(cin >> num) {
        cout << exp(num) << endl;
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

// compute the factorial of each number
void fact() {
    double num;
    while(cin >> num) {
        if(num < 0) {
            cerr << "ERROR: Cannot compute the factorial of a negative number: " << num << endl;
            exit(-1);
        }
        unsigned long f = 1;
        for(unsigned long i = 2; i <= num; ++i) {
            f *= i;
        }
        cout << f << endl;
    }
}

// compute nPk for each line of two integers
void nPk() {
    string line;
    while(getline(cin, line)) {
        istringstream iss(line);
        long n; long k; iss >> n; iss >> k;
        if(n < 0) {
            cerr << "ERROR: For nPk, n cannot be a negative number: " << n << endl;
            exit(-1);
        }
        else if(k < 0) {
            cerr << "ERROR: For nPk, k cannot be a negative number: " << k << endl;
            exit(-1);
        }
        else if(k > n) {
            cerr << "ERROR: For nPk, n must be larger than k: n=" << n << " and k=" << k << endl;
            exit(-1);
        }
        unsigned long p = 1;
        for(unsigned long i = n-k+1; i <= (unsigned long)n; ++i) {
            p *= i;
        }
        cout << p << endl;
    }
}

// compute nCk for each line of two integers
void nCk() {
    string line;
    while(getline(cin, line)) {
        istringstream iss(line);
        long n; long k; iss >> n; iss >> k;
        if(n < 0) {
            cerr << "ERROR: For nCk, n cannot be a negative number: " << n << endl;
            exit(-1);
        }
        else if(k < 0) {
            cerr << "ERROR: For nCk, k cannot be a negative number: " << k << endl;
            exit(-1);
        }
        else if(k > n) {
            cerr << "ERROR: For nCk, n must be larger than k: n=" << n << " and k=" << k << endl;
            exit(-1);
        }
        unsigned long p = 1;
        for(unsigned long i = n-k+1; i <= (unsigned long)n; ++i) {
            p *= i;
        }
        unsigned long den = 1;
        for(unsigned long i = 2; i <= (unsigned long)k; ++i) {
            den *= i;
        }
        p /= den;
        cout << p << endl;
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

// check if a list of numbers is sorted in ascending order
bool sortedA() {
    double prev;
    cin >> prev;
    double next;
    while(cin >> next) {
        if(next < prev) {
            return false;
        }
        prev = next;
    }
    return true;
}

// check if a list of numbers is sorted in descending order
bool sortedD() {
    double prev;
    cin >> prev;
    double next;
    while(cin >> next) {
        if(next > prev) {
            return false;
        }
        prev = next;
    }
    return true;
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

// check argument string for valid double (arg = argv[1], l = length of stuff before number)
double check_num_double( const string & arg, const unsigned int & l ) {
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
        exit(-1);
    }
    else {
        return num;
    }
}

// check argument string for valid integer (arg = argv[1], l = length of stuff before number)
int check_num_int( const string & arg, const unsigned int & l ) {
    if(arg.length() == l) {
        cerr << "ERROR: No number specified" << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    int num = 0;
    bool neg = false;
    unsigned int ZERO = '0';
    for(unsigned int i = l; i < arg.length(); ++i) {
        if(i == l && arg[i] == '-') {
            neg = true;
        }
        else if(arg[i] < '0' or arg[i] > '9') {
            cerr << "ERROR: Invalud integer specified: " << arg.substr(l).c_str() << endl;
            exit(-1);
        }
        else {
            num = (num*10) + (unsigned int)arg[i] - ZERO;
        }
    }
    if(neg) {
        num *= -1;
    }
    return num;
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
    cout.precision(numeric_limits<double>::digits10);

    // perform task
    if(strcmp(argv[1],"-abs") == 0) {
        abs();
    }
    else if(argv[1][1] == 'a' && argv[1][2] == 'd' && argv[1][3] == 'd') {
        check_num_double(argv[1],4);
        add(strtod(((string)argv[1]).substr(4).c_str(),(char**)0));
    }
    else if(strcmp(argv[1],"-avg") == 0) {
        cout << avg() << endl;
    }
    else if(strcmp(argv[1],"-ceil") == 0) {
        ceil();
    }
    else if(strcmp(argv[1],"-cma") == 0) {
        cma();
    }
    else if(strcmp(argv[1],"-csv") == 0) {
        dlm(",");
    }
    else if(argv[1][1] == 'd') {
        if(argv[1][2] == 'i' && argv[1][3] == 'v') {
            div( check_num_double(argv[1],4));
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
    else if(strcmp(argv[1],"-exp") == 0) {
        Exp();
    }
    else if(strcmp(argv[1],"-fact") == 0) {
        fact();
    }
    else if(strcmp(argv[1],"-floor") == 0) {
        floor();
    }
    else if(argv[1][1] == 'g' && argv[1][2] == 't') {
        if(argv[1][3] == 'e') {
            gte( check_num_double(argv[1],4));
        }
        else {
            gt( check_num_double(argv[1],3));
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
            Log( check_num_double(argv[1],4));
        }
        else if(argv[1][2] == 't') {
            if(argv[1][3] == 'e') {
                lte( check_num_double(argv[1],4));
            }
            else {
                lt( check_num_double(argv[1],3));
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
    else if(argv[1][1] == 'm' && argv[1][2] == 'o' && argv[1][3] == 'd') {
        mod( check_num_int(argv[1],4));
    }
    else if(argv[1][1] == 'm' && argv[1][2] == 'u' && argv[1][3] == 'l') {
        mult( check_num_double(argv[1],4));
    }
    else if(argv[1][1] == 'n') {
        if(argv[1][2] == 'e' && argv[1][3] == 'g') {
            mult(-1);
        }
        else if(argv[1][2] == 'P' && argv[1][3] == 'k') {
            nPk();
        }
        else if(argv[1][2] == 'C' && argv[1][3] == 'k') {
            nCk();
        }
        else {
            cerr << "ERROR: Invalid argument: " << argv[1] << endl;
            cerr << USAGE_MESSAGE << endl;
            exit(-1);
        }
    }
    else if(argv[1][1] == 'p' && argv[1][2] == 'o' && argv[1][3] == 'w') {
        power( check_num_double(argv[1],4));
    }
    else if(strcmp(argv[1],"-prod") == 0) {
        cout << prod() << endl;
    }
    else if(argv[1][1] == 'q' && argv[1][2] == 'u' && argv[1][3] == 'a' && argv[1][4] == 'n' && argv[1][5] == 't') {
        cout << quant( check_num_double(argv[1],6)) << endl;
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
        sub( check_num_double(argv[1],4));
    }
    else if(strcmp(argv[1],"-sortA") == 0 || strcmp(argv[1],"-sort") == 0) {
        sortA();
    }
    else if(strcmp(argv[1],"-sortD") == 0) {
        sortD();
    }
     else if(strcmp(argv[1],"-sortedA") == 0 || strcmp(argv[1],"-sorted") == 0) {
        cout << sortedA() << endl;
    }
    else if(strcmp(argv[1],"-sortedD") == 0) {
        cout << sortedD() << endl;
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
