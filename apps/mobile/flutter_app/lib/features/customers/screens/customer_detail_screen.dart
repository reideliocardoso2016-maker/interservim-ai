import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class CustomerDetailScreen extends StatelessWidget {
  final String id;
  const CustomerDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detalle del Cliente')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Row(
                  children: [
                    CircleAvatar(radius: 30, child: Text('ML', style: Theme.of(context).textTheme.headlineSmall)),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text('María López', style: Theme.of(context).textTheme.headlineSmall),
                          Text('Importadora López • México', style: Theme.of(context).textTheme.bodyMedium),
                        ],
                      ),
                    ),
                    Chip(label: const Text('ACTIVO'), backgroundColor: AppColors.success.withOpacity(0.2)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            Text('Información', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 8),
            Card(
              child: Column(
                children: [
                  ListTile(leading: const Icon(Icons.phone), title: const Text('Teléfono'), subtitle: const Text('+52 555 123 4567')),
                  const Divider(height: 1),
                  ListTile(leading: const Icon(Icons.email), title: const Text('Email'), subtitle: const Text('maria@importadoralopez.com')),
                  const Divider(height: 1),
                  ListTile(leading: const Icon(Icons.business), title: const Text('Empresa'), subtitle: const Text('Importadora López SA de CV')),
                ],
              ),
            ),
            const SizedBox(height: 16),
            Text('Conversaciones', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 8),
            Card(
              child: ListTile(
                title: const Text('Consulta de arroz'),
                subtitle: const Text('Cliente solicitó precios de arroz'),
                trailing: Chip(label: const Text('Cotizado', style: TextStyle(fontSize: 11)), backgroundColor: AppColors.accent.withOpacity(0.2)),
              ),
            ),
            const SizedBox(height: 16),
            Text('Seguimientos', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 8),
            Card(
              child: ListTile(
                title: const Text('Seguimiento automático'),
                subtitle: const Text('Programado para mañana a las 10:00'),
                trailing: const Icon(Icons.schedule, color: AppColors.accent),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
