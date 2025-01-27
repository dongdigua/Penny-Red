#!/usr/bin/env python

import email.message
import io
import subprocess
import sys

# Change the DB path in COMMAND as needed, and change your email address(es)
COMMAND="hashcash -cdb '%s' -r '%s' -f ~/.mutt/hashcash.db '%s'"
EMAILADDR=("foo@example.com", "bar@example.com")

tokens = []
token_status = []

# converting a list to a file-type object for parsing rfc822 headers
original = sys.stdin.read()
# emailmsg = io.StringIO(''.join(original))
message = email.message_from_string(original)


# check for the presence of "X-Hashcash" and "Hashcash" headers
# and extract only matches from EMAILADDR
if "X-Hashcash" in message.keys():
    for hc_list in message.get_all("X-Hashcash"):
        if hc_list.split(":")[3] in EMAILADDR:
            tokens.append(hc_list)
# if message.has_key("Hashcash"):
#     for hc_list in message.getheaders("Hashcash"):
#         if hc_list.split(":")[3] in EMAILADDR:
#             tokens.append(hc_list)

# check each token
if tokens:
    token_status.append("[-- Begin Hashcash output --]")
    for token in tokens:
        bits = token.split(":")[1]
        emailaddr = token.split(":")[3]
        p = subprocess.Popen(COMMAND % (bits, emailaddr, token),
            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        out = p.stderr.read().strip().decode('ascii')
        token_status.append(out)
    token_status.append("[-- End Hashcash output --]")

headers_str = "\n".join(f"{key}: {value}" for key, value in message.items())
print(headers_str)
print('')
for status in token_status:
    print(status)
if tokens:
    print('')
print(message.get_payload())
