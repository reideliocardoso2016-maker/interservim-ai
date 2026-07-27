import sys, re

path = sys.argv[1] if len(sys.argv) > 1 else 'android/app/build.gradle.kts'

with open(path, 'r') as f:
    c = f.read()

c = '@file:Suppress("DEPRECATION")\n\n' + c
c = re.sub(r'compileSdk\s*=\s*flutter\.compileSdkVersion', 'compileSdk = 36', c)
c = re.sub(r'targetSdk\s*=\s*flutter\.(compileSdkVersion|targetSdkVersion)', 'targetSdk = 36', c)
c = c.replace('targetCompatibility = JavaVersion.VERSION_11', 'targetCompatibility = JavaVersion.VERSION_17')
c = c.replace('targetCompatibility = JavaVersion.VERSION_1_8', 'targetCompatibility = JavaVersion.VERSION_17')
c = c.replace('targetCompatibility = JavaVersion.VERSION_17', 'targetCompatibility = JavaVersion.VERSION_17\n        isCoreLibraryDesugaringEnabled = true')

c += '\ndependencies {\n    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n}\n'

# Disable AAR metadata check for all variants via androidComponents
c += '''
androidComponents {
    onVariants { variant ->
        variant.checkAarMetadata?.enabled = false
    }
}
'''

with open(path, 'w') as f:
    f.write(c)

print(f"Updated {path}")
