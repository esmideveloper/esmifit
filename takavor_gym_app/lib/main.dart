import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:window_manager/window_manager.dart';
import 'presentation/providers/app_providers.dart';
import 'presentation/screens/dashboard/dashboard_screen.dart';
import 'routes/app_router.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize window manager for desktop
  await windowManager.ensureInitialized();
  
  WindowOptions windowOptions = const WindowOptions(
    size: Size(1357, 871),
    minimumSize: Size(1024, 768),
    center: true,
    title: 'داشبورد مدیریت — باشگاه تکاور',
    titleBarStyle: TitleBarStyle.normal,
  );
  
  await windowManager.waitUntilReadyToShow(windowOptions, () async {
    await windowManager.show();
    await windowManager.focus();
  });
  
  // Set system UI overlay style
  SystemChrome.setSystemUIOverlayStyle(const SystemUiOverlayStyle(
    statusBarColor: Colors.transparent,
    statusBarIconBrightness: Brightness.light,
  ));
  
  runApp(const TakavorGymApp());
}

class TakavorGymApp extends StatelessWidget {
  const TakavorGymApp({super.key});

  @override
  Widget build(BuildContext context) {
    return ProviderScope(
      child: MaterialApp.router(
        title: 'داشبورد مدیریت — باشگاه تکاور',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          fontFamily: 'Vazirmatn',
          brightness: Brightness.dark,
          primaryColor: const Color(0xFFFFFFFF),
          scaffoldBackgroundColor: const Color(0xFF04121B),
          colorScheme: const ColorScheme.dark(
            primary: Color(0xFFFFFFFF),
            secondary: Color(0xFFFFFFFF),
            surface: Color(0xFF04121B),
            background: Color(0xFF04121B),
          ),
          textTheme: const TextTheme(
            displayLarge: TextStyle(
              fontFamily: 'Vazirmatn',
              fontWeight: FontWeight.w500,
              fontFeatures: [FontFeature.enable('kern')],
            ),
            headlineLarge: TextStyle(
              fontFamily: 'Vazirmatn',
              fontWeight: FontWeight.w500,
              fontFeatures: [FontFeature.enable('kern')],
            ),
            bodyLarge: TextStyle(
              fontFamily: 'Vazirmatn',
              fontWeight: FontWeight.w500,
              fontFeatures: [FontFeature.enable('kern')],
            ),
          ),
        ),
        routerConfig: appRouter,
        builder: (context, child) {
          return Directionality(
            textDirection: TextDirection.rtl,
            child: child!,
          );
        },
      ),
    );
  }
}
