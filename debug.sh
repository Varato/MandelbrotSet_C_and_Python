rm -rf build;
rm *.so;
python setup.py build_ext --inplace && python draw.py
