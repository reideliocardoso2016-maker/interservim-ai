import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'app/config/app_config.dart';
import 'app/theme/app_theme.dart';
import 'app/routes/app_router.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(
    ProviderScope(
      child: InterservimAIApp(),
    ),
  );
}

class InterservimAIApp extends ConsumerStatefulWidget {
  const InterservimAIApp({super.key});

  @override
  ConsumerState<InterservimAIApp> createState() => _InterservimAIAppState();
}

class _InterservimAIAppState extends ConsumerState<InterservimAIApp> {
  late final GoRouter _router;

  @override
  void initState() {
    super.initState();
    _router = AppRouter.createRouter(ref);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: AppConfig.appName,
      theme: AppTheme.lightTheme,
      routerConfig: _router,
      debugShowCheckedModeBanner: false,
    );
  }
}
