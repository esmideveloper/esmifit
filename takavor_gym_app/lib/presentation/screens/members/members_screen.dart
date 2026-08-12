import 'package:flutter/material.dart';

class MembersScreen extends StatelessWidget {
  const MembersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Text(
          'صفحه مدیریت اعضا و اشتراک‌ها',
          style: TextStyle(color: Colors.white, fontSize: 24),
        ),
      ),
    );
  }
}
