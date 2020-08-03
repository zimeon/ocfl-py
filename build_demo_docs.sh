#!/bin/bash

python tests/test_demo_build_spec_examples.py > docs/demo_build_spec_examples.md
python tests/test_demo_ocfl_object_script.py > docs/demo_ocfl_object_script.md
python tests/test_demo_ocfl_store_script.py > docs/demo_ocfl_store_script.md
python tests/test_demo_using_bagit_bags.py > docs/demo_using_bagit_bags.md
python tests/test_demo_ocfl_sidecar_script.py > docs/demo_ocfl_sidecar_script.md
