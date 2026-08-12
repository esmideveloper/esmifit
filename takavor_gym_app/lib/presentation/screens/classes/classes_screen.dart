import 'package:flutter/material.dart';

class ClassesScreen extends StatelessWidget {
  const ClassesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          'صفحه کلاس‌ها و تقویم',
          style: TextStyle(color: Colors.white, fontSize: 24),
        ),
      ),
    );
  }
}
