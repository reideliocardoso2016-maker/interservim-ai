import 'package:flutter/material.dart';
import '../../../app/theme/app_theme.dart';

class ConversationDetailScreen extends StatelessWidget {
  final String id;
  const ConversationDetailScreen({super.key, required this.id});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Conversación')),
      body: Column(
        children: [
          Expanded(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                _MessageBubble(isUser: true, text: 'Hola, ¿tienen disponibilidad de arroz?', time: '10:30'),
                _MessageBubble(isUser: false, text: '¡Hola! Sí, tenemos arroz de alta calidad disponible. Contamos con variedad de origen vietnamita y tailandés. ¿Qué cantidad necesita?', time: '10:31'),
                _MessageBubble(isUser: true, text: 'Necesito 20 toneladas para entrega en Guatemala.', time: '10:32'),
                _MessageBubble(isUser: false, text: 'Excelente. Tenemos disponibilidad para esa cantidad. El precio por tonelada es de \$450 USD FOB. ¿Le interesaría recibir una cotización formal?', time: '10:33'),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10)],
            ),
            child: Row(
              children: [
                IconButton(icon: const Icon(Icons.attach_file), onPressed: () {}),
                Expanded(
                  child: TextField(
                    decoration: InputDecoration(
                      hintText: 'Escribe un mensaje...',
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(24)),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  icon: const Icon(Icons.send, color: AppColors.primary),
                  onPressed: () {},
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _MessageBubble extends StatelessWidget {
  final bool isUser;
  final String text, time;

  const _MessageBubble({required this.isUser, required this.text, required this.time});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(12),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
        decoration: BoxDecoration(
          color: isUser ? AppColors.primary : Colors.grey[100],
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 16),
          ),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(text, style: TextStyle(color: isUser ? Colors.white : Colors.black87)),
            const SizedBox(height: 4),
            Text(time, style: TextStyle(fontSize: 11, color: isUser ? Colors.white70 : Colors.grey)),
          ],
        ),
      ),
    );
  }
}
