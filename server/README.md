# Python XMLRPC Server

Demonstrating the difficulty of protecting remote python server against DDoS attacks and Remote Code Execution (RCE) attacks.

After applying defensive programming principles and following security
best practices, I came up with a more reliable solution.

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

# How to run server

```bash
pip install -r requirements.txt
python {version folder}/server.py
```
