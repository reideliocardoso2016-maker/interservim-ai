import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class ProductsScreen extends StatelessWidget {
  const ProductsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Productos')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              decoration: InputDecoration(
                hintText: 'Buscar productos...',
                prefixIcon: const Icon(Icons.search),
                filled: true,
                fillColor: Colors.grey[100],
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
              ),
            ),
          ),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              itemCount: 4,
              itemBuilder: (_, i) => Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: Padding(
                  padding: const EdgeInsets.all(12),
                  child: Row(
                    children: [
                      Container(
                        width: 80,
                        height: 80,
                        decoration: BoxDecoration(
                          color: AppColors.surface,
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: const Icon(Icons.inventory_2, color: AppColors.primary),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(['Arroz Blanco', 'Azúcar Refinada', 'Maíz Amarillo', 'Frijol Negro'][i], style: Theme.of(context).textTheme.labelLarge),
                            const SizedBox(height: 4),
                            Text(['\$450 USD/Ton • Vietnam', '\$380 USD/Ton • Brasil', '\$320 USD/Ton • USA', '\$550 USD/Ton • Uganda'][i], style: Theme.of(context).textTheme.bodyMedium),
                            const SizedBox(height: 8),
                            Chip(
                              label: Text('Disponible', style: const TextStyle(fontSize: 11, color: Colors.white)),
                              backgroundColor: AppColors.success,
                              padding: EdgeInsets.zero,
                              materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
                            ),
                          ],
                        ),
                      ),
                      IconButton(
                        icon: const Icon(Icons.chevron_right),
                        onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => Scaffold(
                          appBar: AppBar(title: Text(['Arroz Blanco', 'Azúcar Refinada', 'Maíz Amarillo', 'Frijol Negro'][i])),
                        ))),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {},
        child: const Icon(Icons.add),
      ),
    );
  }
}
