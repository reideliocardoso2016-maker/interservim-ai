import sys, os

base = sys.argv[1] if len(sys.argv) > 1 else 'android'
root_path = os.path.join(base, 'build.gradle')

with open(root_path, 'r') as f:
    r = f.read()

patch = '''
subprojects {
    afterEvaluate { project ->
        if (project.hasProperty("android")) {
            project.android.compileSdk = 36
        }
        project.tasks.findAll { it.name.contains("checkAarMetadata") }.each {
            it.enabled = false
        }
    }
}
'''

if 'subprojects' not in r:
    r += patch
    with open(root_path, 'w') as f:
        f.write(r)
    print(f"Patched {root_path}")
else:
    print(f"{root_path} already patched")
