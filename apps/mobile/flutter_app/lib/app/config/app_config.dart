class AppConfig {
  static const String appName = 'InterServim AI Sales Agent';
  static const String version = '1.0.0';
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000/api/v1',
  );
  static const int connectionTimeout = 30000;
  static const int receiveTimeout = 30000;
}
