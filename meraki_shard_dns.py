# meraki_shard_dns.py
"""
A script that runs and queries all meraki shards and prints out their CNAME, A and AAAA records.
If a flag is given to the script it should just return the records of the specified machine.

"""


import argparse
import dns.resolver as resolver


# create parser
script_parser = argparse.ArgumentParser(
    prog='meraki_shard_dns', usage='%(prog)s [options] ', description='Returns CNAME, A records of Meraki shards')

# add an argument or a flag to parse
parser = script_parser.add_argument('-m', metavar='meraki_shard', type=str,
                                    help='the shard to query')

# initialize parser
args = script_parser.parse_args()

# variable for meraki domain
domain = 'meraki.com'

# variable to keep track of the shard number
count = 1

# variable used to keep track of shards that have no records.
# after 5 consecutive increments we stop script with the assumption
# that there are no more active shards.
no_value = 0

# check for presence of flag and provide CNAME and A record for shard
if args.m:
    meraki_shard = args.m

    dns_resolver = resolver.Resolver()

    try:

        response = dns_resolver.resolve(meraki_shard)
        CNAME = response.canonical_name.to_text()

        A_record = response.rrset.to_text().split()[-1]

        print(meraki_shard, CNAME, A_record)

    except:
        print(f"{meraki_shard} DNS name does not exist")
# run script to get all the CNAME and A records for all the active shards.
else:
    # while loop that keeps running.
    while True:
        meraki_shard = f'n{count}.{domain}'
        dns_resolver = resolver.Resolver()

        try:

            response = dns_resolver.resolve(meraki_shard)
            CNAME = response.canonical_name.to_text()

            A_record = response.rrset.to_text().split()[-1]

            print(meraki_shard, CNAME, A_record)

            count += 1
            no_value = 0
        # if there is an error, print DNS name does not exist.
        except:
            no_value += 1
            count += 1
            print(f"{meraki_shard} DNS name does not exist")
        # after 5 consecutive failed queries, stop script.
        if no_value > 5:
            break
