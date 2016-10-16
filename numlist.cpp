/* Niema Moshiri 2016
 *
 * Perform various basic tasks on a list of numbers passed in via STDIN. Only
 * one number should be on each line of the input.
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
"    -avg:    Compute average of list of numbers\n"
"    -csv:    Print the list as comma-separated values\n"
"    -int:    Print the list as integers\n"
"    -max:    Compute maximum of list of numbers\n"
"    -min:    Compute minimum of list of numbers\n"
"    -sum:    Compute sum of list of numbers\n";

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
    else if(strcmp(argv[1],"-int") == 0) {
        Int(nums);
    }
    else if(strcmp(argv[1],"-max") == 0) {
        cout << max(nums) << endl;
    }
    else if(strcmp(argv[1],"-min") == 0) {
        cout << min(nums) << endl;
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