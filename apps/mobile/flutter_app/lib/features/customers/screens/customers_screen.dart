import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class CustomersScreen extends StatelessWidget {
  const CustomersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final customers = [
      {'name': 'María López', 'company': 'Importadora López', 'country': 'México', 'type': 'IMPORTADOR', 'status': 'ACTIVO'},
      {'name': 'Carlos Ruiz', 'company': 'Distribuidora Ruiz', 'country': 'Colombia', 'type': 'DISTRIBUIDOR', 'status': 'COTIZADO'},
      {'name': 'Ana Torres', 'company': 'Torres Retail', 'country': 'Perú', 'type': 'MINORISTA', 'status': 'NUEVO'},
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Clientes')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: customers.length,
        itemBuilder: (_, i) => Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: CircleAvatar(child: Text(customers[i]['name']![0])),
            title: Text(customers[i]['name']!),
            subtitle: Text('${customers[i]['company']} • ${customers[i]['country']}'),
            trailing: Chip(
              label: Text(customers[i]['status']!, style: const TextStyle(fontSize: 11, color: Colors.white)),
              backgroundColor: [AppColors.success, AppColors.accent, AppColors.primary][i],
              padding: EdgeInsets.zero,
            ),
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}
