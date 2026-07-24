import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';
import '../../../app/providers/auth_provider.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Configuración')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            child: Column(
              children: [
                const ListTile(leading: Icon(Icons.person), title: Text('Perfil'), trailing: Icon(Icons.chevron_right)),
                const Divider(height: 1),
                const ListTile(leading: Icon(Icons.notifications), title: Text('Notificaciones'), trailing: Icon(Icons.chevron_right)),
                const Divider(height: 1),
                const ListTile(leading: Icon(Icons.security), title: Text('Seguridad'), trailing: Icon(Icons.chevron_right)),
                const Divider(height: 1),
                const ListTile(leading: Icon(Icons.language), title: Text('Idioma'), subtitle: Text('Español'), trailing: Icon(Icons.chevron_right)),
                const Divider(height: 1),
                SwitchListTile(
                  secondary: const Icon(Icons.smart_toy),
                  title: const Text('IA Automática'),
                  subtitle: const Text('Responder mensajes automáticamente'),
                  value: true,
                  onChanged: (_) {},
                ),
              ],
            ),
          ),
          const SizedBox(height: 24),
          Text('Información', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          Card(
            child: Column(
              children: [
                const ListTile(title: Text('Versión'), subtitle: Text('1.0.0')),
                const Divider(height: 1),
                const ListTile(title: Text('Backend'), subtitle: Text('FastAPI + PostgreSQL')),
              ],
            ),
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: () {
                ref.read(authProvider.notifier).logout();
                context.go('/login');
              },
              icon: const Icon(Icons.logout),
              label: const Text('Cerrar Sesión'),
              style: OutlinedButton.styleFrom(foregroundColor: AppColors.error),
            ),
          ),
        ],
      ),
    );
  }
}
