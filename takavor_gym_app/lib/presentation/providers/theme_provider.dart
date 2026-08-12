import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class ThemeState {
  final double u; // Scaling unit
  final bool reduceMotion;
  
  const ThemeState({
    this.u = 1.0,
    this.reduceMotion = false,
  });
  
  ThemeState copyWith({double? u, bool? reduceMotion}) {
    return ThemeState(
      u: u ?? this.u,
      reduceMotion: reduceMotion ?? this.reduceMotion,
    );
  }
}

final themeProvider = StateNotifierProvider<ThemeNotifier, ThemeState>((ref) {
  return ThemeNotifier();
});

class ThemeNotifier extends StateNotifier<ThemeState> {
  ThemeNotifier() : super(const ThemeState());
  
  void updateScalingUnit(double u) {
    state = state.copyWith(u: u);
  }
  
  void setReduceMotion(bool value) {
    state = state.copyWith(reduceMotion: value);
  }
}

// Liquid Glass Color Constants
class GlassColors {
  static const ink = Color(0xFFFFFFFF);
  static const glass = Color(0x27FFFFFF); // rgba(255,255,255,.155)
  static const glassLine = Color(0x33FFFFFF); // rgba(255,255,255,.20)
  static const background = Color(0xFF04121B);
  
  // Glass gradient stops
  static const glassGradientStart = Color(0x24FFFFFF); // .14
  static const glassGradientEnd = Color(0x0DFFFFFF); // .05
}
