import 'package:flutter/material.dart';

class FinanceScreen extends StatelessWidget {
  const FinanceScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          'صفحه گزارش‌ها و مالی',
          style: TextStyle(color: Colors.white, fontSize: 24),
        ),
      ),
    );
  }
}
