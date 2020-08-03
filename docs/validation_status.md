# Implementation status for errors and warnings

The following tables show the implementation status of all errors and warnings in the OCFL v1.0 specification, with links to the specification and into the code repository.

## Errors

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| E001 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E001a | OCFL Object root contains unexpected file: %s \[[ocfl/validator.py#L164](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L164)\] |
| | E001b | OCFL Object root contains unexpected directory: %s \[[ocfl/validator.py#L171](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L171)\] |
| | E001c | OCFL Object root contains unexpected entry that isn't a file or directory: %s \[[ocfl/validator.py#L173](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L173)\] |
| E002 | **Not in specification** | NOTE - E002 is redundant to more specific errors E003, E004, E005, E006. \[_Not implemented_\] |
| E003 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E003a | OCFL Object version declaration file is missing \[[ocfl/validator.py#L76](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L76)\] |
| | E003b | OCFL Object includes more that one file that looks like an object declaration (got %s) \[[ocfl/validator.py#L78](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L78)\] |
| | E003c | No OCFL Object to validate at path %s. The root of an OCFL Object must be a directory containing an object declaration \[[ocfl/validator.py#L71](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L71)\] |
| E007 | **Not in specification** | OCFL Object declaration file contents do not match file name without leading 0= (the 'dvalue') \[[ocfl/validator.py#L80](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L80)\] |
| E008 | **Not in specification** | OCFL Object %s inventory versions block does not contain any versions, there must be at least version 1 \[[ocfl/inventory_validator.py#L208](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L208)\] |
| E009 | **Not in specification** | OCFL Object %s inventory versions block does not contain v1 or a zero padded equivalent \[[ocfl/inventory_validator.py#L228](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L228)\] |
| E010 | **Not in specification** | OCFL Object %s inventory versions block includes an out-of-sequence version \[[ocfl/inventory_validator.py#L239](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L239)\] |
| E011 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L246](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L246)\] |
| E015 | **Not in specification** | OCFL Object version directory %s includes an illegal file (%s) \[[ocfl/validator.py#L255](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L255)\] |
| E018 | **Not in specification** | Content directory must not contain a forward slash (/) or be . or .. \[[ocfl/inventory_validator.py#L83](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L83)\] |
| E023 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E023a | OCFL Object %s inventory manifest refers to a file path that is not present in the object (%s) \[[ocfl/validator.py#L264](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L264)\] |
| | E023b | OCFL Object includes one or more files that are not mentioned in the %s inventory manifest (%s) \[[ocfl/validator.py#L282](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L282)\] |
| E024 | **Not in specification** | OCFL Object version %s content directory includes empty path %s \[[ocfl/validator.py#L246](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L246)\] |
| E025 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E025a | OCFL Object %s inventory manifest block includes a digest (%s) that doesn't have the correct form for the %s algorithm \[[ocfl/inventory_validator.py#L130](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L130)\] |
| E026 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E026a | OCFL Object %s inventory uses unknown digest type %s \[[ocfl/inventory_validator.py#L354](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L354)\] |
| E033 | **Not in specification** | OCFL Object %s inventory is not valid JSON (%s) \[[ocfl/validator.py#L117](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L117)\] |
| E034 | **Not in specification** | OCFL Object root inventory is missing \[[ocfl/validator.py#L84](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L84)\] |
| E036 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E036a | OCFL Object %s inventory missing `id` attribute \[[ocfl/inventory_validator.py#L63](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L63)\] |
| | E036b | OCFL Object %s inventory missing `type` attribute \[[ocfl/inventory_validator.py#L65](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L65)\] |
| | E036c | OCFL Object %s inventory missing `digestAlgorithm` attribute \[[ocfl/inventory_validator.py#L69](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L69)\] |
| | E036d | OCFL Object %s inventory missing `head` attribute \[[ocfl/inventory_validator.py#L96](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L96)\] |
| E037 | **Not in specification** | OCFL Object %s inventory `id` attribute is empty or badly formed \[[ocfl/inventory_validator.py#L59](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L59)\] |
| E038 | **Not in specification** | OCFL Object %s inventory `type` attribute has wrong value \[[ocfl/inventory_validator.py#L67](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L67)\] |
| E039 | **Not in specification** | OCFL Object %s inventory `digestAlgorithm` attribute not an allowed value (got '%s') \[[ocfl/inventory_validator.py#L78](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L78)\] |
| E040 | **Not in specification** | OCFL Object %s inventory head attribute doesn't match versions (got %s, expected %s) \[[ocfl/inventory_validator.py#L100](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L100)\] |
| E041 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E041a | OCFL Object %s inventory missing `manifest` attribute \[[ocfl/inventory_validator.py#L87](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L87)\] |
| | E041b | OCFL Object %s inventory missing `versions` attribute \[[ocfl/inventory_validator.py#L91](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L91)\] |
| | E041c | OCFL Object %s inventory manifest block is not a JSON object \[[ocfl/inventory_validator.py#L123](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L123)\] |
| E042 | **Not in specification** | OCFL Object %s inventory manifest includes invalid content path %s \[[ocfl/inventory_validator.py#L396](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L396)\] |
| E044 | **Not in specification** | OCFL Object %s inventory versions block is not a JSON object \[[ocfl/inventory_validator.py#L205](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L205)\] |
| E046 | **Not in specification** | OCFL Object root inventory describes versions %s but no corresponding version directory is present \[[ocfl/validator.py#L258](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L258)\] |
| E048 | **Not in specification** | OCFL Object %s inventory %s version block does not include a created date or it is malformed \[[ocfl/inventory_validator.py#L266](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L266)\] |
| | E048c | OCFL Object %s inventory %s version block does not include a state block \[[ocfl/inventory_validator.py#L282](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L282)\] |
| E049 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E049a | OCFL Object %s inventory %s version block created date SHOULD include a timezone designator \[[ocfl/inventory_validator.py#L274](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L274)\] |
| | E049b | OCFL Object %s inventory %s version block created date SHOULD be granular to the seconds level \[[ocfl/inventory_validator.py#L276](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L276)\] |
| | E049c | OCFL Object %s inventory %s version block has bad created date, must be IS8601 (%s) \[[ocfl/inventory_validator.py#L278](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L278)\] |
| | E049d | OCFL Object %s inventory %s version block created value is not a JSON string \[[ocfl/inventory_validator.py#L268](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L268)\] |
| E050 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E050a | OCFL Object %s inventory state refers to one or more digests that are not in the manifest (%s) \[[ocfl/inventory_validator.py#L343](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L343)\] |
| | E050b | OCFL Object %s inventory manifest refers to one or more digests that are not in any state (%s) \[[ocfl/inventory_validator.py#L346](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L346)\] |
| | E050c | OCFL Object %s inventory %s version block state block is not a JSON object \[[ocfl/inventory_validator.py#L315](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L315)\] |
| | E050d | OCFL Object %s inventory %s version state block includes a bad digest (%s) \[[ocfl/inventory_validator.py#L320](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L320)\] |
| | E050e | OCFL Object %s inventory %s version block state block value for digest %s is not list \[[ocfl/inventory_validator.py#L322](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L322)\] |
| | E050f | OCFL Object %s inventory version %s state includes digest value %s that is not listed in the manifest block \[[ocfl/inventory_validator.py#L328](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L328)\] |
| E051 | **Not in specification** | NOTE - E051 is essentially a processing instruction and can't be tested for. \[_Not implemented_\] |
| E052 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that starts or ends with / \[[ocfl/inventory_validator.py#L371](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L371)\] |
| E053 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that includes . .. or // \[[ocfl/inventory_validator.py#L366](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L366)\] |
| E054 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E054a | OCFL Object %s inventory %s version block has user key with value that isn't a JSON object \[[ocfl/inventory_validator.py#L292](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L292)\] |
| | E054b | OCFL Object %s inventory %s version block has user/name key with value that isn't a string \[[ocfl/inventory_validator.py#L295](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L295)\] |
| | E054c | OCFL Object %s inventory %s version block has user/address key with value that isn't a string \[[ocfl/inventory_validator.py#L299](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L299)\] |
| E056 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E056a | OCFL Object %s inventory includes a fixity key with value that isn't a JSON object \[[ocfl/inventory_validator.py#L158](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L158)\] |
| | E056b | OCFL Object %s inventory fixity block includes and unknown digest algorithm name %s \[[ocfl/inventory_validator.py#L166](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L166)\] |
| E057 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E057a | OCFL Object %s inventory fixity block entry for digest algorithm name %s is not a JSON object \[[ocfl/inventory_validator.py#L173](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L173)\] |
| | E057b | OCFL Object %s inventory fixity block entry for digest algorithm %s includes digest %s which has the wrong form \[[ocfl/inventory_validator.py#L179](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L179)\] |
| | E057c | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s is not a JSON list \[[ocfl/inventory_validator.py#L181](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L181)\] |
| | E057d | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s includes a content path %s that is not in the manifest \[[ocfl/inventory_validator.py#L194](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L194)\] |
| E058 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E058a | OCFL Object %s inventory is missing sidecar digest file at %s \[[ocfl/validator.py#L128](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L128)\] |
| | E058b | Cannot extract digest type from inventory digest file name %s \[[ocfl/validator.py#L151](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L151)\] |
| E060 | **Not in specification** | Mismatch between actual and recorded inventory digests for %s (calcuated %s but read %s from %s) \[[ocfl/validator.py#L147](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L147)\] |
| E061 | **Not in specification** | Cannot extract digest from inventory digest file (%s) \[[ocfl/validator.py#L149](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L149)\] |
| E064 | **Not in specification** | Object root inventory and copy in last version MUST be identical but are not (%s and %s) \[[ocfl/validator.py#L211](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L211)\] |
| E066 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E066a | OCFL Object inventory for %s doesn't have a subset of version blocks of inventory for %s \[[ocfl/inventory_validator.py#L405](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L405)\] |
| | E066b | OCFL Object inventory manifest for %s in %s doesn't have a subset of manifest entries of inventory for %s \[[ocfl/inventory_validator.py#L413](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L413)\] |
| | E066c | OCFL Object %s inventory %s version block has no state description \[[ocfl/inventory_validator.py#L418](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L418)\] |
| E067 | **Not in specification** | OCFL Object extensions direct contains an unexpected non-directory entry: %s \[[ocfl/validator.py#L189](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L189)\] |
| E090 | **Not in specification** | NOTE - E090 is essentially a processing instruction and can't be tested for. \[_Not implemented_\] |
| E091 | **Not in specification** | OCFL Object %s inventory manifest file list for digest %s is not a JSON array \[_Not implemented_\] |
| E092 | **Not in specification** | OCFL Object %s inventory manifest has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocfl/inventory_validator.py#L132](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L132) [ocfl/validator.py#L269](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L269)\] |
| E093 | **Not in specification** | OCFL Object %s inventory fixity block for digest algorithm %s has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocfl/validator.py#L279](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L279)\] |
| E094 | **Not in specification** | OCFL Object %s inventory %s version block has message key with value that isn't a string \[[ocfl/inventory_validator.py#L286](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L286)\] |
| E095 | **Not in specification** | OCFL Object %s inventory version %s state has logical path %s used as both a directory and a file path. \[[ocfl/inventory_validator.py#L334](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L334)\] |
| E096 | **Not in specification** | OCFL Object %s inventory manifest block includes digest %s more than once with different normalizations \[[ocfl/inventory_validator.py#L138](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L138)\] |
| E097 | **Not in specification** | OCFL Object %s inventory fixity block for digest algorithm %s, includes digest %s more than once with different normalizations \[[ocfl/inventory_validator.py#L189](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L189)\] |
| E099 | **Not in specification** | OCFL Object %s inventory manifest content path %s includes invalid element ., .., or empty (//). \[[ocfl/inventory_validator.py#L390](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L390)\] |
| E100 | **Not in specification** | OCFL Object %s inventory manifest content path %s must not begin or end with /. \[[ocfl/inventory_validator.py#L383](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L383)\] |
| E101 | **Not in specification** | OCFL Object %s inventory manifest content path %s used as both a directory and a file path. \[[ocfl/inventory_validator.py#L147](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L147)\] |

## Warnings

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| W001 | **Not in specification** | OCFL Object %s inventory version numbers SHOULD NOT be zero-padded \[[ocfl/inventory_validator.py#L231](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L231)\] |
| W002 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain any directory except the designated content directory (found %s) \[[ocfl/validator.py#L253](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L253)\] |
| W003 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain an empty content directory \[[ocfl/validator.py#L251](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L251)\] |
| W004 | **Not in specification** | OCFL Object %s inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm \[[ocfl/inventory_validator.py#L75](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L75)\] |
| W005 | **Not in specification** | OCFL Object %s inventory id SHOULD be a URI (got %s) \[[ocfl/inventory_validator.py#L61](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L61)\] |
| W007 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | W007a | OCFL Object %s inventory %s version block SHOULD include a message key \[[ocfl/inventory_validator.py#L284](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L284)\] |
| | W007b | OCFL Object %s inventory %s version block SHOULD include a user key \[[ocfl/inventory_validator.py#L288](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L288)\] |
| W008 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD have an address \[[ocfl/inventory_validator.py#L297](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L297)\] |
| W009 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD be a mailto: or person identifier URI \[[ocfl/inventory_validator.py#L301](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L301)\] |
| W010 | **Not in specification** | OCFL Object %s SHOULD have an inventory file but does not \[[ocfl/validator.py#L200](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L200)\] |
| W011 | **Not in specification** | OCFL Object version metadata '%s' for %s in %s inventory does not match that in %s inventory \[[ocfl/inventory_validator.py#L424](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L424)\] |
| W013 | **Not in specification** | OCFL Object includes unregistered extension directory '%s' \[[ocfl/validator.py#L187](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L187)\] |

_Generated by `extract_codes.py` at 2020-08-03 10:12:18.864719_