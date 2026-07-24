import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class WhatsAppStatusScreen extends StatelessWidget {
  const WhatsAppStatusScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Estado de WhatsApp')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text('Selecciona un producto', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  DropdownButtonFormField(
                    decoration: const InputDecoration(labelText: 'Producto'),
                    items: ['Arroz Blanco', 'Azúcar Refinada', 'Maíz Amarillo'].map((p) => DropdownMenuItem(value: p, child: Text(p))).toList(),
                    onChanged: (_) {},
                  ),
                  const SizedBox(height: 12),
                  DropdownButtonFormField(
                    decoration: const InputDecoration(labelText: 'Objetivo'),
                    items: ['Promocionar Producto', 'Generar Leads', 'Crear Urgencia'].map((o) => DropdownMenuItem(value: o, child: Text(o))).toList(),
                    onChanged: (_) {},
                  ),
                  const SizedBox(height: 12),
                  DropdownButtonFormField(
                    decoration: const InputDecoration(labelText: 'Tono'),
                    items: ['Profesional', 'Urgente', 'Comercial', 'Amigable'].map((t) => DropdownMenuItem(value: t, child: Text(t))).toList(),
                    onChanged: (_) {},
                  ),
                  const SizedBox(height: 20),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.auto_awesome),
                      label: const Text('Generar Estado'),
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 24),
          Text('Vista Previa', style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              gradient: const LinearGradient(colors: [AppColors.primary, AppColors.primaryDark]),
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('🌾', style: TextStyle(fontSize: 40)),
                SizedBox(height: 16),
                Text('Arroz Premium - Directo de Vietnam', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                SizedBox(height: 8),
                Text('La mejor calidad al mejor precio. Contáctanos para cotización.', style: TextStyle(color: Colors.white70, fontSize: 14)),
                SizedBox(height: 24),
                Align(
                  alignment: Alignment.center,
                  child: Chip(
                    label: Text('Solicita Información', style: TextStyle(color: Colors.white)),
                    backgroundColor: Colors.white24,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
