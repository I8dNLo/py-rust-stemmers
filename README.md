brew install maturin

maturin build --release
pip install target/wheels/py_rust_stemmers-0.1.0-cp312-cp312-macosx_11_0_arm64.whl
python speedtest.py