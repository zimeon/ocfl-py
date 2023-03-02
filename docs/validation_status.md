# Implementation status for errors and warnings

The following tables show the implementation status of all errors and warnings in the OCFL v1.0 specification, with links to the specification and into the code repository.

## Errors

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| E001 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E001a | OCFL Object root contains unexpected file: %s \[[ocfl/validator.py#L203](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L203)\] |
| | E001b | OCFL Object root contains unexpected directory: %s \[[ocfl/validator.py#L214](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L214)\] |
| | E001c | OCFL Object root contains unexpected entry that isn't a file or directory: %s \[[ocfl/validator.py#L216](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L216)\] |
| E002 | **Not in specification** | NOTE - E002 is redundant to more specific errors E003, E004, E005, E006. \[_Not implemented_\] |
| E003 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E003a | OCFL Object version declaration file is missing (assuming version %s) \[[ocfl/validator.py#L92](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L92)\] |
| | E003b | OCFL Object includes more that one file that looks like an object declaration (got %s), using version %s \[[ocfl/validator.py#L113](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L113)\] |
| | E003c | OCFL Object includes one or move object declaration files (starting 0=) but no valid version number could be extracted from any of them (assuming version %s) \[[ocfl/validator.py#L109](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L109)\] |
| | E003d | OCFL Storage Root hierarchy includes directory %s with more that one file that looks like an object declaration, ignoring \[[ocfl/store.py#L168](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L168)\] |
| | E003e | No OCFL Object to validate at path %s. The root of an OCFL Object must be a directory containing an object declaration \[[ocfl/validator.py#L86](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L86)\] |
| E004 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E004a | OCFL Storage Root hierarchy includes directory %s with an object declaration giving unknown version %s, ignoring \[[ocfl/store.py#L175](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L175)\] |
| | E004b | OCFL Storage Root hierarchy includes directory %s with an unrecognized object declaration %s, ignoring \[[ocfl/store.py#L177](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L177)\] |
| E006 | **Not in specification** | The OCFL object conformance declaration filename must be 0=ocfl_object_, followed by the OCFL specification version number, got %s instead \[[ocfl/validator.py#L103](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L103)\] |
| E007 | **Not in specification** | OCFL Object declaration file %s contents do not match file name without leading 0= (the 'dvalue') \[[ocfl/validator.py#L107](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L107)\] |
| E008 | **Not in specification** | OCFL Object %s inventory versions block does not contain any versions, there must be at least version 1 \[[ocfl/inventory_validator.py#L252](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L252)\] |
| E009 | **Not in specification** | OCFL Object %s inventory versions block does not contain v1 or a zero padded equivalent \[[ocfl/inventory_validator.py#L272](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L272)\] |
| E010 | **Not in specification** | OCFL Object %s inventory versions block includes an out-of-sequence version \[[ocfl/inventory_validator.py#L283](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L283)\] |
| E011 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L290](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L290)\] |
| E015 | **Not in specification** | OCFL Object version directory %s includes an illegal file (%s) \[[ocfl/validator.py#L357](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L357)\] |
| E017 | **Not in specification** | OCFL Object %s inventory contentDirectory must be a string and must not contain a forward slash (/) \[[ocfl/inventory_validator.py#L112](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L112)\] |
| E018 | **Not in specification** | OCFL Object %s inventory contentDirectory must not be either . or .. \[[ocfl/inventory_validator.py#L114](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L114)\] |
| E023 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E023a | OCFL Object includes one or more files that are not mentioned in the  %s inventory manifest (%s) \[[ocfl/validator.py#L395](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L395)\] |
| | E023b | OCFL Object %s manifest does not include files listed in previous version manifests (%s) \[[ocfl/validator.py#L289](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L289)\] |
| E024 | **Not in specification** | OCFL Object version %s content directory includes empty path %s \[[ocfl/validator.py#L348](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L348)\] |
| E025 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E025a | OCFL Object %s inventory manifest block includes a digest (%s) that doesn't have the correct form for the %s algorithm \[[ocfl/inventory_validator.py#L171](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L171)\] |
| E026 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E026a | OCFL Object %s inventory uses unknown digest type %s \[[ocfl/inventory_validator.py#L413](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L413)\] |
| E033 | **Not in specification** | OCFL Object %s inventory is not valid JSON (%s) \[[ocfl/object.py#L542](https://github.com/zimeon/ocfl-py/blob/main/ocfl/object.py#L542) [ocfl/validator.py#L155](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L155)\] |
| E036 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E036a | OCFL Object %s inventory missing `id` attribute \[[ocfl/inventory_validator.py#L82](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L82)\] |
| | E036b | OCFL Object %s inventory missing `type` attribute \[[ocfl/inventory_validator.py#L84](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L84)\] |
| | E036c | OCFL Object %s inventory missing `digestAlgorithm` attribute \[[ocfl/inventory_validator.py#L98](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L98)\] |
| | E036d | OCFL Object %s inventory missing `head` attribute \[[ocfl/inventory_validator.py#L129](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L129)\] |
| E037 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E037a | OCFL Object %s inventory `id` attribute is empty or badly formed \[[ocfl/inventory_validator.py#L74](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L74)\] |
| | E037b | OCFL Object %s inventory id `%s` does not match the value in the root inventory `%s` \[[ocfl/validator.py#L279](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L279)\] |
| E038 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E038a | OCFL Object %s inventory `type` attribute has wrong value (expected %s, got %s) \[[ocfl/inventory_validator.py#L96](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L96)\] |
| | E038b | OCFL Object %s inventory `type` attribute does not look like a valid specification URI (got %s), will proceed as if using version %s \[[ocfl/inventory_validator.py#L90](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L90)\] |
| | E038c | OCFL Object %s inventory `type` attribute has an unsupported specification version number (%s), will proceed as if using version %s \[[ocfl/inventory_validator.py#L94](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L94)\] |
| E039 | **Not in specification** | OCFL Object %s inventory `digestAlgorithm` attribute not an allowed value (got '%s') \[[ocfl/inventory_validator.py#L107](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L107)\] |
| E040 | **Not in specification** | OCFL Object %s inventory head attribute doesn't match versions (got %s, expected %s) \[[ocfl/inventory_validator.py#L133](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L133)\] |
| E041 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E041a | OCFL Object %s inventory missing `manifest` attribute \[[ocfl/inventory_validator.py#L119](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L119)\] |
| | E041b | OCFL Object %s inventory missing `versions` attribute \[[ocfl/inventory_validator.py#L124](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L124)\] |
| | E041c | OCFL Object %s inventory manifest block is not a JSON object \[[ocfl/inventory_validator.py#L164](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L164)\] |
| E042 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E042a | OCFL Object %s inventory manifest includes invalid content path %s \[[ocfl/inventory_validator.py#L448](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L448)\] |
| | E042b | OCFL Object %s inventory manifest includes content path %s with invalid version directory \[[ocfl/inventory_validator.py#L394](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L394)\] |
| E044 | **Not in specification** | OCFL Object %s inventory versions block is not a JSON object \[[ocfl/inventory_validator.py#L249](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L249)\] |
| E046 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E046a | OCFL Object root inventory describes version %s but no corresponding version directory is present \[[ocfl/validator.py#L359](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L359)\] |
| | E046b | OCFL Object includes directory %s that looks like a version directory but isn't a valid version in the inventory \[[ocfl/validator.py#L211](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L211)\] |
| E048 | **Not in specification** | OCFL Object %s inventory %s version block does not include a created date or it is malformed \[[ocfl/inventory_validator.py#L310](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L310)\] |
| | E048c | OCFL Object %s inventory %s version block does not include a state block \[[ocfl/inventory_validator.py#L326](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L326)\] |
| E049 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E049a | OCFL Object %s inventory %s version block created date SHOULD include a timezone designator \[[ocfl/inventory_validator.py#L318](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L318)\] |
| | E049b | OCFL Object %s inventory %s version block created date SHOULD be granular to the seconds level \[[ocfl/inventory_validator.py#L320](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L320)\] |
| | E049c | OCFL Object %s inventory %s version block has bad created date, must be IS8601 (%s) \[[ocfl/inventory_validator.py#L322](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L322)\] |
| | E049d | OCFL Object %s inventory %s version block created value is not a JSON string \[[ocfl/inventory_validator.py#L312](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L312)\] |
| E050 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E050a | OCFL Object %s inventory state refers to one or more digests that are not in the manifest (%s) \[[ocfl/inventory_validator.py#L402](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L402)\] |
| | E050c | OCFL Object %s inventory %s version block state block is not a JSON object \[[ocfl/inventory_validator.py#L359](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L359)\] |
| | E050d | OCFL Object %s inventory %s version state block includes a bad digest (%s) \[[ocfl/inventory_validator.py#L364](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L364)\] |
| | E050e | OCFL Object %s inventory %s version block state block value for digest %s is not list \[[ocfl/inventory_validator.py#L366](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L366)\] |
| | E050f | OCFL Object %s inventory version %s state includes digest value %s that is not listed in the manifest block \[[ocfl/inventory_validator.py#L375](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L375)\] |
| E051 | **Not in specification** | NOTE - E051 is essentially a processing instruction and can't be tested for. \[_Not implemented_\] |
| E052 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that starts or ends with / \[[ocfl/inventory_validator.py#L430](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L430)\] |
| E053 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that includes . .. or // \[[ocfl/inventory_validator.py#L425](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L425)\] |
| E054 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E054a | OCFL Object %s inventory %s version block has user key with value that isn't a JSON object \[[ocfl/inventory_validator.py#L336](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L336)\] |
| | E054b | OCFL Object %s inventory %s version block has user/name key with value that isn't a string \[[ocfl/inventory_validator.py#L339](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L339)\] |
| | E054c | OCFL Object %s inventory %s version block has user/address key with value that isn't a string \[[ocfl/inventory_validator.py#L343](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L343)\] |
| E056 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E056a | OCFL Object %s inventory includes a fixity key with value that isn't a JSON object \[[ocfl/inventory_validator.py#L202](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L202)\] |
| | E056b | OCFL Object %s inventory fixity block includes a key that is not a known digest algorithm name: %s \[[ocfl/inventory_validator.py#L210](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L210)\] |
| E057 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E057a | OCFL Object %s inventory fixity block entry for digest algorithm name %s is not a JSON object \[[ocfl/inventory_validator.py#L217](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L217)\] |
| | E057b | OCFL Object %s inventory fixity block entry for digest algorithm %s includes digest %s which has the wrong form \[[ocfl/inventory_validator.py#L223](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L223)\] |
| | E057c | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s is not a JSON list \[[ocfl/inventory_validator.py#L225](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L225)\] |
| | E057d | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s includes a content path %s that is not in the manifest \[[ocfl/inventory_validator.py#L238](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L238)\] |
| E058 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E058a | OCFL Object %s inventory is missing sidecar digest file at %s \[[ocfl/validator.py#L167](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L167)\] |
| | E058b | Cannot extract digest type from inventory digest file name %s \[[ocfl/validator.py#L190](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L190)\] |
| E060 | **Not in specification** | Mismatch between actual and recorded inventory digests for %s (calculated %s but read %s from %s) \[[ocfl/validator.py#L186](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L186)\] |
| E061 | **Not in specification** | Cannot extract digest from inventory digest file (%s) \[[ocfl/validator.py#L188](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L188)\] |
| E063 | **Not in specification** | OCFL Object root inventory is missing \[[ocfl/validator.py#L117](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L117)\] |
| E064 | **Not in specification** | Object root inventory and copy in last version MUST be identical but are not (%s and %s) \[[ocfl/validator.py#L261](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L261)\] |
| E066 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E066a | OCFL Object inventory for %s doesn't have a subset of version blocks of inventory for %s \[[ocfl/inventory_validator.py#L472](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L472)\] |
| | E066b | OCFL Object %s inventory %s version state doesn't have same logical paths as same version in %s inventory (paths %s only in %s inventory) \[[ocfl/inventory_validator.py#L492](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L492) [ocfl/inventory_validator.py#L494](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L494)\] |
| | E066c | OCFL Object %s inventory %s version state has logical path %s that maps to content path %s, but in %s inventory it maps to content path %s \[[ocfl/inventory_validator.py#L499](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L499)\] |
| | E066d | OCFL Object %s inventory %s version state has digest %s (mapping to logical files %s) that does not appear in the %s inventory \[[ocfl/inventory_validator.py#L528](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L528)\] |
| | E066e | OCFL Object %s inventory %s version state has digest %s (mapping to logical files %s) that does not appear in the %s inventory \[[ocfl/inventory_validator.py#L531](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L531)\] |
| E067 | **Not in specification** | OCFL Object extensions direct contains an unexpected non-directory entry: %s \[[ocfl/validator.py#L232](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L232)\] |
| E072 | **Not in specification** | OCFL storage root hierarchy include directory %s with at least one file but no object declaration. Such additional files are not allowed \[[ocfl/store.py#L179](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L179)\] |
| E073 | **Not in specification** | OCFL storage root hierarchy contains an empty directory: %s \[[ocfl/store.py#L161](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L161)\] |
| E086 | **Not in specification** | OCFL Storage Root extensions direct contains an unexpected non-directory entry: %s \[[ocfl/store.py#L195](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L195)\] |
| E087 | **Not in specification** | NOTE - E087 is a processing instruction and can't be tested for \[_Not implemented_\] |
| E088 | **Not in specification** | NOTE - E088 is redundant to more specific errors E072 and E073 \[_Not implemented_\] |
| E090 | **Not in specification** | NOTE - E090 is a processing instruction and can't be tested for \[_Not implemented_\] |
| E091 | **Not in specification** | OCFL Object %s inventory manifest file list for digest %s is not a JSON array \[_Not implemented_\] |
| E092 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L173](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L173)\] |
| | E092a | OCFL Object %s inventory manifest using digest algorithm %s has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocfl/validator.py#L385](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L385) [ocfl/validator.py#L390](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L390)\] |
| | E092b | OCFL Object %s inventory manifest refers to a file path that is not present in the object (%s) \[[ocfl/validator.py#L380](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L380)\] |
| E093 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E093a | OCFL Object %s inventory fixity block for digest algorithm %s has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocfl/validator.py#L388](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L388) [ocfl/validator.py#L391](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L391)\] |
| | E093b | OCFL Object %s inventory fixity block for digest algorithm %s has digest %s for a file %s which does not exist in the object \[[ocfl/validator.py#L374](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L374)\] |
| E094 | **Not in specification** | OCFL Object %s inventory %s version block has message key with value that isn't a string \[[ocfl/inventory_validator.py#L330](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L330)\] |
| E095 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E095a | OCFL Object %s inventory version %s state has logical path %s used more than once \[[ocfl/inventory_validator.py#L370](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L370)\] |
| | E095b | OCFL Object %s inventory version %s state has logical path %s used as both a directory and a file path. \[[ocfl/inventory_validator.py#L381](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L381)\] |
| E096 | **Not in specification** | OCFL Object %s inventory manifest block includes digest %s more than once with different normalizations \[[ocfl/inventory_validator.py#L179](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L179)\] |
| E097 | **Not in specification** | OCFL Object %s inventory fixity block for digest algorithm %s, includes digest %s more than once with different normalizations \[[ocfl/inventory_validator.py#L233](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L233)\] |
| E099 | **Not in specification** | OCFL Object %s inventory manifest content path %s includes invalid element ., .., or empty (//). \[[ocfl/inventory_validator.py#L453](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L453)\] |
| E100 | **Not in specification** | OCFL Object %s inventory manifest content path %s must not begin or end with /. \[[ocfl/inventory_validator.py#L444](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L444)\] |
| E101 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E101a | OCFL Object %s inventory manifest content path %s is repeated \[[ocfl/inventory_validator.py#L457](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L457)\] |
| | E101b | OCFL Object %s inventory manifest content path %s used as both a directory and a file path \[[ocfl/inventory_validator.py#L189](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L189)\] |
| E103 | **Not in specification** | OCFL Object %s inventory conforms to specification version %s which is an earlier version than the %s inventory which conforms to specification version %s \[[ocfl/validator.py#L321](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L321)\] |
| E107 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L405](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L405)\] |
| E111 | **Not in specification** | OCFL Object %s inventory includes a fixity key with value that isn't a JSON object \[_Not implemented_\] |
| E999 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L86](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L86)\] |

## Warnings

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| W001 | **Not in specification** | OCFL Object %s inventory version numbers SHOULD NOT be zero-padded \[[ocfl/inventory_validator.py#L275](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L275)\] |
| W002 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain any directory except the designated content directory (found %s) \[[ocfl/validator.py#L355](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L355)\] |
| W003 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain an empty content directory \[[ocfl/validator.py#L353](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L353)\] |
| W004 | **Not in specification** | OCFL Object %s inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm \[[ocfl/inventory_validator.py#L104](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L104)\] |
| W005 | **Not in specification** | OCFL Object %s inventory id SHOULD be a URI (got %s) \[[ocfl/inventory_validator.py#L79](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L79)\] |
| W007 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | W007a | OCFL Object %s inventory %s version block SHOULD include a message key \[[ocfl/inventory_validator.py#L328](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L328)\] |
| | W007b | OCFL Object %s inventory %s version block SHOULD include a user key \[[ocfl/inventory_validator.py#L332](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L332)\] |
| W008 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD have an address \[[ocfl/inventory_validator.py#L341](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L341)\] |
| W009 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD be a mailto: or person identifier URI \[[ocfl/inventory_validator.py#L345](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L345)\] |
| W010 | **Not in specification** | OCFL Object %s SHOULD have an inventory file but does not \[[ocfl/validator.py#L253](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L253)\] |
| W011 | **Not in specification** | OCFL Object version metadata '%s' for %s in %s inventory does not match that in %s inventory \[[ocfl/inventory_validator.py#L507](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L507)\] |
| W013 | **Not in specification** | OCFL Object includes unregistered extension directory '%s' \[[ocfl/validator.py#L230](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L230)\] |
| W901 | **Not in specification** | OCFL Storage Root includes unregistered extension directory '%s' \[[ocfl/store.py#L193](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L193)\] |

_Generated by `extract_codes.py` at 2023-03-02 15:49:04.348263_