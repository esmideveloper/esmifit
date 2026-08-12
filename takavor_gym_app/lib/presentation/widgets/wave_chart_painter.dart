import 'dart:math' as math;
import 'dart:ui';
import 'package:flutter/material.dart';

/// Wave chart painter with exact animation timings
/// - drawLine animation with path metric (stroke-dashoffset 1→0)
/// - fill wipe left→right with wipeX (fill ~220ms behind stroke)
class WaveChartPainter extends CustomPainter {
  final List<double> data;
  final Animation<double> drawAnimation;
  final Animation<double> fillAnimation;
  final double u;
  
  WaveChartPainter({
    required this.data,
    required this.drawAnimation,
    required this.fillAnimation,
    required this.u,
  }) : super(repaint: Listenable.merge([drawAnimation, fillAnimation]));
  
  @override
  void paint(Canvas canvas, Size size) {
    if (data.isEmpty) return;
    
    final width = size.width;
    final height = size.height;
    
    // Create wave path based on data points
    final path = _createWavePath(width, height);
    final fillPath = _createFillPath(width, height, path);
    
    // Stroke gradient (horizontal white with opacity)
    final strokeGradient = LinearGradient(
      begin: Alignment.centerLeft,
      end: Alignment.centerRight,
      colors: [
        Colors.white.withOpacity(0.9),
        Colors.white.withOpacity(0.5),
      ],
    );
    
    // Draw stroke (animated)
    final strokePaint = Paint()
      ..shader = strokeGradient.createShader(Rect.fromLTWH(0, 0, width, height))
      ..style = PaintingStyle.stroke
      ..strokeWidth = 3 * u
      ..strokeCap = StrokeCap.round;
    
    // Animate stroke drawing using path metrics
    final pathMetrics = path.computeMetrics();
    for (final metric in pathMetrics) {
      final extractLength = metric.length * drawAnimation.value;
      final extractedPath = metric.extractPath(0, extractLength);
      canvas.drawPath(extractedPath, strokePaint);
    }
    
    // Draw fill (wipes in after stroke, ~220ms delay)
    if (fillAnimation.value > 0) {
      // Vertical fade mask for fill
      final fillGradient = LinearGradient(
        begin: Alignment.topCenter,
        end: Alignment.bottomCenter,
        colors: [
          Colors.white.withOpacity(0.3 * fillAnimation.value),
          Colors.white.withOpacity(0.1 * fillAnimation.value),
          Colors.transparent,
        ],
        stops: const [0.0, 0.5, 1.0],
      );
      
      final fillPaint = Paint()
        ..shader = fillGradient.createShader(Rect.fromLTWH(0, 0, width, height))
        ..style = PaintingStyle.fill
        ..blendMode = BlendMode.srcOver;
      
      // Clip fill to progressive reveal from left to right
      final revealWidth = width * fillAnimation.value;
      canvas.save();
      canvas.clipRect(Rect.fromLTWH(0, 0, revealWidth, height));
      canvas.drawPath(fillPath, fillPaint);
      canvas.restore();
    }
    
    // Draw three additional stroke paths with different opacities (ghost lines)
    final ghostPaths = _createGhostPaths(width, height);
    for (int i = 0; i < ghostPaths.length; i++) {
      final ghostPaint = Paint()
        ..color = Colors.white.withOpacity(0.15 - (i * 0.04))
        ..style = PaintingStyle.stroke
        ..strokeWidth = (2 - i * 0.5) * u
        ..strokeCap = StrokeCap.round;
      
      final metric = ghostPaths[i].computeMetrics().first;
      final extractLength = metric.length * drawAnimation.value;
      final extractedPath = metric.extractPath(0, extractLength);
      canvas.drawPath(extractedPath, ghostPaint);
    }
  }
  
  Path _createWavePath(double width, double height) {
    final path = Path();
    
    // Normalize data to fit in canvas
    final maxValue = data.reduce(math.max);
    final minValue = data.reduce(math.min);
    final range = maxValue - minValue;
    
    final segmentWidth = width / (data.length - 1);
    final padding = height * 0.15;
    final drawHeight = height - (padding * 2);
    
    // Start point
    final startX = 0.0;
    final startY = padding + drawHeight - ((data[0] - minValue) / range) * drawHeight;
    path.moveTo(startX, startY);
    
    // Create smooth curve through points
    for (int i = 1; i < data.length; i++) {
      final x = i * segmentWidth;
      final y = padding + drawHeight - ((data[i] - minValue) / range) * drawHeight;
      
      // Use quadratic bezier for smooth curves
      final prevX = (i - 1) * segmentWidth;
      final prevY = padding + drawHeight - ((data[i - 1] - minValue) / range) * drawHeight;
      final controlX = (prevX + x) / 2;
      final controlY = (prevY + y) / 2;
      
      path.quadraticBezierTo(controlX, controlY, x, y);
    }
    
    return path;
  }
  
  Path _createFillPath(double width, double height, Path wavePath) {
    final fillPath = Path();
    fillPath.addPath(wavePath, Offset.zero);
    
    // Close the path to bottom for fill
    fillPath.lineTo(width, height);
    fillPath.lineTo(0, height);
    fillPath.close();
    
    return fillPath;
  }
  
  List<Path> _createGhostPaths(double width, double height) {
    // Create offset versions of the main wave for layered effect
    final baseOffset = 8 * u;
    final paths = <Path>[];
    
    for (int i = 1; i <= 3; i++) {
      final offsetPath = Path();
      
      final maxValue = data.reduce(math.max);
      final minValue = data.reduce(math.min);
      final range = maxValue - minValue;
      
      final segmentWidth = width / (data.length - 1);
      final padding = height * 0.15 + (i * baseOffset);
      final drawHeight = height - (padding * 2);
      
      final startX = 0.0;
      final startY = padding + drawHeight - ((data[0] - minValue) / range) * drawHeight;
      offsetPath.moveTo(startX, startY);
      
      for (int j = 1; j < data.length; j++) {
        final x = j * segmentWidth;
        final y = padding + drawHeight - ((data[j] - minValue) / range) * drawHeight;
        
        final prevX = (j - 1) * segmentWidth;
        final prevY = padding + drawHeight - ((data[j - 1] - minValue) / range) * drawHeight;
        final controlX = (prevX + x) / 2;
        final controlY = (prevY + y) / 2;
        
        offsetPath.quadraticBezierTo(controlX, controlY, x, y);
      }
      
      paths.add(offsetPath);
    }
    
    return paths;
  }
  
  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
