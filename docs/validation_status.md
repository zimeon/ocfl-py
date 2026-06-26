# Implementation status for errors and warnings

The following tables show the implementation status of all errors and warnings in the OCFL v1.1 specification, with links to the specification and into the code repository.

## Errors

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| E001 | **Not in specification** | **Missing description** \[[ocflvalidation_logger.py#L5](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidation_logger.py#L5)\] |
| | E001a | OCFL Object root contains unexpected file: %s \[[ocflvalidation_logger.py#L10](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidation_logger.py#L10) [ocflvalidator.py#L258](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L258)\] |
| | E001b | OCFL Object root contains unexpected directory: %s \[[ocflvalidation_logger.py#L16](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidation_logger.py#L16) [ocflvalidator.py#L275](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L275)\] |
| | E001c | OCFL Object root contains unexpected entry that isn't a file or directory: %s \[[ocflvalidator.py#L277](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L277)\] |
| E002 | **Not in specification** | NOTE - E002 is redundant to more specific errors E003, E004, E005, E006. \[_Not implemented_\] |
| E003 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E003a | OCFL Object version declaration file is missing (assuming version %s) \[[ocflvalidator.py#L135](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L135)\] |
| | E003b | OCFL Object includes more that one file that looks like an object declaration (got %s), using version %s \[[ocflvalidator.py#L157](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L157)\] |
| | E003c | OCFL Object includes one or more object declaration files (starting 0=) but no valid version number could be extracted from any of them (assuming version %s) \[[ocflvalidator.py#L152](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L152)\] |
| | E003d | OCFL Storage Root hierarchy includes directory %s with more that one file that looks like an object declaration, ignoring \[[ocflstorage_root.py#L321](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L321)\] |
| | E003e | No OCFL Object to validate at path %s. The root of an OCFL Object must be a directory containing an object declaration \[[ocflvalidator.py#L129](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L129)\] |
| E004 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E004a | OCFL Storage Root hierarchy includes directory %s with an object declaration giving unknown version %s, ignoring \[[ocflstorage_root.py#L328](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L328)\] |
| | E004b | OCFL Storage Root hierarchy includes directory %s with an unrecognized object declaration %s, ignoring \[[ocflstorage_root.py#L330](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L330)\] |
| E006 | **Not in specification** | The OCFL object conformance declaration filename must be 0=ocfl_object_, followed by the OCFL specification version number, got %s instead \[[ocflvalidator.py#L146](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L146)\] |
| E007 | **Not in specification** | OCFL Object declaration file %s contents do not match file name without leading 0= (the 'dvalue') \[[ocflvalidator.py#L150](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L150)\] |
| E008 | **Not in specification** | OCFL Object %s inventory versions block does not contain any versions, there must be at least version 1 \[[ocflinventory_validator.py#L192](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L192) [ocflinventory_validator.py#L362](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L362)\] |
| E009 | **Not in specification** | OCFL Object %s inventory versions block does not contain v1 or a zero padded equivalent \[[ocflinventory_validator.py#L382](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L382)\] |
| E010 | **Not in specification** | OCFL Object %s inventory versions block includes an out-of-sequence version \[[ocflinventory_validator.py#L393](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L393)\] |
| E011 | **Not in specification** | **Missing description** \[[ocflinventory_validator.py#L400](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L400)\] |
| E015 | **Not in specification** | OCFL Object version directory %s includes an illegal file (%s) \[[ocflvalidator.py#L437](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L437)\] |
| E017 | **Not in specification** | OCFL Object %s inventory contentDirectory must be a string and must not contain a forward slash (/) \[[ocflinventory_validator.py#L162](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L162)\] |
| E018 | **Not in specification** | OCFL Object %s inventory contentDirectory must not be either . or .. \[[ocflinventory_validator.py#L164](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L164)\] |
| E019 | **Not in specification** | OCFL Object %s inventory sets contentDirectory whereas it was not set in the first version inventory \[[ocflvalidator.py#L347](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L347) [ocflvalidator.py#L355](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L355)\] |
| E020 | **Not in specification** | OCFL Object %s inventory contentDirectory %s does not match root contentDirectory %s \[[ocflvalidator.py#L358](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L358)\] |
| E023 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E023a | OCFL Object includes one or more files that are not mentioned in the  %s inventory manifest (%s) \[[ocflvalidator.py#L475](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L475)\] |
| | E023b | OCFL Object %s manifest does not include files listed in previous version manifests (%s) \[[ocflvalidator.py#L368](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L368)\] |
| E024 | **Not in specification** | OCFL Object version %s content directory includes empty path %s \[[ocflvalidator.py#L428](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L428)\] |
| E025 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E025a | OCFL Object %s inventory `digestAlgorithm` attribute not an allowed digest type (got '%s') \[[ocflinventory_validator.py#L156](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L156)\] |
| | E025b | OCFL Object %s inventory manifest block includes a digest (%s) that doesn't have the correct form for the %s algorithm \[[ocflinventory_validator.py#L281](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L281)\] |
| E026 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E026a | OCFL Object %s inventory uses unknown digest type %s \[[ocflinventory_validator.py#L524](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L524)\] |
| E033 | **Not in specification** | OCFL Object %s inventory is not valid JSON (%s) \[[ocflobject.py#L672](https://github.com/zimeon/ocfl-py/blob/main/ocflobject.py#L672) [ocflvalidator.py#L206](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L206) [ocflvalidator.py#L209](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L209)\] |
| E036 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E036a | OCFL Object %s inventory missing `id` attribute \[[ocflinventory_validator.py#L128](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L128)\] |
| | E036b | OCFL Object %s inventory missing `type` attribute \[[ocflinventory_validator.py#L130](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L130)\] |
| | E036c | OCFL Object %s inventory missing `digestAlgorithm` attribute \[[ocflinventory_validator.py#L147](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L147)\] |
| | E036d | OCFL Object %s inventory missing `head` attribute \[[ocflinventory_validator.py#L180](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L180)\] |
| E037 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E037a | OCFL Object %s inventory `id` attribute is empty or badly formed \[[ocflinventory_validator.py#L120](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L120)\] |
| | E037b | OCFL Object %s inventory id `%s` does not match the value in the root inventory `%s` \[[ocflvalidator.py#L343](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L343)\] |
| E038 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E038a | OCFL Object %s inventory `type` attribute has wrong value (expected %s, got %s) \[[ocflinventory_validator.py#L135](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L135)\] |
| | E038b | OCFL Object %s inventory `type` attribute does not look like a valid specification URI (got %s), will proceed as if using version %s \[[ocflinventory_validator.py#L140](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L140)\] |
| | E038c | OCFL Object %s inventory `type` attribute has an unsupported specification version number (%s), will proceed as if using version %s \[[ocflinventory_validator.py#L145](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L145)\] |
| | E038d | OCFL Object %s inventory `type` attribute does not have a string value \[[ocflinventory_validator.py#L132](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L132)\] |
| E040 | **Not in specification** | OCFL Object %s inventory head attribute doesn't match versions (got %s, expected %s) \[[ocflinventory_validator.py#L184](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L184)\] |
| E041 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E041a | OCFL Object %s inventory missing `manifest` attribute \[[ocflinventory_validator.py#L170](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L170)\] |
| | E041b | OCFL Object %s inventory missing `versions` attribute \[[ocflinventory_validator.py#L175](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L175)\] |
| | E041c | OCFL Object %s inventory manifest block is not a JSON object \[[ocflinventory_validator.py#L274](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L274)\] |
| E042 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E042a | OCFL Object %s inventory manifest includes invalid content path %s \[[ocflinventory_validator.py#L559](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L559)\] |
| | E042b | OCFL Object %s inventory manifest includes content path %s with invalid version directory \[[ocflinventory_validator.py#L505](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L505)\] |
| | E042c | OCFL Object %s inventory manifest includes invalid content path %s that doesn't match the content directory name %s \[[ocflinventory_validator.py#L562](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L562)\] |
| E044 | **Not in specification** | OCFL Object %s inventory versions block is not a JSON object \[[ocflinventory_validator.py#L359](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L359)\] |
| E046 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E046a | OCFL Object root inventory describes version %s but no corresponding version directory is present \[[ocflvalidator.py#L439](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L439)\] |
| | E046b | OCFL Object includes directory %s that looks like a version directory but isn't a valid version in the inventory \[[ocflvalidator.py#L272](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L272)\] |
| E048 | **Not in specification** | OCFL Object %s inventory %s version block does not include a created date or it is malformed \[[ocflinventory_validator.py#L421](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L421)\] |
| | E048c | OCFL Object %s inventory %s version block does not include a state block \[[ocflinventory_validator.py#L437](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L437)\] |
| E049 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E049a | OCFL Object %s inventory %s version block created date SHOULD include a timezone designator \[[ocflinventory_validator.py#L429](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L429)\] |
| | E049b | OCFL Object %s inventory %s version block created date SHOULD be granular to the seconds level \[[ocflinventory_validator.py#L431](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L431)\] |
| | E049c | OCFL Object %s inventory %s version block has bad created date, must be IS8601 (%s) \[[ocflinventory_validator.py#L433](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L433)\] |
| | E049d | OCFL Object %s inventory %s version block created value is not a JSON string \[[ocflinventory_validator.py#L423](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L423)\] |
| E050 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E050a | OCFL Object %s inventory state refers to one or more digests that are not in the manifest (%s) \[[ocflinventory_validator.py#L513](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L513)\] |
| | E050c | OCFL Object %s inventory %s version block state block is not a JSON object \[[ocflinventory_validator.py#L470](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L470)\] |
| | E050d | OCFL Object %s inventory %s version state block includes a bad digest (%s) \[[ocflinventory_validator.py#L475](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L475)\] |
| | E050e | OCFL Object %s inventory %s version block state block value for digest %s is not list \[[ocflinventory_validator.py#L477](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L477)\] |
| | E050f | OCFL Object %s inventory version %s state includes digest value %s that is not listed in the manifest block \[[ocflinventory_validator.py#L486](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L486)\] |
| E051 | **Not in specification** | NOTE - E051 is essentially a processing instruction and can't be tested for. \[_Not implemented_\] |
| E052 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that starts or ends with / \[[ocflinventory_validator.py#L541](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L541)\] |
| E053 | **Not in specification** | OCFL Object %s inventory %s version block state block includes an invalid path %s that includes . .. or // \[[ocflinventory_validator.py#L536](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L536)\] |
| E054 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E054a | OCFL Object %s inventory %s version block has user key with value that isn't a JSON object \[[ocflinventory_validator.py#L447](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L447)\] |
| | E054b | OCFL Object %s inventory %s version block has user/name key with value that isn't a string \[[ocflinventory_validator.py#L450](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L450)\] |
| | E054c | OCFL Object %s inventory %s version block has user/address key with value that isn't a string \[[ocflinventory_validator.py#L454](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L454)\] |
| E056 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E056a | OCFL Object %s inventory includes a fixity key with value that isn't a JSON object \[[ocflinventory_validator.py#L312](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L312)\] |
| | E056b | OCFL Object %s inventory fixity block includes a key that is not a known digest algorithm name: %s \[[ocflinventory_validator.py#L320](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L320)\] |
| E057 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E057a | OCFL Object %s inventory fixity block entry for digest algorithm name %s is not a JSON object \[[ocflinventory_validator.py#L327](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L327)\] |
| | E057b | OCFL Object %s inventory fixity block entry for digest algorithm %s includes digest %s which has the wrong form \[[ocflinventory_validator.py#L333](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L333)\] |
| | E057c | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s is not a JSON list \[[ocflinventory_validator.py#L335](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L335)\] |
| | E057d | OCFL Object %s inventory fixity block entry for digest algorithm %s, digest %s includes a content path %s that is not in the manifest \[[ocflinventory_validator.py#L348](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L348)\] |
| E058 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E058a | OCFL Object %s inventory is missing sidecar digest file at %s \[[ocflvalidator.py#L221](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L221)\] |
| | E058b | Cannot extract digest type from inventory digest file name %s \[[ocflvalidator.py#L244](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L244)\] |
| E060 | **Not in specification** | Mismatch between actual and recorded inventory digests for %s (calculated %s but read %s from %s) \[[ocflvalidator.py#L240](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L240)\] |
| E061 | **Not in specification** | Cannot extract digest from inventory digest file (%s) \[[ocflvalidator.py#L242](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L242)\] |
| E063 | **Not in specification** | OCFL Object root inventory is missing \[[ocflvalidator.py#L161](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L161)\] |
| E064 | **Not in specification** | Object root inventory and copy in last version MUST be identical but are not (%s and %s) \[[ocflvalidator.py#L325](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L325)\] |
| E066 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E066a | OCFL Object inventory for %s doesn't have a subset of version blocks of inventory for %s \[[ocflinventory_validator.py#L217](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L217)\] |
| | E066b | OCFL Object %s inventory %s version state doesn't have same logical paths as same version in %s inventory (paths %s only in %s inventory) \[[ocflinventory_validator.py#L237](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L237) [ocflinventory_validator.py#L239](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L239)\] |
| | E066c | OCFL Object %s inventory %s version state has logical path %s that maps to content path %s, but in %s inventory it maps to content path %s \[[ocflinventory_validator.py#L244](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L244)\] |
| | E066d | OCFL Object %s inventory %s version state has digest %s (mapping to logical files %s) that does not appear in the %s inventory \[[ocflinventory_validator.py#L596](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L596)\] |
| | E066e | OCFL Object %s inventory %s version state has digest %s (mapping to logical files %s) that does not appear in the %s inventory \[[ocflinventory_validator.py#L599](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L599)\] |
| E067 | **Not in specification** | OCFL Object extensions direct contains an unexpected non-directory entry: %s \[[ocflvalidator.py#L294](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L294)\] |
| E069 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E069a | OCFL Storage Root %s lacks required 0= declaration file \[[ocflstorage_root.py#L238](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L238)\] |
| | E069b | OCFL Storage Root %s has more than one 0= declaration file \[[ocflstorage_root.py#L240](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L240)\] |
| | E069c | OCFL Storage Root %s has unrecognized 0= declaration file %s \[[ocflstorage_root.py#L247](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L247) [ocflstorage_root.py#L250](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L250)\] |
| | E069d | OCFL Storage Root %s 0= declaration is for spec version %s, not %s as expected \[_Not implemented_\] |
| | E069e | OCFL Storage Root %s required declaration file %s has invalid content \[[ocflstorage_root.py#L255](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L255)\] |
| E070 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E070a | OCFL Storage Root %s includes ocfl_layout.json with unknown layout %s \[[ocflstorage_root.py#L287](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L287)\] |
| | E070b | OCFL Storage Root %s has an ocfl_layout.json file that isn't a JSON object \[[ocflstorage_root.py#L289](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L289)\] |
| | E070c | OCFL Storage Root %s Storage root %s has layout file doesn't have required extension and description string entries \[[ocflstorage_root.py#L292](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L292)\] |
| E071 | **Not in specification** | OCFL Storage Root %s includes ocfl_layout.json with unknown layout %s \[[ocflstorage_root.py#L261](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L261)\] |
| E072 | **Not in specification** | OCFL storage root hierarchy include directory %s with at least one file but no object declaration. Such additional files are not allowed \[[ocflstorage_root.py#L332](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L332) [ocflstorage_root.py#L36](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L36)\] |
| E073 | **Not in specification** | OCFL storage root hierarchy contains an empty directory: %s \[[ocflstorage_root.py#L314](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L314)\] |
| E086 | **Not in specification** | OCFL Storage Root extensions direct contains an unexpected non-directory entry: %s \[[ocflstorage_root.py#L356](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L356)\] |
| E087 | **Not in specification** | NOTE - E087 is a processing instruction and can't be tested for \[_Not implemented_\] |
| E088 | **Not in specification** | NOTE - E088 is redundant to more specific errors E072 and E073 \[_Not implemented_\] |
| E090 | **Not in specification** | NOTE - E090 is a processing instruction and can't be tested for \[_Not implemented_\] |
| E091 | **Not in specification** | OCFL Object %s inventory manifest file list for digest %s is not a JSON array \[_Not implemented_\] |
| E092 | **Not in specification** | **Missing description** \[[ocflinventory_validator.py#L283](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L283)\] |
| | E092a | OCFL Object %s inventory manifest using digest algorithm %s has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocflvalidator.py#L465](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L465) [ocflvalidator.py#L470](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L470)\] |
| | E092b | OCFL Object %s inventory manifest refers to a file path that is not present in the object (%s) \[[ocflvalidator.py#L460](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L460)\] |
| E093 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E093a | OCFL Object %s inventory fixity block for digest algorithm %s has digest %s for file %s which doesn't match calculated digest %s for that file \[[ocflvalidator.py#L468](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L468) [ocflvalidator.py#L471](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L471)\] |
| | E093b | OCFL Object %s inventory fixity block for digest algorithm %s has digest %s for a file %s which does not exist in the object \[[ocflvalidator.py#L454](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L454)\] |
| E094 | **Not in specification** | OCFL Object %s inventory %s version block has message key with value that isn't a string \[[ocflinventory_validator.py#L441](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L441)\] |
| E095 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E095a | OCFL Object %s inventory version %s state has logical path %s used more than once \[[ocflinventory_validator.py#L481](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L481)\] |
| | E095b | OCFL Object %s inventory version %s state has logical path %s used as both a directory and a file path. \[[ocflinventory_validator.py#L492](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L492)\] |
| E096 | **Not in specification** | OCFL Object %s inventory manifest block includes digest %s more than once with different normalizations \[[ocflinventory_validator.py#L289](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L289)\] |
| E097 | **Not in specification** | OCFL Object %s inventory fixity block for digest algorithm %s, includes digest %s more than once with different normalizations \[[ocflinventory_validator.py#L343](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L343)\] |
| E099 | **Not in specification** | OCFL Object %s inventory manifest content path %s includes invalid element ., .., or empty (//). \[[ocflinventory_validator.py#L567](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L567)\] |
| E100 | **Not in specification** | OCFL Object %s inventory manifest content path %s must not begin or end with /. \[[ocflinventory_validator.py#L555](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L555)\] |
| E101 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | E101a | OCFL Object %s inventory manifest content path %s is repeated \[[ocflinventory_validator.py#L571](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L571)\] |
| | E101b | OCFL Object %s inventory manifest content path %s used as both a directory and a file path \[[ocflinventory_validator.py#L299](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L299)\] |
| E103 | **Not in specification** | OCFL Object %s inventory conforms to specification version %s which is an earlier version than the %s inventory which conforms to specification version %s \[[ocflvalidator.py#L400](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L400)\] |
| E107 | **Not in specification** | OCFL Object %s inventory manifest contains digest(s) (%s) that are not used in the object state \[[ocflinventory_validator.py#L516](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L516)\] |
| E111 | **Not in specification** | OCFL Object %s inventory includes a fixity key with value that isn't a JSON object \[_Not implemented_\] |

## Warnings

| Code | Specification text (or suffixed code) | Implementation status and message/links |
| --- | --- | --- |
| W001 | **Not in specification** | OCFL Object %s inventory version numbers SHOULD NOT be zero-padded \[[ocflinventory_validator.py#L385](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L385)\] |
| W002 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain any directory except the designated content directory (found %s) \[[ocflvalidator.py#L435](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L435)\] |
| W003 | **Not in specification** | OCFL Object version directory %s SHOULD NOT contain an empty content directory \[[ocflvalidator.py#L433](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L433)\] |
| W004 | **Not in specification** | OCFL Object %s inventory SHOULD use sha512 but uses sha256 as the DigestAlgorithm \[[ocflinventory_validator.py#L153](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L153)\] |
| W005 | **Not in specification** | OCFL Object %s inventory id SHOULD be a URI (got %s) \[[ocflinventory_validator.py#L125](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L125)\] |
| W007 | **Not in specification** | _See multiple cases identified with suffixes below_ |
| | W007a | OCFL Object %s inventory %s version block SHOULD include a message key \[[ocflinventory_validator.py#L439](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L439)\] |
| | W007b | OCFL Object %s inventory %s version block SHOULD include a user key \[[ocflinventory_validator.py#L443](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L443)\] |
| W008 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD have an address \[[ocflinventory_validator.py#L452](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L452)\] |
| W009 | **Not in specification** | OCFL Object %s inventory %s version block user description SHOULD be a mailto: or person identifier URI \[[ocflinventory_validator.py#L456](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L456)\] |
| W010 | **Not in specification** | OCFL Object %s SHOULD have an inventory file but does not \[[ocflvalidator.py#L317](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L317)\] |
| W011 | **Not in specification** | OCFL Object version metadata '%s' for %s in %s inventory does not match that in %s inventory \[[ocflinventory_validator.py#L252](https://github.com/zimeon/ocfl-py/blob/main/ocflinventory_validator.py#L252)\] |
| W013 | **Not in specification** | OCFL Object includes unregistered extension directory '%s' \[[ocflvalidator.py#L292](https://github.com/zimeon/ocfl-py/blob/main/ocflvalidator.py#L292)\] |
| W901 | **Not in specification** | OCFL Storage Root includes unregistered extension directory '%s' \[[ocflstorage_root.py#L354](https://github.com/zimeon/ocfl-py/blob/main/ocflstorage_root.py#L354)\] |

_Generated by `extract_codes.py` at 2026-06-26 20:32:17.942655_