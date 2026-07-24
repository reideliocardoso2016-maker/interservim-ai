import 'package:flutter/material.dart';

class QuoteDetailScreen extends StatelessWidget {
  final String id;
  const QuoteDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Cotización')),
      body: const Center(child: Text('Quote Detail - Coming Soon')),
    );
  }
}
