This is a collection of command-line tools I wrote to make various repetitive tasks more convenient. They will typically take input from standard input and will output to standard output. I make an effort to not use external libraries so that compilation requires the least possible dependencies. Note that some other tools/scripts I write for other projects use these tools and assume they can be found in your `PATH`.

* **[numlist](numlist.cpp): Perform various basic tasks on a list of numbers**
    * The list of numbers must be passed in via standard input
    * Run it without arguments to see the usage message, which contains a list of functions
    * The list of numbers can be integers or decimals: the tool handles both
    * The numbers must be delimited by whitespace
    * If your numbers are *not* delimited by whitespace, you can use `tr` to fix your list. For example:
    ```bash
    echo "1,2,3,4,5" | tr ',' ' ' | numlist -sum
    ```

* **[touchall.sh](touchall.sh): Recursively touch all files in current directory (and subdirectories)**
    * Run it without arguments


INSTALLATION
===
1. Clone the [GitHub repository](https://github.com/niemasd/tools.git) wherever you want to install the tools. For example, if I wanted to install the collection into a directory `~/bin`:
    ```bash
    cd ~/bin
    git clone https://github.com/niemasd/tools.git
    ```

2. Compile the tools with `make` (the `Makefile` should compile all of the tools automatically). To continue the previous example:
    ```bash
    cd ~/bin/tools
    make
    ```

3. **OPTIONAL:** Other tools/scripts I write for other projects may expect these tools to be found in your `PATH`, so I would suggest adding the directory to your `PATH` variable. To continue the previous example, if I were to add it to my `.profile`:
    ```bash
    echo "PATH=~/bin/tools:$PATH" >> ~/.profile
    ```
