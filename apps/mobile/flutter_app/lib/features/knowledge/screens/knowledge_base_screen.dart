import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class KnowledgeBaseScreen extends StatelessWidget {
  const KnowledgeBaseScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Base de Conocimiento')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Documentos', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          Card(
            child: ListTile(
              leading: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(color: AppColors.error.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                child: const Icon(Icons.picture_as_pdf, color: AppColors.error),
              ),
              title: const Text('Catálogo de Productos 2024'),
              subtitle: const Text('PDF • 2.4 MB • Procesado'),
              trailing: const Chip(label: Text('Listo', style: TextStyle(fontSize: 11)), backgroundColor: AppColors.success),
            ),
          ),
          Card(
            child: ListTile(
              leading: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(color: AppColors.info.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                child: const Icon(Icons.description, color: AppColors.info),
              ),
              title: const Text('Condiciones Comerciales'),
              subtitle: const Text('DOCX • 156 KB • Procesado'),
              trailing: const Chip(label: Text('Listo', style: TextStyle(fontSize: 11)), backgroundColor: AppColors.success),
            ),
          ),
          Card(
            child: ListTile(
              leading: Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(color: AppColors.secondary.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
                child: const Icon(Icons.table_chart, color: AppColors.secondary),
              ),
              title: const Text('Precios Mayoristas'),
              subtitle: const Text('XLSX • 89 KB • Procesado'),
              trailing: const Chip(label: Text('Listo', style: TextStyle(fontSize: 11)), backgroundColor: AppColors.success),
            ),
          ),
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            child: OutlinedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.upload_file),
              label: const Text('Subir Documento'),
            ),
          ),
        ],
      ),
    );
  }
}
