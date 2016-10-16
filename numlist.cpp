/* Niema Moshiri 2016
 *
 * Perform various basic tasks on a list of numbers passed in via STDIN.
 *
 * Only pass in a single argument.
 */

// include statements
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// usage message
const string USAGE_MESSAGE =
"\nUSAGE: numlist -ARG\n"
"    -avg:       Compute average of list of numbers\n"
"    -csv:       Print the list as comma-separated values\n"
"    -div<NUM>:  Divide all numbers by <NUM>\n"
"    -gt<NUM>:   Print all numbers greater than <NUM>\n"
"    -gte<NUM>:  Print all numbers greater than or equal to <NUM>\n"
"    -int:       Print the list as integers\n"
"    -lt<NUM>:   Print all numbers less than <NUM>\n"
"    -lte<NUM>:  Print all numbers less than or equal to <NUM>\n"
"    -max:       Compute maximum of list of numbers\n"
"    -min:       Compute minimum of list of numbers\n"
"    -mult<NUM>: Multiply all numbers by <NUM>\n"
"    -sum:       Compute sum of list of numbers\n";

// compute the sum of a list of numers
double sum( vector<double> & nums ) {
    double out = 0;
    for(auto i : nums) {
        out += i;
    }
    return out;
}

// compute the average of a list of numbers
double avg( vector<double> & nums ) {
    return sum(nums) / nums.size();
}

// print the list of numbers as comma-separated
void csv( vector<double> & nums ) {
    cout << nums[0];
    for(int i = 1; i < nums.size(); ++i) {
        cout << ',' << nums[i];
    }
    cout << endl;
}

// print the list of numbers as integers
void Int( vector<double> & nums ) {
    for(auto i : nums) {
        cout << (int)i << endl;
    }
}

// find the max of a list of numbers
double max( vector<double> & nums ) {
    double out = nums[0];
    for(auto i : nums) {
        if(i > out) {
            out = i;
        }
    }
    return out;
}

// find the min of a list of numbers
double min( vector<double> & nums ) {
    double out = nums[0];
    for(auto i : nums) {
        if(i < out) {
            out = i;
        }
    }
    return out;
}

// output all numbers greater than the threshold
void gt( vector<double> & nums, double thresh ) {
    for(auto i : nums) {
        if(i > thresh) {
            cout << i << endl;
        }
    }
}

// output all numbers greater than or equal to the threshold
void gte( vector<double> & nums, double thresh ) {
    for(auto i : nums) {
        if(i >= thresh) {
            cout << i << endl;
        }
    }
}

// output all numbers less than the threshold
void lt( vector<double> & nums, double thresh ) {
    for(auto i : nums) {
        if(i < thresh) {
            cout << i << endl;
        }
    }
}

// divide all numbers by num
void div( vector<double> & nums, double num ) {
    for(auto i : nums) {
        cout << i/num << endl;
    }
}

// multiply all numbers by num
void mult( vector<double> & nums, double num ) {
    for(auto i : nums) {
        cout << i*num << endl;
    }
}

// output all numbers less than or equal to the threshold
void lte( vector<double> & nums, double thresh ) {
    for(auto i : nums) {
        if(i <= thresh) {
            cout << i << endl;
        }
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
    if(strcmp(argv[1],"-avg") == 0) {
        cout << avg(nums) << endl;
    }
    else if(strcmp(argv[1],"-csv") == 0) {
        csv(nums);
    }
    else if(argv[1][1] == 'd' && argv[1][2] == 'i' && argv[1][3] == 'v') {
        div(nums, stod(((string)argv[1]).substr(4)));
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
    else if(strcmp(argv[1],"-sum") == 0) {
        cout << sum(nums) << endl;
    }
    else {
        cerr << "ERROR: Invalid argument: " << argv[1] << endl;
        cerr << USAGE_MESSAGE << endl;
        exit(-1);
    }
    return 0;
}