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

# flutter_plugin_android_lifecycle requires compileSdk 36
if 'compileSdk = flutter.compileSdkVersion' not in content:
    content = content.replace('compileSdk = flutter.compileSdkVersion', 'compileSdk = 36')
    content = content.replace('compileSdk = 34', 'compileSdk = 36')
    content = content.replace('compileSdk = 33', 'compileSdk = 36')

# Ensure minSdk uses flutter.minSdkVersion
content = content.replace('minSdk = 23', 'minSdk = flutter.minSdkVersion')
content = content.replace('minSdk = 21', 'minSdk = flutter.minSdkVersion')

# Ensure targetSdk uses flutter.targetSdkVersion
content = content.replace('targetSdk = 34', 'targetSdk = flutter.targetSdkVersion')
content = content.replace('targetSdk = 33', 'targetSdk = flutter.targetSdkVersion')
content = content.replace('targetSdk = flutter.compileSdkVersion', 'targetSdk = flutter.targetSdkVersion')

with open(path, 'w') as f:
    f.write(content)

print(f"Updated {path}")
