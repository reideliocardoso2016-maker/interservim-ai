import sys, os

base = sys.argv[1] if len(sys.argv) > 1 else 'android'

# try both build.gradle and build.gradle.kts
root_path = None
for fname in ('build.gradle.kts', 'build.gradle'):
    p = os.path.join(base, fname)
    if os.path.exists(p):
        root_path = p
        break

if not root_path:
    print(f"ERROR: no build.gradle(.kts) found in {base}")
    sys.exit(1)

print(f"ROOT BUILD: {root_path}")

with open(root_path, 'r') as f:
    r = f.read()

marker = '// CI_PATCH_APPLIED'

if marker not in r:
    patch = f'''
// {marker}
subprojects {{
    if (name == 'jni') {{
        apply plugin: 'kotlin-android'
    }}
}}
subprojects {{
    afterEvaluate {{ project ->
        if (project.hasProperty("android")) {{
            project.android.compileSdk = 36
        }}
        project.tasks.findAll {{ it.name.contains("checkAarMetadata") }}.each {{
            it.enabled = false
        }}
    }}
}}
'''
    r += patch
    with open(root_path, 'w') as f:
        f.write(r)
    print(f"PATCHED {root_path}")
else:
    print(f"ALREADY PATCHED {root_path}")
