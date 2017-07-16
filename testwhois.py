#!/usr/bin/env python2
# writedata.py

import argparse, pythonwhois, json, datetime, sys


parser = argparse.ArgumentParser(description="Retrieves and parses WHOIS data for a domain name.")
parser.add_argument("-f", "--file", action="store", help="Loads and parses WHOIS data from a specified file. ", default=None)
#parser.add_argument("domain", nargs=1)
args = parser.parse_args()


if args.file is None:
    	data, server_list = pythonwhois.net.get_whois_raw(args.domain[0], with_server_list=True)
else:
	server_list = []
	with open(args.file, "r") as f:
		data = f.read().split("\n")

try:
	from collections import OrderedDict
except ImportError as e:
	from ordereddict import OrderedDict

def json_fallback(obj):
    	if isinstance(obj, datetime.datetime):
		return obj.isoformat()
	else:
		return obj

data, server_list = pythonwhois.net.get_whois_raw(data[0], with_server_list=True)

#print data
parsed = pythonwhois.parse.parse_raw_whois(data, normalized=True, never_query_handles=False, handle_server=server_list[-1])

with open("output", "w") as outfile:
	json.dump(parsed, outfile, default=json_fallback)
