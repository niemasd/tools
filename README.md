This is a collection of command-line tools I wrote to make various repetitive tasks more convenient. They will typically take input from standard input and will output to standard output. I make an effort to not use external libraries so that compilation requires the least possible dependencies. Note that some other tools/scripts I write for other projects use these tools and assume they can be found in your `PATH`.

* **[boxplots.py](boxplots.py): Create box plots from data**
    * Reads the data from standard input by default, or a file can be passed via `-i`
        * The data must be in the JSON (or Python dictionary) format
    * For help message: `python boxplots.py -h`

* **[fasta2json.py](fasta2json.py): Convert a FASTA file to JSON**
    * For help message: `python fasta2json.py -h`

* **[fastq_header_rename_illumina.py](fastq_header_rename_illumina.py): Rename the read identifiers of a FASTQ file to follow the Illumina standard**
    * For help message: `python fastq_header_rename_illumina.py -h`

* **[histogram.py](histogram.py): Create a histogram from a list of numbers**
    * Reads the list of numbers from standard input by default, or a file can be passed via `-i`
        * The numbers in the list must be whitespace-delimited
    * For help message: `python histogram.py -h`

* **[mergebib.py](mergebib.py): Merge multiple BibTeX files into a single file named `merged.bib`**
    * Usage: `python mergebib.py <file1.bib> <file2.bib> ...`
    * Verbose messages are output to standard error, and the merged file is output to standard output

* **[numlist](numlist.cpp): Perform various basic tasks on a list of numbers**
    * The list of numbers must be passed in via standard input
    * Run it without arguments to see the usage message, which contains a list of functions
    * The list of numbers can be integers or decimals: the tool handles both
    * The numbers must be delimited by whitespace
    * If your numbers are *not* delimited by whitespace, you can use `tr` to fix your list. For example:
    ```bash
    echo "1,2,3,4,5" | tr ',' ' ' | numlist -sum
    ```

* **[nw_error](nw_error)**: Compute various error metrics on Newick trees
    * Usage: `nw_error metric tree1 tree2`

* **[scatterplot.py](scatterplot.py): Create a scatterplot from two lists of numbers (x,y)**
    * Reads the list of points from standard input by default, or a file can be passed vi `-i`
        * Each line should contain a single point in the format `xvalue,yvalue`, e.g.:
            ```
            1,10
            2,9
            3,8
            ```
    * For help message: `python scatterplot.py -h`

* **[touchall.sh](touchall.sh): Recursively touch all files in current directory (and subdirectories)**
    * Run it without arguments

* **[violinplots.py](violinplots.py): Create violin plots from data**
    * Reads the data from standard input by default, or a file can be passed via `-i`
        * The data must be in the JSON (or Python dictionary) format
    * For help message: `python violinplots.py -h`

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
