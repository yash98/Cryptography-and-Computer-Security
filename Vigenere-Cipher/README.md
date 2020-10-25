# Cryptanalysis of Vigenere Cipher

## How to run?

`python cryptanalysis.py`

All modules are written in python 3 and only use the default libraries (i.e. no external dependencies).

Default input directory is `tests` and default output directory is `crypt_analysis`. Both these directories should be in the same directory as `cryptanalysis.py` file. These defaults can be changed by the arguments mentioned in the next section.

## Arguments for the program

- `-d` : Directory for picking input files with the encrypted text. Only files with name of pattern `test[0-9]*` are picked
- `-f` : Takes a space separated list of file paths
- `-o` : Directory for generating output files with cryptanalysis for encrypted input files 
- `-h` : Prints help, usage details

Paths in the arguments should be relative to `cryptanalysis.py` file. 

A generalized usage could be like - 

`python cryptanalysis.py -d ./Test_case -o ./Output_folder` 

or 

`python cryptanalysis.py -f ./Test_case/abcd ./Examples/examples.txt -o ./Output_folder`. 

Only one of `-d` or `-f` can be used at a time

## Brief implementation details

1. List of input files
   1. Either thorugh `-f` flag or picked through `-d` flag. Otherwise default location is used
2. Kisaski Method - `kasiski_method.py`
   1. To generate set of candidate key lengths
   2. Gcd of distance between same keywords (or n-grams)
3. Index of Coincidence - `ic.py`
   1. Picking/Verifying the best key length out of all the candidates
   2. Probability of 2 randomly picked characters from the encrypted text being the same
   3. Encrypted message is divided into key length number of set. Average of probability mentioned is calculated.
   4. Probability closest (Norm 1) to IC English is the best key length 
4. Mutual Index of Coincidence - `mic.py`
   1. To calculate the key of selected key length
   2. Probability of drawing same character from different texts
   3. One is text in english language other is our encrypted message shifted divided into part according to key length 
   4. Shift value giving MIC closest to MIC English is selected. This is how a character of the key is calculated
5. Decryption using the calculated key
6. Write info generated into required files along with the execution of the above steps
