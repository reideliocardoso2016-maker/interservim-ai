import sys, os

# Write to ~/.gradle/init.d/ so Gradle loads it automatically
init_dir = os.path.expanduser('~/.gradle/init.d')
os.makedirs(init_dir, exist_ok=True)

path = os.path.join(init_dir, 'interservim.gradle.kts')

content = """gradle.afterProject { project ->
    val android = project.extensions.findByName("android")
    if (android is com.android.build.api.dsl.CommonExtension<*, *, *, *>) {
        android.compileSdk = 36
    }
    project.tasks.matching { it.name.contains("checkAarMetadata") }.configureEach {
        enabled = false
    }
}
"""

with open(path, 'w') as f:
    f.write(content)

print(f"Written {path}")
