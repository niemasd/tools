This is a collection of command-line tools I wrote to make various repetitive tasks more convenient. They will typically take input from standard input and will output to standard output. I make an effort to not use external libraries so that compilation requires the least possible dependencies. Note that some other tools/scripts I write for other projects use these tools and assume they can be found in your `PATH`.

* **[boxplots.py](boxplots.py): Create box plots from data**
    * Reads the data from standard input by default, or a file can be passed via `-i`
        * The data must be in the JSON (or Python dictionary) format
    * For help message: `python boxplots.py -h`

* **[convert_trees.py](convert_trees.py): Convert input tree(s) to different formats**
    * Can convert branch support values from decimal to percentage (and vice-versa)
    * Can convert tree schema between formats: {'newick','nexus','phyloxml','nexml'}
    * For branches without support values, can give them a default value (e.g. 100), or keep them empty by default
    * For help message: `python convert_trees.py`

* **[fasta1ln.py](fasta1ln.py): Convert a multiline FASTA file to one-line**
    * For help message: `python fasta1ln.py -h`

* **[fasta2json.py](fasta2json.py): Convert a FASTA file to JSON**
    * For help message: `python fasta2json.py -h`

* **[fasta2phylip.py](fasta2json.py): Convert a FASTA multiple sequence alignment to Phylip**
    * For help message: `python fasta2phylip.py -h`

* **[fasta_cut_seqs.py](fasta_cut_seqs.py): Cut the sequences of a given FASTA file to be a given length**
    * For help message: `python fasta_cut_seqs.py -h`

* **[fasta_subsample.py](fasta_subsample.py): Subsample a given FASTA file**
    * For help message: `python fasta_subsample.py -h`

* **[fastq_header_rename_illumina.py](fastq_header_rename_illumina.py): Rename the read identifiers of a FASTQ file to follow the Illumina standard**
    * For help message: `python fastq_header_rename_illumina.py -h`

* **[fastq_merge.py](fastq_merge.py): Merge multiple FASTQ files**
    * Usage: `fastq_merge.py <fastq_files>`

* **[fastq2fasta.py](fastq2fasta.py): Convert a FASTQ file to FASTA**
    * For help message: `python fastq2fasta.py -h`

* **[hamming.py](hamming.py): Compute all pairwise Hamming distances from a given multiple sequence alignment**
    * For help message: `python hamming.py -h`

* **[histogram.py](histogram.py): Create a histogram from a list of numbers**
    * Reads the list of numbers from standard input by default, or a file can be passed via `-i`
        * The numbers in the list must be whitespace-delimited
    * For help message: `python histogram.py -h`

* **[hmmer_to_pomegranate.py](hmmer_to_pomegranate.py): Convert a profile HMM from the HMMER-3 format to the pomegranate serialized JSON format**
    * For help message: `python hmmer_to_pomegranate.py -h`

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

* **[nw_error](nw_error): Compute various error metrics on Newick trees**
    * Usage: `nw_error metric tree1 tree2`

* **[patristic_distances.py](patristic_distances.py): Compute all patristic distances from the given tree**
    * For help message: `python patristic_distances.py -h`

* **[ranDNA.py](ranDNA.py): Generate random DNA sequences**
    * For help message: `python ranDNA.py -h`

* **[resolve_random.R](resolve_random.R): Randomly resolve a multifurcating tree**
    * Reads multifurcating tree from STDIN and writes resolved tree to STDOUT
    * Usage: `resolve_random.R < UNRESOLVED.tre > RESOLVED.tre`

* **[rmdup.sh](rmdup.sh): Remove consecutive identical files (keep first instance)**
    * Usage: `rmdup.sh`

* **[safenames.py](safenames.py): Convert the identifiers of a FASTA file to random safe names**
    * Safename FASTA is output to STDOUT
    * Dictionary of name mappings is output to STDERR
    * For help message: `python safenames.py -h`

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

* **[tree_subsample.py](tree_subsample.py): Subsample a given Newick file**
    * For help message: ``python tree_subsample.py -h``

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
