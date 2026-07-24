import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class ConversationsScreen extends StatelessWidget {
  const ConversationsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Conversaciones')),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: 5,
        itemBuilder: (_, i) => Card(
          margin: const EdgeInsets.only(bottom: 8),
          child: ListTile(
            leading: CircleAvatar(child: Text(['JM', 'PG', 'ML', 'CR', 'AT'][i])),
            title: Text(['Juan Martínez', 'Pedro García', 'María López', 'Carlos Ruiz', 'Ana Torres'][i]),
            subtitle: Text(['¿Tienen disponibilidad?', 'Necesito cotización', 'Precio del producto', 'Información de envío', 'Certificaciones'][i]),
            trailing: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(['10:30', '09:15', 'Ayer', 'Ayer', 'Lun'][i], style: const TextStyle(fontSize: 12, color: Colors.grey)),
                if (i == 0) const SizedBox(height: 4),
                if (i == 0) Container(
                  padding: const EdgeInsets.all(4),
                  decoration: const BoxDecoration(color: AppColors.primary, shape: BoxShape.circle),
                  child: const Text('2', style: TextStyle(color: Colors.white, fontSize: 10)),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
