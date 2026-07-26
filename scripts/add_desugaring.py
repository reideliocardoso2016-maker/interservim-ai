import re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'android/app/build.gradle.kts'

with open(path, 'r') as f:
    content = f.read()

content = content.replace(
    'targetCompatibility = JavaVersion.VERSION_17',
    'targetCompatibility = JavaVersion.VERSION_17\n        isCoreLibraryDesugaringEnabled = true'
)

if 'coreLibraryDesugaring' not in content:
    content += '\ndependencies {\n    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n}\n'

with open(path, 'w') as f:
    f.write(content)

print(f"Updated {path}")
