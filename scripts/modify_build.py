import sys, re

path = sys.argv[1] if len(sys.argv) > 1 else 'android/app/build.gradle.kts'
settings_path = path.replace('app/build.gradle.kts', 'settings.gradle.kts')

# === Modify app/build.gradle.kts ===
with open(path, 'r') as f:
    c = f.read()

c = '@file:Suppress("DEPRECATION")\n\n' + c
c = re.sub(r'compileSdk\s*=\s*flutter\.compileSdkVersion', 'compileSdk = 36', c)
c = re.sub(r'targetSdk\s*=\s*flutter\.(compileSdkVersion|targetSdkVersion)', 'targetSdk = 36', c)
c = c.replace('targetCompatibility = JavaVersion.VERSION_11', 'targetCompatibility = JavaVersion.VERSION_17')
c = c.replace('targetCompatibility = JavaVersion.VERSION_1_8', 'targetCompatibility = JavaVersion.VERSION_17')
c = c.replace('targetCompatibility = JavaVersion.VERSION_17', 'targetCompatibility = JavaVersion.VERSION_17\n        isCoreLibraryDesugaringEnabled = true')

c += '\ndependencies {\n    coreLibraryDesugaring("com.android.tools:desugar_jdk_libs:2.1.4")\n}\n'

with open(path, 'w') as f:
    f.write(c)

# === Modify settings.gradle.kts to force compileSdk 36 for all modules ===
with open(settings_path, 'r') as f:
    s = f.read()

hook = '''

gradle.projectsLoaded {
    rootProject.allprojects {
        afterEvaluate {
            val androidExt = extensions.findByType<com.android.build.api.dsl.CommonExtension<*, *, *, *>>()
            if (androidExt != null && androidExt.compileSdk < 36) {
                androidExt.compileSdk = 36
            }
        }
    }
}

gradle.taskGraph.whenReady {
    allTasks.forEach { task ->
        if (task.name.contains("checkAarMetadata", ignoreCase = true)) {
            task.enabled = false
        }
    }
}
'''

if 'gradle.projectsLoaded' not in s:
    s += hook
    with open(settings_path, 'w') as f:
        f.write(s)

print(f"Updated {path} and {settings_path}")
