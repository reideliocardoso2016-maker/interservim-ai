import os, sys, glob

pub_cache = os.path.expanduser('~/.pub-cache/hosted/pub.dev')
pattern = os.path.join(pub_cache, 'jni-*/android/build.gradle')
files = glob.glob(pattern)

if not files:
    print(f"NO JNI BUILD.GRADLE FOUND in {pattern}")
    sys.exit(1)

path = files[0]
print(f"FOUND: {path}")

with open(path, 'r') as f:
    data = f.read()

changes = 0

# 1. Apply kotlin-android unconditionally
old = 'if (agpMajor < 9) {\n    apply plugin: \'kotlin-android\'\n}'
new = '// patched by patch_jni.py\napply plugin: \'kotlin-android\''

if old in data:
    data = data.replace(old, new)
    changes += 1
    print("PATCHED: kotlin-android applied unconditionally")
else:
    print("SKIP kotlin-android: pattern not found")

# 2. Bump compileSdk from 35 to 36
old2 = 'compileSdk 35'
new2 = 'compileSdk 36'

if old2 in data:
    data = data.replace(old2, new2)
    changes += 1
    print("PATCHED: compileSdk 35 -> 36")
else:
    print("SKIP compileSdk: 'compileSdk 35' not found")

if changes > 0:
    with open(path, 'w') as f:
        f.write(data)
    print(f"DONE: {changes} change(s) applied")
else:
    print("NO CHANGES NEEDED")
