# Contributing to ocfl-py

Issues and pull requests are appreciated. I apologize if it takes me some time to respond or review..

## Submitting issues

In the case of bugs please describe in detail, preferably with a recipe to repeat and demonstrate the problem. Although you should include test data as necessary, please be careful not to include secrets or passwords!

If you propose a major change or new feature, please submit an issue to discuss before moving ahead with a pull request.

## Coding style

If submitting a pull request:

   * Understand that this code and any merged contributions are covered by the [MIT license](LICENSE.txt)
   * First create an [issue](https://github.com/zimeon/ocfl-py/issues) to discuss the proposed change
   * Please submit pull requests against the `main` branch
   * Please write code that passes the linting tests in `.github/workflows/action.yml`, these include:
     * `pycodestyle` implements [PEP8](https://www.python.org/dev/peps/pep-0008/) with the following warnings disabled:
       * Line length is not enforced (E501), just be reasonable
       * Where necessary, line breaks should occur before binary operators (warning W504 is enabled, but W503 is disabled)
     * `pydocstyle` implements [PEP257](https://www.python.org/dev/peps/pep-0257/) style rules:
       * Nothing is disabled
     * `pylint` implements more complex static analysis and looks for code smells, some rules are disabled including:
       * [Checks already implemented in `pycodestyle` and `pydocstyle`](http://pylint.pycqa.org/en/latest/faq.html#i-am-using-another-popular-linter-alongside-pylint-which-messages-should-i-disable-to-avoid-duplicates)
       * A FIXME doesn't generate and error, but please avoid anyway (W0511)
       * See `.github/workflows/action.yml` for current exclusions
  * Other style choices not enforced:
    * Use double quotes (") and triple-double quotes (""") for strings unless
      there is reason to avoid having to quote these inside
  * Please don't repeat code
   * Please cover the code with tests
