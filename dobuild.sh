#!/bin/bash

APPNAME="InternetTester"
APPDIR="$APPNAME.app/Contents/MacOS/"
echo "Cleaning build dirs"
rm -rf __pycache__
rm -rf build
rm -rf dist
rm *.spec
rm -rf $APPDIR

echo "Doing build"

source venv/bin/activate

pyinstaller --clean -F --windowed --osx-bundle-identifier "com.terminaloutcomes.internettester" "script.py"

mkdir -p $APPDIR
cp run_other $APPDIR/$APPNAME
cp "dist/script" $APPDIR
chmod +x $APPDIR/$APPNAME
