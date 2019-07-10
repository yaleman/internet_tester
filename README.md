# Internet Tester

Package the app for macOS by running `dobuild.sh`. This'll make InternetTester.app which should be portable.

You'll need a few things first, I suggest using pipenv or a virtualenv.

Build requirements:

    virtualenv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    ./dobuild.sh
    open InternetTester.app

Done!

If you're running something other than macOS, do the above, stop at the line starting with `pip3` then run `script.py`.