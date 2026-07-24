import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../app/theme/app_theme.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  int _selectedIndex = 0;

  final _screens = [
    const _DashboardContent(),
    _ConversationsList(),
    _CustomersList(),
    _SettingsView(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(['Dashboard', 'Conversaciones', 'Clientes', 'Ajustes'][_selectedIndex]),
        actions: [
          IconButton(icon: const Icon(Icons.notifications_outlined), onPressed: () {}),
          IconButton(icon: const Icon(Icons.person_outline), onPressed: () {}),
        ],
      ),
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (i) => setState(() => _selectedIndex = i),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.dashboard), label: 'Dashboard'),
          BottomNavigationBarItem(icon: Icon(Icons.chat), label: 'Conversaciones'),
          BottomNavigationBarItem(icon: Icon(Icons.people), label: 'Clientes'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Ajustes'),
        ],
      ),
    );
  }
}

class _DashboardContent extends StatelessWidget {
  const _DashboardContent();

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(child: _MetricCard(title: 'Clientes Nuevos', value: '12', icon: Icons.person_add, color: AppColors.primary)),
              const SizedBox(width: 12),
              Expanded(child: _MetricCard(title: 'Activos', value: '8', icon: Icons.chat, color: AppColors.secondary)),
            ],
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              Expanded(child: _MetricCard(title: 'Cotizaciones', value: '5', icon: Icons.description, color: AppColors.accent)),
              const SizedBox(width: 12),
              Expanded(child: _MetricCard(title: 'Ganadas', value: '3', icon: Icons.trending_up, color: AppColors.success)),
            ],
          ),
          const SizedBox(height: 24),
          Text('Acceso Rápido', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          _QuickActionCard(
            icon: Icons.auto_awesome,
            title: 'Marketing IA',
            subtitle: 'Genera contenido con IA',
            onTap: () => context.go('/dashboard/marketing'),
          ),
          _QuickActionCard(
            icon: Icons.inventory_2,
            title: 'Productos',
            subtitle: 'Gestiona tu catálogo',
            onTap: () => context.go('/dashboard/products'),
          ),
          _QuickActionCard(
            icon: Icons.analytics,
            title: 'Estadísticas',
            subtitle: 'Analiza tu rendimiento',
            onTap: () => context.go('/dashboard/analytics'),
          ),
          _QuickActionCard(
            icon: Icons.menu_book,
            title: 'Base de Conocimiento',
            subtitle: 'Documentos y recursos',
            onTap: () => context.go('/dashboard/knowledge'),
          ),
        ],
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  final String title, value;
  final IconData icon;
  final Color color;

  const _MetricCard({required this.title, required this.value, required this.icon, required this.color});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                  child: Icon(icon, color: color, size: 20),
                ),
              ],
            ),
            const SizedBox(height: 12),
            Text(value, style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontSize: 28)),
            Text(title, style: Theme.of(context).textTheme.bodyMedium),
          ],
        ),
      ),
    );
  }
}

class _QuickActionCard extends StatelessWidget {
  final IconData icon;
  final String title, subtitle;
  final VoidCallback onTap;

  const _QuickActionCard({required this.icon, required this.title, required this.subtitle, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: AppColors.primary),
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
      ),
    );
  }
}

class _ConversationsList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Card(
          child: ListTile(
            leading: CircleAvatar(child: Text('JM')),
            title: const Text('Juan Martínez'),
            subtitle: const Text('¿Tienen disponibilidad de arroz?'),
            trailing: const Text('10:30', style: TextStyle(color: Colors.grey, fontSize: 12)),
          ),
        ),
        Card(
          child: ListTile(
            leading: CircleAvatar(child: Text('PG')),
            title: const Text('Pedro García'),
            subtitle: const Text('Necesito cotización de azúcar'),
            trailing: const Text('09:15', style: TextStyle(color: Colors.grey, fontSize: 12)),
          ),
        ),
      ],
    );
  }
}

class _CustomersList extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        _buildCustomerCard(context, 'María López', 'importador', 'México'),
        _buildCustomerCard(context, 'Carlos Ruiz', 'distribuidor', 'Colombia'),
        _buildCustomerCard(context, 'Ana Torres', 'minorista', 'Perú'),
      ],
    );
  }

  Widget _buildCustomerCard(BuildContext context, String name, String type, String country) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: CircleAvatar(child: Text(name[0])),
        title: Text(name),
        subtitle: Text('$type • $country'),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => context.go('/dashboard/customers/1'),
      ),
    );
  }
}

class _SettingsView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Card(child: ListTile(leading: Icon(Icons.person), title: Text('Perfil'), trailing: Icon(Icons.chevron_right))),
        const Card(child: ListTile(leading: Icon(Icons.notifications), title: Text('Notificaciones'), trailing: Icon(Icons.chevron_right))),
        const Card(child: ListTile(leading: Icon(Icons.security), title: Text('Seguridad'), trailing: Icon(Icons.chevron_right))),
        const SizedBox(height: 24),
        SizedBox(
          width: double.infinity,
          child: OutlinedButton.icon(
            onPressed: () {},
            icon: const Icon(Icons.logout),
            label: const Text('Cerrar Sesión'),
            style: OutlinedButton.styleFrom(foregroundColor: AppColors.error),
          ),
        ),
      ],
    );
  }
}
