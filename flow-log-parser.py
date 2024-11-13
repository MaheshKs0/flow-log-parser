import csv
import os

protocol_mapping = {}
lookup_table = {}
port_protocol_matches = {}
tag_counts = {}

def read_flow_logs():
    if not os.path.exists("Flow_Logs.txt"):
        print("Error: Flow log file does not exist.")
        return
    try:
        #creating a generator/yielding to make sure that we don't load the whole file at a time.
        with open("Flow_Logs.txt",'r') as file:
            for line in file:
                yield line
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def parse_log_line(line):
    log_details = line.strip().split()
    expected_log_length = 14  # assuming the log line should have 14 columns
    if len(log_details) == expected_log_length:
        #based on the log file format, pulling the 6th and 7th value from each row which are dest port and protocol.
        return {
            'dstport': log_details[6],
            'protocol_number': log_details[7],
        }
    else:
        print(f"Skipping log line: {line.strip()}")
        return None


def map_protocol(protocol_number):
    #get the protocol name based on the protocol number in the log file.
    protocol = protocol_mapping.get(protocol_number, "unknown")
    return protocol

def process_flow_logs():
    for line in read_flow_logs():
        log_details = parse_log_line(line)
        if not log_details:
            continue #for any logs which don't have expected number of columns
        protocol = map_protocol(log_details["protocol_number"])
        destination_port = log_details["dstport"]

        #count Port/Protocol Combinations
        port_protocol_matches[(destination_port, protocol.lower())] = port_protocol_matches.get(
            (destination_port, protocol.lower()), 0) + 1

        #check for dest port and protocol tuple key in lookup table hashmap and get the tag.
        destport_protocol = (destination_port, protocol.lower())
        if destport_protocol in lookup_table:
            log_details['Tag'] = lookup_table[destport_protocol]
        else:
            log_details['Tag'] = "untagged"

        #count the tags
        tag = log_details['Tag']
        tag_counts[tag] = tag_counts.get(tag,0) + 1
    return port_protocol_matches,tag_counts

def read_lookup_table():
    if not os.path.exists("look_up_table.csv"):
        print("Error: Lookup table file does not exist.")
        return
    with open("look_up_table.csv") as file:
        table = csv.reader(file)
        next(table)
        for val in table:
            if any(cell == '' for cell in val):
                print(f"Skipping row with missing values: {val}")
                continue #skip if we have any empty cells
            lookup_table[(val[0],val[1])] =val[2] #dstport and protocol in a tuple (key) with tag as the value in a hashmap/dictionary

def get_protocol_name_from_number():
    if not os.path.exists("protocol-numbers.csv"):
        print("Error: Protocol numbers file does not exist.")
        return
    with open("protocol-numbers.csv", 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skip the header
        for row in csv_reader:
            #we only care about the first two columns as a number is mapped to a protocol.
            if row[0]: #values which are not null
                if row[1]:
                    protocol_mapping[row[0]] = row[1]
                else:
                    protocol_mapping[row[0]] = 'Unassigned' #Handling a scenario where we have no protocol mapped


def write_counts_to_file(ptop_matches,t_matches):
    try:
        with open("output_file.txt", mode='w') as file:
            #Writing the Port/Protocol Combinations first
            file.write("Port/Protocol Combination Counts: \n")
            file.write("Port,Protocol,Count \n")
            for key,value in ptop_matches.items():
                file.write(f"{key[0]},{key[1]},{value}\n")
            # Writing the Tag Counts Combinations
            file.write("\nTag Counts: \n")
            file.write("Tag,Count \n")
            for key,value in t_matches.items():
                file.write(f"{key},{value}\n")
    except IOError as e:
        print(f"Error writing output to file: {e}")


if __name__ == "__main__":
    '''as we have a number representing a protocol,idea is to get all the protocols mapped to different numbers.
    I got a csv file from website: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
    this was shared in https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields
    So, I manually downloaded the file with mappings and parsing the details using the func below. '''
    get_protocol_name_from_number()
    #read the lookup table
    read_lookup_table()
    #read log data and process it while calculating tag counts and Port/Protocol Combination counts
    process_flow_logs()
    #write the calculated data back to text file
    write_counts_to_file(port_protocol_matches,tag_counts)











