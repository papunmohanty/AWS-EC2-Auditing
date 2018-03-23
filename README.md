### This script use to get the AWS EC2 detail in an Excel Sheet

#### Note: This script uses Python3.x

### Python library used:
1. boto3
2. pandas

### Installation of libraries prior to running this script

#### **NOTE:** Please use pip for `python3` version

```sh
1. pip install boto3
2. pip install pandas
```

### Your AWS Credential files should look like this
```sh
[qa]
aws_access_key_id = XXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[dev]
aws_access_key_id = XXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[prod]
aws_access_key_id = XXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Running this script:
colning this repository or download this script and then running the script by using following commands in your `cli`
```sh
$ git clone https://github.com/papunmohanty/AWS-EC2-Auditing.git
$ python boto3WithPandas_the_OOP_Way.py
```
##### It will ask for the `environment` and `region` details like:
```sh
Enter the Environment Name: prod
Enter the Region Name: us-east-1
```
##### **NOTE:** Please choose according to what is configured in your AWS Credential file.
