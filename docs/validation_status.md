# Implementation status for errors and warnings

The following tables show the implementation status of all errors and warnings in the OCFL v1.0 specification, with links to the specification and into the code repository.

## Errors

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| E001 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E001a | OCFL Object root contains unexpected file: %s \[[ocfl/validator.py#L186](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L186)\] |
| | E001b | OCFL Object root contains unexpected directory: %s \[[ocfl/validator.py#L197](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L197)\] |
| | E001c | OCFL Object root contains unexpected entry that isn't a file or directory: %s \[[ocfl/validator.py#L199](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L199)\] |
| E002 | **Not in specification** | NOTE - E002 is redundant to more specific errors E003, E004, E005, E006. \[_Not implemented_\] |
| E003 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E003a | OCFL Object version declaration file is missing \[[ocfl/validator.py#L87](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L87)\] |
| | E003b | OCFL Object includes more that one file that looks like an object declaration (got %s) \[[ocfl/validator.py#L89](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L89)\] |
| | E003c | No OCFL Object to validate at path %s. The root of an OCFL Object must be a directory containing an object declaration \[[ocfl/validator.py#L82](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L82)\] |
| | E003d | OCFL Storage Root hierarchy includes directory %s with more that one file that looks like an object declaration, ignoring \[[ocfl/store.py#L168](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L168)\] |
| E004 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E004a | OCFL Storage Root hierarchy includes directory %s with an object declaration giving unknown version %s, ignoring \[[ocfl/store.py#L175](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L175)\] |
| | E004b | OCFL Storage Root hierarchy includes directory %s with an unrecognized object declaration %s, ignoring \[[ocfl/store.py#L177](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L177)\] |
| E006 | **Not in specification** | The OCFL object conformance declaration filename must be 0=ocfl_object_, followed by the OCFL specification version number, got %s instead \[[ocfl/validator.py#L99](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L99)\] |
| E007 | **Not in specification** | OCFL Object declaration file contents do not match file name without leading 0= (the 'dvalue') \[[ocfl/validator.py#L91](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L91)\] |
| E008 | **Not in specification** | OCFL Object %s inventory versions block does not contain any versions, there must be at least version 1 \[[ocfl/inventory_validator.py#L232](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L232)\] |
| E009 | **Not in specification** | OCFL Object %s inventory versions block does not contain v1 or a zero padded equivalent \[[ocfl/inventory_validator.py#L252](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L252)\] |
| E010 | **Not in specification** | OCFL Object %s inventory versions block includes an out-of-sequence version \[[ocfl/inventory_validator.py#L263](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L263)\] |
| E011 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L270](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L270)\] |
| E015 | **Not in specification** | OCFL Object version directory %s includes an illegal file (%s) \[[ocfl/validator.py#L322](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L322)\] |
| E017 | **Not in specification** | OCFL Object %s inventory contentDirectory must be a string and must not contain a forward slash (/) \[[ocfl/inventory_validator.py#L95](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L95)\] |
| E018 | **Not in specification** | OCFL Object %s inventory contentDirectory must not be either . or .. \[[ocfl/inventory_validator.py#L97](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L97)\] |
| E023 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E023a | OCFL Object includes one or more files that are not mentioned in the  %s inventory manifest (%s) \[[ocfl/validator.py#L360](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L360)\] |
| | E023b | OCFL Object %s manifest does not include files listed in previous version manifests (%s) \[[ocfl/validator.py#L261](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L261)\] |
| E024 | **Not in specification** | OCFL Object version %s content directory includes empty path %s \[[ocfl/validator.py#L313](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L313)\] |
| E025 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E025a | OCFL Object %s inventory manifest block includes a digest (%s) that doesn't have the correct form for the %s algorithm \[[ocfl/inventory_validator.py#L154](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L154)\] |
| E026 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E026a | OCFL Object %s inventory uses unknown digest type %s \[[ocfl/inventory_validator.py#L393](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L393)\] |
| E033 | **Not in specification** | OCFL Object %s inventory is not valid JSON (%s) \[[ocfl/validator.py#L138](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L138) [ocfl/object.py#L544](https://github.com/zimeon/ocfl-py/blob/main/ocfl/object.py#L544)\] |
| E036 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E036a | OCFL Object %s inventory missing `id` attribute \[[ocfl/inventory_validator.py#L75](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L75)\] |
| | E036b | OCFL Object %s inventory missing `type` attribute \[[ocfl/inventory_validator.py#L77](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L77)\] |
| | E036c | OCFL Object %s inventory missing `digestAlgorithm` attribute \[[ocfl/inventory_validator.py#L81](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L81)\] |
| | E036d | OCFL Object %s inventory missing `head` attribute \[[ocfl/inventory_validator.py#L112](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L112)\] |
| E037 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E037a | OCFL Object %s inventory `id` attribute is empty or badly formed \[[ocfl/inventory_validator.py#L67](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L67)\] |
| | E037b | OCFL Object %s inventory id `%s` does not match the value in the root inventory `%s` \[[ocfl/validator.py#L251](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L251)\] |
| E038 | **Not in specification** | OCFL Object %s inventory `type` attribute has wrong value \[[ocfl/inventory_validator.py#L79](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L79)\] |
| E039 | **Not in specification** | OCFL Object %s inventory `digestAlgorithm` attribute not an allowed value (got '%s') \[[ocfl/inventory_validator.py#L90](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L90)\] |
| E040 | **Not in specification** | OCFL Object %s inventory head attribute doesn't match versions (got %s, expected %s) \[[ocfl/inventory_validator.py#L116](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L116)\] |
| E041 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E041a | OCFL Object %s inventory missing `manifest` attribute \[[ocfl/inventory_validator.py#L102](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L102)\] |
| | E041b | OCFL Object %s inventory missing `versions` attribute \[[ocfl/inventory_validator.py#L107](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L107)\] |
| | E041c | OCFL Object %s inventory manifest block is not a JSON object \[[ocfl/inventory_validator.py#L147](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L147)\] |
| E042 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E042a | OCFL Object %s inventory manifest includes invalid content path %s \[[ocfl/inventory_validator.py#L428](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L428)\] |
| | E042b | OCFL Object %s inventory manifest includes content path %s with invalid version directory \[[ocfl/inventory_validator.py#L374](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L374)\] |
| E044 | **Not in specification** | OCFL Object %s inventory versions block is not a JSON object \[[ocfl/inventory_validator.py#L229](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L229)\] |
| E046 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E046a | OCFL Object root inventory describes version %s but no corresponding version directory is present \[[ocfl/validator.py#L324](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L324)\] |
| | E046b | OCFL Object includes directory %s that looks like a version directory but isn't a valid version in the inventory \[[ocfl/validator.py#L194](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L194)\] |
| E048 | **Not in specification** | OCFL Object %s inventory %s version block does not include a created date or it is malformed \[[ocfl/inventory_validator.py#L290](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L290)\] |
| | E048c | OCFL Object %s inventory %s version block does not include a state block \[[ocfl/inventory_validator.py#L306](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L306)\] |
| E049 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E049a | OCFL Object %s inventory %s version block created date SHOULD include a timezone designator \[[ocfl/inventory_validator.py#L298](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L298)\] |
| | E049b | OCFL Object %s inventory %s version block created date SHOULD be granular to the seconds level \[[ocfl/inventory_validator.py#L300](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L300)\] |
| | E049c | OCFL Object %s inventory %s version block has bad created date, must be IS8601 (%s) \[[ocfl/inventory_validator.py#L302](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L302)\] |
| | E049d | OCFL Object %s inventory %s version block created value is not a JSON string \[[ocfl/inventory_validator.py#L292](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L292)\] |
| E050 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E050a | OCFL Object %s inventory state refers to one or more digests that are not in the manifest (%s) \[[ocfl/inventory_validator.py#L382](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L382)\] |
| | E050c | OCFL Object %s inventory %s version block state block is not a JSON object \[[ocfl/inventory_validator.py#L339](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L339)\] |
| | E050d | OCFL Object %s inventory %s version state block includes a bad digest (%s) \[[ocfl/inventory_validator.py#L344](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L344)\] |
| | E050e | OCFL Object %s inventory %s version block state block value for digest %s is not list \[[ocfl/inventory_validator.py#L346](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L346)\] |
| | E050f | OCFL Object %s inventory version %s state includes digest value %s that is not listed in the manifest block \[[ocfl/inventory_validator.py#L355](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L355)\] |
| E051 | **Not in specification** | NOTE - E051 is essentially a processing instruction and can't be tested for. \[_Not implemented_\] |
| E052 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that starts or ends with / \[[ocfl/inventory_validator.py#L410](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L410)\] |
| E053 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that includes . .. or // \[[ocfl/inventory_validator.py#L405](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L405)\] |
| E054 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E054a | OCFL Object %s inventory %s version block has user key with value that isn't a JSON object \[[ocfl/inventory_validator.py#L316](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L316)\] |
| | E054b | OCFL Object %s inventory %s version block has user/name key with value that isn't a string \[[ocfl/inventory_validator.py#L319](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L319)\] |
| | E054c | OCFL Object %s inventory %s version block has user/address key with value that isn't a string \[[ocfl/inventory_validator.py#L323](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L323)\] |
| E056 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E056a | OCFL Object %s inventory includes a fixity key with value that isn't a JSON object \[[ocfl/inventory_validator.py#L182](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L182)\] |
| | E056b | OCFL Object %s inventory fixity block includes and unknown digest algorithm name %s \[[ocfl/inventory_validator.py#L190](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L190)\] |
| E057 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E057a | OCFL Object %s inventory fixity block entry for digest algorithm name %s is not a JSON object \[[ocfl/inventory_validator.py#L197](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L197)\] |
| | E057b | OCFL Object %s inventory fixity block entry for digest algorithm %s includes digest %s which has the wrong form \[[ocfl/inventory_validator.py#L203](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L203)\] |
| | E057c | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s is not a JSON list \[[ocfl/inventory_validator.py#L205](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L205)\] |
| | E057d | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s includes a content path %s that is not in the manifest \[[ocfl/inventory_validator.py#L218](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L218)\] |
| E058 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E058a | OCFL Object %s inventory is missing sidecar digest file at %s \[[ocfl/validator.py#L150](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L150)\] |
| | E058b | Cannot extract digest type from inventory digest file name %s \[[ocfl/validator.py#L173](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L173)\] |
| E060 | **Not in specification** | Mismatch between actual and recorded inventory digests for %s (calculated %s but read %s from %s) \[[ocfl/validator.py#L169](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L169)\] |
| E061 | **Not in specification** | Cannot extract digest from inventory digest file (%s) \[[ocfl/validator.py#L171](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L171)\] |
| E063 | **Not in specification** | OCFL Object root inventory is missing \[[ocfl/validator.py#L105](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L105)\] |
| E064 | **Not in specification** | Object root inventory and copy in last version MUST be identical but are not (%s and %s) \[[ocfl/validator.py#L237](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L237)\] |
| E066 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E066a | OCFL Object inventory for %s doesn't have a subset of version blocks of inventory for %s \[[ocfl/inventory_validator.py#L452](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L452)\] |
| | E066b | OCFL Object inventory manifest for %s in %s doesn't have a subset of manifest entries of inventory for %s \[[ocfl/inventory_validator.py#L468](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L468)\] |
| | E066c | OCFL Object %s inventory %s version state has file %s that maps to different content files (%s) than in the %s inventory (%s) \[[ocfl/inventory_validator.py#L473](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L473)\] |
| | E066d | OCFL Object %s inventory %s version state has digest %s (mapping to logical files %s) that does not appear in the %s inventory \[[ocfl/inventory_validator.py#L501](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L501)\] |
| | E066e | OCFL Object %s inventory %s version state has digest %s (mapping to logical files %s) that does not appear in the %s inventory \[[ocfl/inventory_validator.py#L504](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L504)\] |
| E067 | **Not in specification** | OCFL Object extensions direct contains an unexpected non-directory entry: %s \[[ocfl/validator.py#L215](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L215)\] |
| E072 | **Not in specification** | OCFL storage root hierarchy include directory %s with at least one file but no object declaration. Such additional files are not allowed \[[ocfl/store.py#L179](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L179)\] |
| E073 | **Not in specification** | OCFL storage root hierarchy contains an empty directory: %s \[[ocfl/store.py#L161](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L161)\] |
| E086 | **Not in specification** | OCFL Storage Root extensions direct contains an unexpected non-directory entry: %s \[[ocfl/store.py#L195](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L195)\] |
| E087 | **Not in specification** | NOTE - E087 is a processing instruction and can't be tested for. \[_Not implemented_\] |
| E088 | **Not in specification** | NOTE - E088 is redundant to more specific errors E072 and E073 \[_Not implemented_\] |
| E090 | **Not in specification** | NOTE - E090 is a processing instruction and can't be tested for. \[_Not implemented_\] |
| E091 | **Not in specification** | OCFL Object %s inventory manifest file list for digest %s is not a JSON array \[_Not implemented_\] |
| E092 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L156](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L156)\] |
| | E092a | OCFL Object %s inventory manifest using digest algorithm %s has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocfl/validator.py#L355](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L355) [ocfl/validator.py#L350](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L350)\] |
| | E092b | OCFL Object %s inventory manifest refers to a file path that is not present in the object (%s) \[[ocfl/validator.py#L345](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L345)\] |
| E093 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E093a | OCFL Object %s inventory fixity block for digest algorithm %s has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocfl/validator.py#L356](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L356) [ocfl/validator.py#L353](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L353)\] |
| | E093b | OCFL Object %s inventory fixity block for digest algorithm %s has digest %s for a file %s which does not exist in the object \[[ocfl/validator.py#L339](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L339)\] |
| E094 | **Not in specification** | OCFL Object %s inventory %s version block has message key with value that isn't a string \[[ocfl/inventory_validator.py#L310](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L310)\] |
| E095 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E095a | OCFL Object %s inventory version %s state has logical path %s used more than once. \[[ocfl/inventory_validator.py#L350](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L350)\] |
| | E095b | OCFL Object %s inventory version %s state has logical path %s used as both a directory and a file path. \[[ocfl/inventory_validator.py#L361](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L361)\] |
| E096 | **Not in specification** | OCFL Object %s inventory manifest block includes digest %s more than once with different normalizations \[[ocfl/inventory_validator.py#L162](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L162)\] |
| E097 | **Not in specification** | OCFL Object %s inventory fixity block for digest algorithm %s, includes digest %s more than once with different normalizations \[[ocfl/inventory_validator.py#L213](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L213)\] |
| E099 | **Not in specification** | OCFL Object %s inventory manifest content path %s includes invalid element ., .., or empty (//). \[[ocfl/inventory_validator.py#L433](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L433)\] |
| E100 | **Not in specification** | OCFL Object %s inventory manifest content path %s must not begin or end with /. \[[ocfl/inventory_validator.py#L424](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L424)\] |
| E101 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E101a | OCFL Object %s inventory manifest content path %s is repeated. \[[ocfl/inventory_validator.py#L437](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L437)\] |
| | E101b | OCFL Object %s inventory manifest content path %s used as both a directory and a file path. \[[ocfl/inventory_validator.py#L172](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L172)\] |
| E107 | **Not in specification** | **Missing description** \[[ocfl/inventory_validator.py#L385](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L385)\] |

## Warnings

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| W001 | **Not in specification** | OCFL Object %s inventory version numbers SHOULD NOT be zero-padded \[[ocfl/inventory_validator.py#L255](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L255)\] |
| W002 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain any directory except the designated content directory (found %s) \[[ocfl/validator.py#L320](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L320)\] |
| W003 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain an empty content directory \[[ocfl/validator.py#L318](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L318)\] |
| W004 | **Not in specification** | OCFL Object %s inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm \[[ocfl/inventory_validator.py#L87](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L87)\] |
| W005 | **Not in specification** | OCFL Object %s inventory id SHOULD be a URI (got %s) \[[ocfl/inventory_validator.py#L72](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L72)\] |
| W007 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | W007a | OCFL Object %s inventory %s version block SHOULD include a message key \[[ocfl/inventory_validator.py#L308](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L308)\] |
| | W007b | OCFL Object %s inventory %s version block SHOULD include a user key \[[ocfl/inventory_validator.py#L312](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L312)\] |
| W008 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD have an address \[[ocfl/inventory_validator.py#L321](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L321)\] |
| W009 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD be a mailto: or person identifier URI \[[ocfl/inventory_validator.py#L325](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L325)\] |
| W010 | **Not in specification** | OCFL Object %s SHOULD have an inventory file but does not \[[ocfl/validator.py#L231](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L231)\] |
| W011 | **Not in specification** | OCFL Object version metadata '%s' for %s in %s inventory does not match that in %s inventory \[[ocfl/inventory_validator.py#L481](https://github.com/zimeon/ocfl-py/blob/main/ocfl/inventory_validator.py#L481)\] |
| W013 | **Not in specification** | OCFL Object includes unregistered extension directory '%s' \[[ocfl/validator.py#L213](https://github.com/zimeon/ocfl-py/blob/main/ocfl/validator.py#L213)\] |
| W901 | **Not in specification** | OCFL Storage Root includes unregistered extension directory '%s' \[[ocfl/store.py#L193](https://github.com/zimeon/ocfl-py/blob/main/ocfl/store.py#L193)\] |

_Generated by `extract_codes.py` at 2022-02-03 19:54:14.570927_