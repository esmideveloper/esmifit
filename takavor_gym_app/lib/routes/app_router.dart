import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../screens/dashboard/dashboard_screen.dart';
import '../screens/members/members_screen.dart';
import '../screens/finance/finance_screen.dart';
import '../screens/classes/classes_screen.dart';
import '../screens/settings/settings_screen.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: '/dashboard',
  routes: [
    GoRoute(
      path: '/dashboard',
      name: 'dashboard',
      builder: (context, state) => const DashboardScreen(),
    ),
    GoRoute(
      path: '/members',
      name: 'members',
      builder: (context, state) => const MembersScreen(),
    ),
    GoRoute(
      path: '/finance',
      name: 'finance',
      builder: (context, state) => const FinanceScreen(),
    ),
    GoRoute(
      path: '/classes',
      name: 'classes',
      builder: (context, state) => const ClassesScreen(),
    ),
    GoRoute(
      path: '/settings',
      name: 'settings',
      builder: (context, state) => const SettingsScreen(),
    ),
  ],
);
