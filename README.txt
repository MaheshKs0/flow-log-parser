# Flow Log Parser

This program parses flow logs from a given file, maps each row to a tag based on a lookup table, and outputs counts for port/protocol combinations and tags.

## Assumptions
- The program supports only the default log format (Version 2) as described in the AWS documentation.
- Flow log records should contain the required fields such as `dstport` and `protocol_number`.
- Lookup table and flow logs are text-based files.
- The program assumes that the `Flow_Logs.txt`, `look_up_table.csv`, and `protocol-numbers.csv` files are located in the same directory as the script, or their paths should be provided.
- The first column in downloaded file (from:https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml per AWS documentation): protocol-numbers.csv is protocol number and the second column contains the corresponding protocol name.
 

## Usage/Instructions

Ensure that you have **Python 3.x** installed. 

Step 1: Clone or Download the Repository
If you're using a GitHub repository, clone it using the following command, or download the repository as a ZIP file:
```bash
git clone https://github.com/MaheshKs0/flow-log-parser.git
cd flow-log-parser

2. Make sure the following files are available in the same directory where you're running the script from, and ensure that the filenames match:
   - `Flow_Logs.txt`: Contains the flow log records in the default format.
   - `look_up_table.csv`: Contains port/protocol combinations and corresponding tags.
   - `protocol-numbers.csv`: Maps protocol numbers to protocol names. You can download this file from (https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) as mentioned in AWS website for default logs.
   
3. If the files are not in the same directory, you may provide the full file paths instead.

4. To run the script, execute the following command from the project directory:
   python flow_log_parser.py
   
   The program will process the flow log data and generate an output file named output_file.txt with the results.


## Output
- The program generates an output_file.txt containing the following:
Port/Protocol Combination Counts: A count of each unique port/protocol combination found in the flow logs.
Tag Counts: A count of how many times each tag is applied based on the lookup table.

## Test Cases
- Test with sample flow logs and a lookup table to verify tag mapping and counts. You can find these sample files in the GitHub repository.

