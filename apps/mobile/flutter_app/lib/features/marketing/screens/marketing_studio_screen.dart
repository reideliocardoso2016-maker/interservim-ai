import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class MarketingStudioScreen extends StatelessWidget {
  const MarketingStudioScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Marketing IA')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Generar Contenido', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          _MarketingCard(
            icon: Icons.campaign,
            title: 'Estado de WhatsApp',
            subtitle: 'Crea contenido para estados',
            color: AppColors.primary,
          ),
          _MarketingCard(
            icon: Icons.message,
            title: 'Mensaje Comercial',
            subtitle: 'Redacta mensajes de venta',
            color: AppColors.secondary,
          ),
          _MarketingCard(
            icon: Icons.article,
            title: 'Anuncio Publicitario',
            subtitle: 'Genera anuncios para productos',
            color: AppColors.accent,
          ),
          _MarketingCard(
            icon: Icons.email,
            title: 'Email Comercial',
            subtitle: 'Crea campañas de email',
            color: AppColors.info,
          ),
          _MarketingCard(
            icon: Icons.flight,
            title: 'Campaña de Importación',
            subtitle: 'Promociona servicios de importación',
            color: AppColors.error,
          ),
          const SizedBox(height: 24),
          Text('Campañas Activas', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              title: const Text('Campaña Arroz Julio'),
              subtitle: const Text('5 contenidos generados • Activa'),
              trailing: Chip(label: const Text('Activa', style: TextStyle(fontSize: 11)), backgroundColor: AppColors.success.withOpacity(0.2)),
            ),
          ),
        ],
      ),
    );
  }
}

class _MarketingCard extends StatelessWidget {
  final IconData icon;
  final String title, subtitle;
  final Color color;

  const _MarketingCard({required this.icon, required this.title, required this.subtitle, required this.color});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
          child: Icon(icon, color: color),
        ),
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => Scaffold(
          appBar: AppBar(title: Text(title)),
          body: const Center(child: Text('Content generator - Coming Soon')),
        ))),
      ),
    );
  }
}
