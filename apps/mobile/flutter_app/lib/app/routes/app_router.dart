import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter/material.dart';
import '../../features/auth/screens/splash_screen.dart';
import '../../features/dashboard/screens/dashboard_screen.dart';
import '../../features/conversations/screens/conversations_screen.dart';
import '../../features/conversations/screens/conversation_detail_screen.dart';
import '../../features/customers/screens/customers_screen.dart';
import '../../features/customers/screens/customer_detail_screen.dart';
import '../../features/products/screens/products_screen.dart';
import '../../features/products/screens/product_detail_screen.dart';
import '../../features/quotes/screens/quotes_screen.dart';
import '../../features/quotes/screens/quote_detail_screen.dart';
import '../../features/marketing/screens/marketing_studio_screen.dart';
import '../../features/marketing/screens/whatsapp_status_screen.dart';
import '../../features/knowledge/screens/knowledge_base_screen.dart';
import '../../features/analytics/screens/analytics_screen.dart';
import '../../features/settings/screens/settings_screen.dart';
import '../providers/auth_provider.dart';

class AppRouter {
  static GoRouter createRouter(WidgetRef ref) {
    final authState = ref.watch(authProvider);
    return GoRouter(
      initialLocation: '/splash',
      redirect: (context, state) {
        final isLoggedIn = authState.isAuthenticated;
        if (!isLoggedIn && state.matchedLocation != '/splash') return '/splash';
        return null;
      },
      routes: [
        GoRoute(path: '/splash', builder: (_, __) => const SplashScreen()),
        GoRoute(
          path: '/dashboard',
          builder: (_, __) => const DashboardScreen(),
          routes: [
            GoRoute(path: 'conversations', builder: (_, __) => const ConversationsScreen()),
            GoRoute(path: 'conversations/:id', builder: (_, state) => ConversationDetailScreen(id: state.pathParameters['id']!)),
            GoRoute(path: 'customers', builder: (_, __) => const CustomersScreen()),
            GoRoute(path: 'customers/:id', builder: (_, state) => CustomerDetailScreen(id: state.pathParameters['id']!)),
            GoRoute(path: 'products', builder: (_, __) => const ProductsScreen()),
            GoRoute(path: 'products/:id', builder: (_, state) => ProductDetailScreen(id: state.pathParameters['id']!)),
            GoRoute(path: 'quotes', builder: (_, __) => const QuotesScreen()),
            GoRoute(path: 'quotes/:id', builder: (_, state) => QuoteDetailScreen(id: state.pathParameters['id']!)),
            GoRoute(path: 'marketing', builder: (_, __) => const MarketingStudioScreen()),
            GoRoute(path: 'marketing/status', builder: (_, __) => const WhatsAppStatusScreen()),
            GoRoute(path: 'knowledge', builder: (_, __) => const KnowledgeBaseScreen()),
            GoRoute(path: 'analytics', builder: (_, __) => const AnalyticsScreen()),
            GoRoute(path: 'settings', builder: (_, __) => const SettingsScreen()),
          ],
        ),
      ],
    );
  }
}
