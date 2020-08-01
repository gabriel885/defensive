# Python XMLRPC Server

Demonstrating the difficulty of protecting remote python server against DDoS attacks and Remote Code Execution (RCE) attacks.

After applying defensive programming principles and following security
best practices, I came up with a more reliable solution. 

## Important note  
I could not manage to protect the server against DoS on the socket layer, 
due to the fact that packets filtration itself for non-legitimate packets is the main 
contributor of DoS attack. 
Those, defending DoS can be mainly prevented on lower levels (CDN/LB/DPI).


## Requirements

Python 3.7 (pip installed)
Unix machine (recommended)

### v1

    -   non isolated code execution
    -   denial of service attack
    -   easy access to host shell via RCE

### v2

    -   isolated and monitored code excution environment
    -   restricted memory usage / cpu time / os and network access
    -   limited private server tokens to access services
    -   No serialization methods involved
    -   Authorisation required

# How to run server

```bash
pip install -r requirements.txt
python {version folder}/server.py
```

Copyrighted to Gabriel Munits. Please do not share material.