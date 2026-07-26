gradle.projectsLoaded {
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
