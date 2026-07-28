import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../shared/services/api_service.dart';

class AuthState {
  final bool isAuthenticated;
  final String? token;
  final String? userName;
  final String? userRole;
  final bool isLoading;
  final String? error;

  const AuthState({
    this.isAuthenticated = false,
    this.token,
    this.userName,
    this.userRole,
    this.isLoading = false,
    this.error,
  });

  AuthState copyWith({
    bool? isAuthenticated,
    String? token,
    String? userName,
    String? userRole,
    bool? isLoading,
    String? error,
  }) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      token: token ?? this.token,
      userName: userName ?? this.userName,
      userRole: userRole ?? this.userRole,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  final ApiService _api;
  final FlutterSecureStorage _storage;

  AuthNotifier(this._api, this._storage) : super(const AuthState()) {
    _api.init();
  }

  Future<void> guestLogin() async {
    state = state.copyWith(isLoading: true);
    try {
      final response = await _api.post('/auth/guest');
      final data = response.data;
      await _storage.write(key: 'access_token', value: data['access_token']);
      await _storage.write(key: 'refresh_token', value: data['refresh_token']);
      state = AuthState(
        isAuthenticated: true,
        token: data['access_token'],
        userRole: 'ADMIN',
      );
    } catch (e) {
      state = state.copyWith(isLoading: false, error: 'Error de conexión');
    }
  }

  Future<void> logout() async {
    await _storage.deleteAll();
    state = const AuthState();
  }
}

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ApiService(), const FlutterSecureStorage());
});
