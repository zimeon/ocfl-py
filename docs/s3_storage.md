# Using S3 storage

The `ocfl-py tools are intended to work with S3-compatible storage by specifying
paths with the `s3` protocol, like `s3://bucket/path`. This is implemented through
[S3Fs](https://s3fs.readthedocs.io/en/latest/index.html) which builds on top of
[aiobotocore](https://aiobotocore.aio-libs.org/en/latest/) and
[botocore](https://github.com/boto/botocore). The best configuration guide for this
seems to be the
[AWS boto3 configuration documentation](https://docs.aws.amazon.com/boto3/latest/guide/configuration.html).

## Simple AWS S3 configuration

AWS created S3 and the Python libraries implementing the interface. AWS S3 is the
default configuration. The default location for access key information is
`~/.aws/config` and this can be as simple as:

```
[default]
aws_access_key_id=ACCESS_KEY
aws_secret_access_key=SECRET_KEY
```

Where `ACCESS_KEY` and `SECRET_KEY` are obtained from the AWS console and given
without quotes.

With configuration set, `ocfl-py` command line tools will work with S3 URLs such as
`s3://ocfl-fixtures/1.1/good-objects/minimal_no_content` given here as an object path:

```
ocfl-py> ./ocfl-object.py show --objdir s3://ocfl-fixtures/1.1/good-objects/diff_files_same_md5
INFO:aiobotocore.credentials:Credentials found in config file: ~/.aws/config
INFO:root:OCFL v1.1 Object at s3://ocfl-fixtures/1.1/good-objects/diff_files_same_md5 has VALID STRUCTURE (DIGESTS NOT CHECKED)
Object tree for None
[s3://ocfl-fixtures/1.1/good-objects/diff_files_same_md5]
├── 0=ocfl_object_1.1
├── inventory.json
├── inventory.json.sha512
└── v1
    ├── content (2 files)
    ├── inventory.json
    └── inventory.json.sha512
```

The bucket name is `ocfl-fixtures` and the path within the bucket is
`1.1/good-objects/minimal_no_content`.

## S3 API access with other providers

Other vendors support the S3 API and can be configured by adding an `endpoint_url` parameter in the
configuration. For example, to configure for Filebase one might have `~/.aws/config`:

```
[default]
endpoint_url=https://s3.filebase.io
aws_access_key_id=ACCESS_KEY
aws_secret_access_key=SECRET_KEY
```

Where `endpoint_url=https://s3.filebase.io` specifies the network location of the Filebase
S3 API. `ACCESS_KEY` and `SECRET_KEY` are obtained from the provider.

```
ocfl-py> ./ocfl-object.py show --objdir s3://filebase-fixtures/1.1/good-objects/minimal_no_content
INFO:aiobotocore.credentials:Credentials found in config file: ~/.aws/config
INFO:botocore.configprovider:Found endpoint for s3 via: config_global.
WARNING:root:OCFL v1.1 Object at s3://filebase-fixtures/1.1/good-objects/minimal_no_content has VALID STRUCTURE (DIGESTS NOT CHECKED)
Object tree for None
[s3://filebase-fixtures/1.1/good-objects/minimal_no_content]
├── 0=ocfl_object_1.1
├── inventory.json
├── inventory.json.sha512
└── v1
    ├── inventory.json
    └── inventory.json.sha512
```

Where the Filebase bucket name is `filebase-fixtures` and the path within the bucket is
`1.1/good-objects/minimal_no_content`.

## Configuration with profiles

S3 API access can also be configured to allow multiple sets of credentials and endpoints through
the use of profiles in the configuration file `~/.aws/config`. For example:

```
[default]
aws_access_key_id=ACCESS_KEY1
aws_secret_access_key=SECRET_KEY1

[profile filebase]
endpoint_url=https://s3.filebase.io
aws_access_key_id=ACCESS_KEY2
aws_secret_access_key=SECRET_KEY2
```

The information in the `[profile filebase]` block is used when a `profile=filebase` query
parameter is added to the S3 path URL:

```
ocfl-py> ./ocfl-validate.py s3://filebase-fixtures/1.1/good-objects/minimal_no_content?profile=filebase
INFO:aiobotocore.credentials:Credentials found in config file: ~/.aws/config
INFO:botocore.configprovider:Found endpoint for s3 via: config_global.
OCFL v1.1 Object at s3://filebase-fixtures/1.1/good-objects/minimal_no_content?profile=filebase is VALID
```
