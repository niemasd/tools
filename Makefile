# use g++ compiler with C++11 support
CXX=g++
CXXFLAGS=-Wall -pedantic -O3 -std=c++11
TOOLS=numlist samstats

# compile all tools
all: $(TOOLS)

# numlist: Perform basic tasks on a list of numbers passed in via STDIN
numlist: numlist.cpp
	$(CXX) $(CXXFLAGS) -o numlist numlist.cpp

# samstats: Compute basic statistics on a SAM file passed in via STDIN
samstats: samstats.cpp
	$(CXX) $(CXXFLAGS) -o samstats samstats.cpp

# remove all compiled files
clean:
	$(RM) $(TOOLS) *.o
