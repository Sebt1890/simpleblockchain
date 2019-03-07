# simpleblockchain
Simple Blockchain w/python

This is a simple blockchain I worked on and used multiple sources to get the framework going. 
Hopefully this helps those interested in learning how the Blockchain works via Python. 
Comments have been added throughout the code to help with understanding. 

To get the transactions to run I used Windows Powershell and used the "Invoke-Webrequest" method. 
--------------
Invoke-RestMethod "http://localhost:5000/txion" -ContentType 'application/json' -Method Post -Body '{"from": "asdfas", "to": "asdfas", "amount": 3}'
