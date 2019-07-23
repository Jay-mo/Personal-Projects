#!/usr/bin/env python3
# A script that simply uses dig to make a dns query for ipv6 address of a given fqdn.
# takes the result and then extracts the ipv6 addresses.
#just using these simple scripts as learning tools

#importing the sys and subprocess module
import sys
import subprocess

#taking the name to lookup from the command line.
name_to_lookup = sys.argv[1]

#constructing the command to be issued.
cmd = "dig {} AAAA".format(name_to_lookup)

# issue the command and store the result in a variable
query_result = subprocess.check_output(cmd)

#decoding the output of the command since it is returned as bytes
#this turns it into strings.
query_string = query_result.decode('utf-8')

#breaking up the string into a list. The delimiter is the newline character.
parse_string = query_string.split('\n')

#creating the list to store ipv6 addresses
ip_addr = []

#use for loop to loop through the list of lines from the string.
#takes lines that start with the fqdn and splits them
for line in parse_string:
    if line.startswith(name_to_lookup):
        line = line.split()
        # add ipv6 addresses to ip_addr 
        ip_addr.append(line[4].strip())

#giving back the results to the user.
if len(ip_addr) == 0:
    print("{} has no ipv6 addresses.".format(name_to_lookup))
else:
    print ("{} has the following ipv6 addresses".format(name_to_lookup))

for entry in ip_addr:
    print (entry)

#ipv6_regex = r'\w{1,4}:\w{1,4}:\w{1,4}:\w{1,4}:\w{1,4}:\w{1,4}:\w{1,4}:\w{1,4}'

#match = re.search(ipv6_regex, query_string)

