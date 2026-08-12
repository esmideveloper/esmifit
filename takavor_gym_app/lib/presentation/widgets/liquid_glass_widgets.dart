import 'dart:ui';
import 'package:flutter/material.dart';
import '../../providers/theme_provider.dart';

/// Liquid Glass Background with full-bleed image and vignette overlay
class LiquidGlassBackground extends StatelessWidget {
  const LiquidGlassBackground({super.key});

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        // Full-bleed background image
        Positioned.fill(
          child: Image.asset(
            'assets/images/storm-background.jpg',
            fit: BoxFit.cover,
            alignment: Alignment.center,
            errorBuilder: (context, error, stackTrace) {
              return Container(
                color: GlassColors.background,
              );
            },
          ),
        ),
        
        // Vignette overlay (multiple gradient layers)
        Positioned.fill(
          child: IgnorePointer(
            child: Opacity(
              opacity: 0.6,
              child: Container(
                decoration: BoxDecoration(
                  gradient: RadialGradient(
                    center: Alignment.center,
                    radius: 1.2,
                    colors: [
                      Colors.transparent,
                      GlassColors.background.withOpacity(0.3),
                      GlassColors.background.withOpacity(0.7),
                    ],
                    stops: const [0.4, 0.7, 1.0],
                  ),
                ),
              ),
            ),
          ),
        ),
        
        // Top-bottom dark overlays
        Positioned.fill(
          child: IgnorePointer(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    GlassColors.background.withOpacity(0.4),
                    Colors.transparent,
                    Colors.transparent,
                    GlassColors.background.withOpacity(0.4),
                  ],
                  stops: const [0.0, 0.15, 0.85, 1.0],
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

/// Glass Panel with BackdropFilter blur and exact liquid glass recipe
class GlassPanel extends StatelessWidget {
  final Widget child;
  final double? borderRadius;
  final double? height;
  final EdgeInsetsGeometry? padding;
  final Color? backgroundColor;
  
  const GlassPanel({
    super.key,
    required this.child,
    this.borderRadius,
    this.height,
    this.padding,
    this.backgroundColor,
  });

  @override
  Widget build(BuildContext context) {
    final r = borderRadius ?? 16.0;
    
    return ClipRRect(
      borderRadius: BorderRadius.circular(r),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 18, sigmaY: 18),
        child: Container(
          height: height,
          padding: padding,
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [
                GlassColors.glassGradientStart,
                GlassColors.glassGradientEnd,
              ],
            ),
            border: Border.all(
              color: GlassColors.glassLine,
              width: 1.0,
            ),
            borderRadius: BorderRadius.circular(r),
          ),
          child: Stack(
            children: [
              child,
              
              // Specular sheen layer (::after equivalent)
              Positioned.fill(
                child: ClipRect(
                  child: FractionallySizedBox(
                    widthFactor: 0.38,
                    alignment: Alignment.topLeft,
                    child: Transform.rotate(
                      angle: -0.314, // -18 degrees in radians
                      child: Container(
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.centerLeft,
                            end: Alignment.centerRight,
                            colors: [
                              Colors.transparent,
                              Colors.white.withOpacity(0.17),
                              Colors.transparent,
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

/// Logo painter - wave circle mark
class LogoPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.white
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.5
      ..strokeCap = StrokeCap.round;
    
    final fillPaint = Paint()
      ..color = Colors.white.withOpacity(0.2)
      ..style = PaintingStyle.fill;
    
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2 - 4;
    
    // Draw circle
    canvas.drawCircle(center, radius, paint..style = PaintingStyle.stroke);
    
    // Draw wave inside
    final wavePath = Path();
    wavePath.moveTo(center.dx - radius * 0.6, center.dy);
    wavePath.quadraticBezierTo(
      center.dx - radius * 0.2,
      center.dy - radius * 0.3,
      center.dx,
      center.dy,
    );
    wavePath.quadraticBezierTo(
      center.dx + radius * 0.2,
      center.dy + radius * 0.3,
      center.dx + radius * 0.6,
      center.dy,
    );
    
    canvas.drawPath(wavePath, paint..style = PaintingStyle.stroke);
  }
  
  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
