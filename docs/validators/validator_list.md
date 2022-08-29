# Available validators

## General Validators

| Name | Parameters | Description |
|---|---|---|
|required| | Value is required|
|bail| | Special validator to skip running all validators on failure|
|id | |Value must be a positive numeric greater than 0|
|uuid| | Value must be a valid UUID|
|notempty| | Value must not be empty|
|in|list,of,values...| Value must be in the specified list of values|
|notin|list,of,values...| Value must not be in the specified list of values|
|strin|list,of,values...| Value is a string and must be in the specified list of values|
|strnotin|list,of,values...| Value is a string and must not be in the specified list of values|
|bool| | Value must be a valid bool representation: 0, 1, y, t, true, n, f, false|
|iso8601| | Value must be a valid iso8601 date string|


## String Validators

| Name | Parameters | Description |
|---|---|---|
|alpha| | Value must contain only letters a-z and A-Z|
|alphanum| | Value must contain only letters a-z and A-Z or digits 0-9|
|slug| | Value must be an alphanum string, but that can contain '-' and '_'|
|len|min,max| Value char length must be between min and max|
|minlen|min| Value char length must be at least min chars|
|maxlen|max| Value char length must be upto max chars|


## List Validators
| Name | Parameters | Description |
|---|---|---|
|list| | Value must be a list of items|
|listlen| min[, max]] | Item list must have at least min elements and optionally max elements|


## Numeric Validators

| Name | Parameters | Description |
|---|---|---|
|between |min,max |Value must be numeric between min and max; Floats are supported|
|numeric | | Value must be a numeral (digits only)|
|decimal | | Value must be a valid decimal numeral|


## Network Validators

| Name | Parameters | Description |
|---|---|---|
|ipv4 | |Value must be a valid IPv4 address|
|ipv6 | |Value must be a valid IPv6 address|
|ip | | Value must be a valid IPv4 or IPv6 address|
|fqdn | | Value must be a valid fqdn (fully qualified domain name)|
|email | | Value must be a valid email address|
|mac | | Value must be a valid MAC address|

## Hash Validators

| Name | Parameters | Description |
|---|---|---|
|md5| | Value must be a valid MD5 hash|
|sha1| | Value must be a valid SHA1 hash|
|sha256| | Value must be a valid SHA256 hash|
|sha512| | Value must be a valid SHA512 hash|
