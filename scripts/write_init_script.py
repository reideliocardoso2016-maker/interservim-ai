import sys, os

path = os.path.join(sys.argv[1], 'init.gradle.kts') if len(sys.argv) > 1 else 'android/init.gradle.kts'

content = """gradle.projectsLoaded {
    allprojects {
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
"""

os.makedirs(os.path.dirname(path), exist_ok=True)
with open(path, 'w') as f:
    f.write(content)

print(f"Written {path}")
