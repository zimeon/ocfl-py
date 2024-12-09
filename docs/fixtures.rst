Test Fixtures
=============

Official `OCFL Fixtures
<https://github.com/OCFL/fixtures>`_ include:

* OCFL v1.1

  * Specification examples:

    * Section `5.1 Minimal OCFL v1.1 Object <https://ocfl.io/1.1/spec/#example-minimal-object>`_ is good

    * Section `5.2 Versioned OCFL v1.1 Object <https://ocfl.io/1.1/spec/#example-versioned-object>`_ is valid and has fixture object `1.1/good-objects/spec-ex-full <https://github.com/OCFL/fixtures/tree/main/1.1/good-objects/spec-ex-full>`_

    * Section `5.3 Different Logical and Content Paths in an OCFL v1.1 Object <https://ocfl.io/1.1/spec/#example-object-diff-paths>`_ is valid but should generate a warning because the ``message`` property is missing.

* OCFL v1.0

  * Specification examples:

    * Section `5.1 Minimal OCFL v1.0 Object <https://ocfl.io/1.0/spec/#example-minimal-object>`_ is valid but should generate a warning because the ``address`` is not a URI

    * Section `5.2 Versioned OCFL v1.0 Object <https://ocfl.io/1.0/spec/#example-versioned-object>`_ is valid and has fixture object `1.0/good-objects/spec-ex-full <https://github.com/OCFL/fixtures/tree/main/1.0/good-objects/spec-ex-full>`_

    * Section `5.3 Different Logical and Content Paths in an OCFL v1.0 Object <https://ocfl.io/1.0/spec/#example-object-diff-paths>`_ is valid but should generate warnings because the ``message`` and the ``user`` ``name`` and ``address`` properties are missing.

Additions from `ocfl-py
<https://github.com/zimeon/ocfl-py/tree/main/extra_fixtures>`_ are in the ``extra_fixtures`` directory
