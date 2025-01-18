## Encrypt a string
echo -n "yourplaintext" | openssl enc -aes-256-cbc -a -salt -pbkdf2 -iter 100000 -pass pass:yourpassword


## decrypt a string
```
echo "ENCRYPTED_STRING" | openssl enc -aes-256-cbc -a -d -salt -pbkdf2 -iter 100000 -pass pass:yourpassword

```
