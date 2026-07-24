import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class AnalyticsScreen extends StatelessWidget {
  const AnalyticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Estadísticas')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(child: _AnalyticCard(title: 'Clientes', value: '45', change: '+12%', color: AppColors.primary)),
                const SizedBox(width: 12),
                Expanded(child: _AnalyticCard(title: 'Conversaciones', value: '128', change: '+8%', color: AppColors.secondary)),
              ],
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(child: _AnalyticCard(title: 'Cotizaciones', value: '32', change: '+15%', color: AppColors.accent)),
                const SizedBox(width: 12),
                Expanded(child: _AnalyticCard(title: 'Tasa Conversión', value: '24%', change: '+3%', color: AppColors.success)),
              ],
            ),
            const SizedBox(height: 24),
            Text('Productos Más Consultados', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 12),
            Card(
              child: Column(
                children: [
                  ListTile(title: const Text('Arroz Blanco'), trailing: Text('32 consultas', style: Theme.of(context).textTheme.bodyMedium)),
                  const Divider(height: 1),
                  ListTile(title: const Text('Azúcar Refinada'), trailing: Text('28 consultas', style: Theme.of(context).textTheme.bodyMedium)),
                  const Divider(height: 1),
                  ListTile(title: const Text('Maíz Amarillo'), trailing: Text('21 consultas', style: Theme.of(context).textTheme.bodyMedium)),
                  const Divider(height: 1),
                  ListTile(title: const Text('Frijol Negro'), trailing: Text('15 consultas', style: Theme.of(context).textTheme.bodyMedium)),
                ],
              ),
            ),
            const SizedBox(height: 24),
            Text('Actividad Reciente', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 12),
            Card(child: ListTile(title: const Text('Nueva cotización creada'), subtitle: const Text('Hace 5 minutos'))),
            Card(child: ListTile(title: const Text('Cliente contactado vía WhatsApp'), subtitle: const Text('Hace 15 minutos'))),
            Card(child: ListTile(title: const Text('Seguimiento automático enviado'), subtitle: const Text('Hace 1 hora'))),
          ],
        ),
      ),
    );
  }
}

class _AnalyticCard extends StatelessWidget {
  final String title, value, change;
  final Color color;

  const _AnalyticCard({required this.title, required this.value, required this.change, required this.color});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 8),
            Text(value, style: Theme.of(context).textTheme.headlineLarge?.copyWith(fontSize: 24)),
            const SizedBox(height: 4),
            Row(
              children: [
                Icon(Icons.trending_up, size: 14, color: AppColors.success),
                const SizedBox(width: 4),
                Text(change, style: const TextStyle(color: AppColors.success, fontSize: 12)),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
