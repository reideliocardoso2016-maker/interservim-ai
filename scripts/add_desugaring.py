import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'android/app/build.gradle.kts'

with open(path, 'r') as f:
    content = f.read()

# Add AGP 9 deprecation suppression at the top
if '@file:Suppress' not in content:
    content = '@file:Suppress("DEPRECATION")\n\n' + content

# Add isCoreLibraryDesugaringEnabled if not present
if 'isCoreLibraryDesugaringEnabled' not in content:
    content = content.replace(
        'targetCompatibility = JavaVersion.VERSION_17',
        'targetCompatibility = JavaVersion.VERSION_17\n        isCoreLibraryDesugaringEnabled = true'
    )
    content = content.replace(
        'targetCompatibility = JavaVersion.VERSION_11',
        'targetCompatibility = JavaVersion.VERSION_11\n        isCoreLibraryDesugaringEnabled = true'
    )

# Append desugaring dependency if not present
if 'coreLibraryDesugaring' not in content:
    content += '\ndependencies {\n    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n}\n'

# Fix AAR metadata check for AGP 9+ compatibility
if 'aarMetadata' not in content:
    content = content.replace(
        '    }\n}\n\nkotlin {',
        '    }\n\n    aarMetadata {\n        minCompileSdk = 34\n    }\n}\n\nkotlin {'
    )

with open(path, 'w') as f:
    f.write(content)

print(f"Updated {path}")
