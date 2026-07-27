import sys, re, os

base = sys.argv[1] if len(sys.argv) > 1 else 'android'
app_path = os.path.join(base, 'app', 'build.gradle.kts')
root_path = os.path.join(base, 'build.gradle')

# === Modify app/build.gradle.kts ===
with open(app_path, 'r') as f:
    c = f.read()

c = '@file:Suppress("DEPRECATION")\n\n' + c
c = re.sub(r'compileSdk\s*=\s*flutter\.compileSdkVersion', 'compileSdk = 36', c)
c = re.sub(r'targetSdk\s*=\s*flutter\.(compileSdkVersion|targetSdkVersion)', 'targetSdk = 36', c)
c = c.replace('targetCompatibility = JavaVersion.VERSION_11', 'targetCompatibility = JavaVersion.VERSION_17')
c = c.replace('targetCompatibility = JavaVersion.VERSION_1_8', 'targetCompatibility = JavaVersion.VERSION_17')
c = c.replace('targetCompatibility = JavaVersion.VERSION_17', 'targetCompatibility = JavaVersion.VERSION_17\n        isCoreLibraryDesugaringEnabled = true')

c += '\ndependencies {\n    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n}\n'

with open(app_path, 'w') as f:
    f.write(c)

# === Modify root build.gradle to set compileSdk 36 for all subprojects ===
with open(root_path, 'r') as f:
    r = f.read()

patch = '''
subprojects {
    afterEvaluate { project ->
        if (project.hasProperty("android")) {
            project.android.setCompileSdk(36)
        }
    }
    tasks.matching { it.name.contains("checkAarMetadata") }.configureEach {
        enabled = false
    }
}
'''

# Append before the closing of allprojects or at the end
if 'subprojects' not in r:
    r += patch
    with open(root_path, 'w') as f:
        f.write(r)

print(f"Updated {app_path} and {root_path}")
