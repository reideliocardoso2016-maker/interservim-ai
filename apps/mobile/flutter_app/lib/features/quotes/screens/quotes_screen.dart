import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class QuotesScreen extends StatelessWidget {
  const QuotesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Cotizaciones')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _QuoteCard(number: 'COT-20240724-0001', client: 'Importadora López', amount: 9000, status: 'Enviada'),
          _QuoteCard(number: 'COT-20240724-0002', client: 'Distribuidora Ruiz', amount: 7600, status: 'Borrador'),
          _QuoteCard(number: 'COT-20240723-0001', client: 'Torres Retail', amount: 5500, status: 'Aceptada'),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}

class _QuoteCard extends StatelessWidget {
  final String number, client, status;
  final double amount;

  const _QuoteCard({required this.number, required this.client, required this.amount, required this.status});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(number, style: const TextStyle(fontWeight: FontWeight.w600)),
                Chip(
                  label: Text(status, style: const TextStyle(fontSize: 11, color: Colors.white)),
                  backgroundColor: status == 'Aceptada' ? AppColors.success : status == 'Enviada' ? AppColors.accent : Colors.grey,
                  padding: EdgeInsets.zero,
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(client, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 4),
            Text('\$${amount.toStringAsFixed(2)} USD', style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: AppColors.primary)),
          ],
        ),
      ),
    );
  }
}
