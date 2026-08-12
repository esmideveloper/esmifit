import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../providers/app_providers.dart';
import '../../widgets/liquid_glass_widgets.dart';
import '../../widgets/wave_chart_painter.dart';
import '../../../routes/app_router.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen>
    with TickerProviderStateMixin {
  double _u = 1.0;
  
  // Animation controllers for entry choreography
  late AnimationController _riseInController;
  late AnimationController _slideLController;
  late AnimationController _slideRController;
  late AnimationController _popInController;
  late AnimationController _lineUpController;
  late AnimationController _wipeDownController;
  late AnimationController _drawLineController;
  late AnimationController _wipeXController;
  late AnimationController _sheenController;
  
  @override
  void initState() {
    super.initState();
    
    // Initialize animation controllers with exact timings from spec
    _riseInController = AnimationController(
      duration: const Duration(milliseconds: 750),
      vsync: this,
    );
    
    _slideLController = AnimationController(
      duration: const Duration(milliseconds: 620),
      vsync: this,
    );
    
    _slideRController = AnimationController(
      duration: const Duration(milliseconds: 620),
      vsync: this,
    );
    
    _popInController = AnimationController(
      duration: const Duration(milliseconds: 420),
      vsync: this,
    );
    
    _lineUpController = AnimationController(
      duration: const Duration(milliseconds: 520),
      vsync: this,
    );
    
    _wipeDownController = AnimationController(
      duration: const Duration(milliseconds: 580),
      vsync: this,
    );
    
    _drawLineController = AnimationController(
      duration: const Duration(milliseconds: 1250),
      vsync: this,
    );
    
    _wipeXController = AnimationController(
      duration: const Duration(milliseconds: 220),
      vsync: this,
    );
    
    _sheenController = AnimationController(
      duration: const Duration(milliseconds: 1150),
      vsync: this,
    );
    
    // Start animations with delays matching spec
    _startAnimations();
  }
  
  void _startAnimations() {
    Future.delayed(const Duration(milliseconds: 0), () {
      _riseInController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 180), () {
      _slideLController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 180), () {
      _slideRController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 420), () {
      _popInController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 520), () {
      _lineUpController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 680), () {
      _wipeDownController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 850), () {
      _drawLineController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 1070), () {
      _wipeXController.forward();
    });
    
    Future.delayed(const Duration(milliseconds: 2550), () {
      _sheenController.forward();
    });
  }
  
  @override
  void dispose() {
    _riseInController.dispose();
    _slideLController.dispose();
    _slideRController.dispose();
    _popInController.dispose();
    _lineUpController.dispose();
    _wipeDownController.dispose();
    _drawLineController.dispose();
    _wipeXController.dispose();
    _sheenController.dispose();
    super.dispose();
  }
  
  void _updateScalingUnit(double screenWidth, double screenHeight) {
    setState(() {
      _u = (screenWidth / 1357).clamp(0.5, 2.0);
      ref.read(themeProvider.notifier).updateScalingUnit(_u);
    });
  }
  
  @override
  Widget build(BuildContext context) {
    final gymData = ref.watch(gymDataProvider);
    final user = ref.watch(userProvider).currentUser;
    
    return LayoutBuilder(
      builder: (context, constraints) {
        _updateScalingUnit(constraints.maxWidth, constraints.maxHeight);
        
        return Stack(
          children: [
            // Full-bleed background with vignette overlay
            const LiquidGlassBackground(),
            
            // Main stage
            Stack(
              children: [
                // Left Sidebar
                _buildSidebar(context, gymData),
                
                // Header
                _buildHeader(context, user),
                
                // Hero section
                _buildHero(context),
                
                // Forecast strip with chart
                _buildForecastStrip(context, gymData),
                
                // Right rail cards
                _buildRightRail(context, gymData),
              ],
            ),
          ],
        );
      },
    );
  }
  
  Widget _buildSidebar(BuildContext context, GymDataState gymData) {
    final navItems = [
      {'icon': Icons.dashboard, 'label': 'داشبورد', 'route': '/dashboard', 'active': true},
      {'icon': Icons.people, 'label': 'اعضا و اشتراک‌ها', 'route': '/members'},
      {'icon': Icons.account_balance_wallet, 'label': 'گزارش‌ها و مالی', 'route': '/finance'},
      {'icon': Icons.calendar_today, 'label': 'کلاس‌ها/تقویم', 'route': '/classes'},
      {'icon': Icons.settings, 'label': 'تنظیمات', 'route': '/settings'},
    ];
    
    return Positioned(
      left: 16 * _u,
      top: 14 * _u,
      bottom: 7 * _u,
      width: 72 * _u,
      child: AnimatedBuilder(
        animation: _slideLController,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset((-50 * (1 - _slideLController.value)) * _u, 0),
            child: Opacity(
              opacity: _slideLController.value,
              child: child,
            ),
          );
        },
        child: GlassPanel(
          borderRadius: 18 * _u,
          child: Column(
            children: [
              SizedBox(height: 22 * _u),
              
              // Logo
              SizedBox(
                width: 40 * _u,
                height: 40 * _u,
                child: CustomPaint(
                  painter: LogoPainter(),
                ),
              ),
              
              SizedBox(height: 57.5 * _u),
              
              // Navigation
              Expanded(
                child: Column(
                  children: List.generate(navItems.length, (index) {
                    final item = navItems[index];
                    final isActive = item['active'] as bool? ?? false;
                    
                    return Padding(
                      padding: EdgeInsets.symmetric(vertical: 4 * _u),
                      child: MouseRegion(
                        cursor: SystemMouseCursors.click,
                        child: GestureDetector(
                          onTap: () {
                            if (!isActive) {
                              context.go(item['route'] as String);
                            }
                          },
                          child: AnimatedContainer(
                            duration: const Duration(milliseconds: 200),
                            padding: EdgeInsets.all(10 * _u),
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(8 * _u),
                              color: isActive 
                                  ? Colors.white.withOpacity(0.24)
                                  : Colors.transparent,
                            ),
                            child: Column(
                              children: [
                                Icon(
                                  item['icon'] as IconData,
                                  size: 23 * _u,
                                  color: Colors.white,
                                ),
                                if (isActive) ...[
                                  SizedBox(height: 4 * _u),
                                  Text(
                                    item['label'] as String,
                                    style: TextStyle(
                                      fontSize: 10 * _u,
                                      color: Colors.white,
                                    ),
                                  ),
                                ],
                              ],
                            ),
                          ),
                        ),
                      ),
                    );
                  }),
                ),
              ),
              
              // Active indicator pip
              Positioned(
                left: -2 * _u,
                top: 131 * _u,
                child: Container(
                  width: 5 * _u,
                  height: 29 * _u,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(3 * _u),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.white.withOpacity(0.55),
                        blurRadius: 10 * _u,
                      ),
                    ],
                  ),
                ),
              ),
              
              SizedBox(height: 52 * _u),
              
              // Logout
              MouseRegion(
                cursor: SystemMouseCursors.click,
                child: GestureDetector(
                  onTap: () {
                    ref.read(userProvider.notifier).logout();
                  },
                  child: Padding(
                    padding: EdgeInsets.all(10 * _u),
                    child: Icon(
                      Icons.logout,
                      size: 23 * _u,
                      color: Colors.white.withOpacity(0.8),
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
  
  Widget _buildHeader(BuildContext context, dynamic user) {
    return Positioned(
      top: 22 * _u,
      left: 126 * _u,
      right: 37 * _u,
      height: 52 * _u,
      child: AnimatedBuilder(
        animation: _riseInController,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset(0, (20 * (1 - _riseInController.value)) * _u),
            child: Opacity(
              opacity: _riseInController.value,
              child: child,
            ),
          );
        },
        child: Row(
          children: [
            // Left block - Welcome text (RTL)
            Expanded(
              child: Directionality(
                textDirection: TextDirection.rtl,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'خوش آمدید',
                      style: TextStyle(
                        fontSize: 14 * _u,
                        color: Colors.white.withOpacity(0.7),
                        fontFamily: 'Vazirmatn',
                      ),
                    ),
                    Text(
                      user?.name ?? 'مدیر باشگاه تکاور',
                      style: TextStyle(
                        fontSize: 18 * _u,
                        fontWeight: FontWeight.w600,
                        color: Colors.white,
                        fontFamily: 'Vazirmatn',
                      ),
                    ),
                  ],
                ),
              ),
            ),
            
            // Right tools
            Row(
              children: [
                _buildToolButton(Icons.add, 'افزودن'),
                SizedBox(width: 16 * _u),
                _buildToolButton(Icons.search, 'جستجو'),
                SizedBox(width: 16 * _u),
                _buildToolButton(Icons.notifications_outlined, 'اعلان‌ها'),
                SizedBox(width: 16 * _u),
                // Avatar
                MouseRegion(
                  cursor: SystemMouseCursors.click,
                  child: Container(
                    width: 52 * _u,
                    height: 52 * _u,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: Colors.white.withOpacity(0.2),
                        width: 1 * _u,
                      ),
                    ),
                    child: ClipOval(
                      child: Image.asset(
                        'assets/images/avatar.jpg',
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) {
                          return Icon(
                            Icons.person,
                            size: 26 * _u,
                            color: Colors.white,
                          );
                        },
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
  
  Widget _buildToolButton(IconData icon, String label) {
    return MouseRegion(
      cursor: SystemMouseCursors.click,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        width: 52 * _u,
        height: 52 * _u,
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.15),
          borderRadius: BorderRadius.circular(12 * _u),
          border: Border.all(
            color: Colors.white.withOpacity(0.2),
            width: 1 * _u,
          ),
        ),
        child: Icon(
          icon,
          size: 22 * _u,
          color: Colors.white,
        ),
      ),
    );
  }
  
  Widget _buildHero(BuildContext context) {
    return Positioned(
      left: 126 * _u,
      top: 136 * _u,
      child: AnimatedBuilder(
        animation: _slideLController,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset((-30 * (1 - _slideLController.value)) * _u, 0),
            child: Opacity(
              opacity: _slideLController.value,
              child: child,
            ),
          );
        },
        child: ConstrainedBox(
          constraints: BoxConstraints(maxWidth: 560 * _u),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Chip
              Container(
                padding: EdgeInsets.symmetric(
                  horizontal: 14 * _u,
                  vertical: 6 * _u,
                ),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(20 * _u),
                  border: Border.all(
                    color: Colors.white.withOpacity(0.3),
                    width: 1 * _u,
                  ),
                ),
                child: Text(
                  'داشبورد مدیریت',
                  style: TextStyle(
                    fontSize: 13 * _u,
                    color: Colors.white,
                    fontFamily: 'Vazirmatn',
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ),
              
              SizedBox(height: 24 * _u),
              
              // H1 - Two lines with mask reveal
              _buildAnimatedText(
                'تکاور',
                fontSize: 63 * _u,
                fontWeight: FontWeight.w500,
                letterSpacing: 0.25 * _u,
                height: 78 / 63,
              ),
              
              SizedBox(height: 8 * _u),
              
              _buildAnimatedText(
                'مدیریت باشگاه',
                fontSize: 63 * _u,
                fontWeight: FontWeight.w500,
                letterSpacing: 0.25 * _u,
                height: 78 / 63,
              ),
              
              SizedBox(height: 24 * _u),
              
              // Blurb
              SizedBox(
                width: 480 * _u,
                child: Text(
                  'نمای کلی امروز: وضعیت اعضا، تمدیدها، حضور و غیاب و درآمد.\n'
                  'از نوار ابزار برای ثبت‌نام سریع، صدور فاکتور و ثبت جلسات\n'
                  'استفاده کنید. گزارش‌ها قابل خروجی PDF/Excel هستند.',
                  textAlign: TextAlign.right,
                  style: TextStyle(
                    fontSize: 15.2 * _u,
                    height: 24 / 15.2,
                    fontWeight: FontWeight.w500,
                    letterSpacing: -0.3 * _u,
                    color: Colors.white.withOpacity(0.95),
                    fontFamily: 'Vazirmatn',
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
  
  Widget _buildAnimatedText(String text, {
    required double fontSize,
    required FontWeight fontWeight,
    double? letterSpacing,
    double? height,
  }) {
    return AnimatedBuilder(
      animation: _lineUpController,
      builder: (context, child) {
        return ClipRect(
          child: Align(
            alignment: Alignment.topCenter,
            heightFactor: _lineUpController.value,
            child: child,
          ),
        );
      },
      child: Text(
        text,
        style: TextStyle(
          fontSize: fontSize,
          fontWeight: fontWeight,
          letterSpacing: letterSpacing,
          height: height,
          color: Colors.white,
          fontFamily: 'Vazirmatn',
          fontFeatures: const [FontFeature.enable('kern')],
        ),
      ),
    );
  }
  
  Widget _buildForecastStrip(BuildContext context, GymDataState gymData) {
    return Positioned(
      left: 126 * _u,
      right: 396 * _u,
      bottom: 99 * _u,
      child: AnimatedBuilder(
        animation: _riseInController,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset(0, (30 * (1 - _riseInController.value)) * _u),
            child: Opacity(
              opacity: _riseInController.value,
              child: child,
            ),
          );
        },
        child: GlassPanel(
          borderRadius: 24 * _u,
          child: Padding(
            padding: EdgeInsets.all(24 * _u),
            child: Column(
              children: [
                // KPI Row
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: gymData.todayKpis.map((kpi) {
                    return Column(
                      children: [
                        Text(
                          kpi.value.toString(),
                          style: TextStyle(
                            fontSize: 37 * _u,
                            fontWeight: FontWeight.w400,
                            letterSpacing: -0.7 * _u,
                            color: Colors.white,
                            fontFamily: 'Vazirmatn',
                          ),
                        ),
                        SizedBox(height: 8 * _u),
                        Icon(
                          kpi.icon,
                          size: 20 * _u,
                          color: Colors.white.withOpacity(0.7),
                        ),
                        SizedBox(height: 4 * _u),
                        Text(
                          kpi.label,
                          style: TextStyle(
                            fontSize: 12 * _u,
                            color: Colors.white.withOpacity(0.7),
                            fontFamily: 'Vazirmatn',
                          ),
                        ),
                      ],
                    );
                  }).toList(),
                ),
                
                SizedBox(height: 43 * _u),
                
                // Wave Chart
                SizedBox(
                  height: 230 * _u,
                  child: CustomPaint(
                    painter: WaveChartPainter(
                      data: gymData.weeklyData,
                      drawAnimation: _drawLineController,
                      fillAnimation: _wipeXController,
                      u: _u,
                    ),
                    size: Size(835 * _u, 230 * _u),
                  ),
                ),
                
                SizedBox(height: -31 * _u),
                
                // Days labels
                Padding(
                  padding: EdgeInsets.only(top: 16 * _u),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: List.generate(gymData.weekDays.length, (index) {
                      final isActive = index == gymData.activeDayIndex;
                      return Text(
                        gymData.weekDays[index],
                        style: TextStyle(
                          fontSize: 18 * _u,
                          fontWeight: isActive ? FontWeight.w600 : FontWeight.w500,
                          color: isActive 
                              ? Colors.white 
                              : Colors.white.withOpacity(0.88),
                          fontFamily: 'Vazirmatn',
                        ),
                      );
                    }),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
  
  Widget _buildRightRail(BuildContext context, GymDataState gymData) {
    return Positioned(
      right: 38 * _u,
      top: 134 * _u,
      bottom: 95 * _u,
      width: 310 * _u,
      child: AnimatedBuilder(
        animation: _slideRController,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset((30 * (1 - _slideRController.value)) * _u, 0),
            child: Opacity(
              opacity: _slideRController.value,
              child: child,
            ),
          );
        },
        child: Column(
          children: [
            // Card A - Big card
            Expanded(
              child: GlassPanel(
                borderRadius: 24 * _u,
                child: Padding(
                  padding: EdgeInsets.all(24 * _u),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Icon(
                            Icons.location_on,
                            size: 20 * _u,
                            color: Colors.white.withOpacity(0.8),
                          ),
                          SizedBox(width: 8 * _u),
                          Text(
                            'شعبه مرکزی',
                            style: TextStyle(
                              fontSize: 16 * _u,
                              color: Colors.white.withOpacity(0.9),
                              fontFamily: 'Vazirmatn',
                            ),
                          ),
                        ],
                      ),
                      
                      Spacer(),
                      
                      // Big number
                      Row(
                        baseline: TextBaseline.alphabetic,
                        textBaseline: TextBaseline.alphabetic,
                        children: [
                          Text(
                            gymData.activeMembers.toString(),
                            style: TextStyle(
                              fontSize: 92 * _u,
                              fontWeight: FontWeight.w400,
                              letterSpacing: -2 * _u,
                              color: Colors.white,
                              fontFamily: 'Vazirmatn',
                            ),
                          ),
                          SizedBox(width: 8 * _u),
                          Text(
                            'نفر',
                            style: TextStyle(
                              fontSize: 24 * _u,
                              color: Colors.white.withOpacity(0.7),
                              fontFamily: 'Vazirmatn',
                              fontStyle: FontStyle.italic,
                            ),
                          ),
                        ],
                      ),
                      
                      Spacer(),
                      
                      // Metrics
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _buildMetric(
                            Icons.attach_money,
                            '${gymData.todayRevenue}M',
                            'درآمد امروز',
                          ),
                          _buildMetric(
                            Icons.warning_amber,
                            '${(gymData.debtRatio * 100).toInt()}%',
                            'بدهی‌ها',
                          ),
                          _buildMetric(
                            Icons.people_outline,
                            gymData.classCapacity.toString(),
                            'ظرفیت کلاس‌ها',
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
            
            SizedBox(height: 20 * _u),
            
            // Card B
            _buildBranchCard(gymData.branches[0]),
            
            SizedBox(height: 20 * _u),
            
            // Card C
            _buildBranchCard(gymData.branches[1]),
            
            SizedBox(height: 20 * _u),
            
            // Card D
            _buildBranchCard(gymData.branches[2]),
          ],
        ),
      ),
    );
  }
  
  Widget _buildMetric(IconData icon, String value, String label) {
    return Column(
      children: [
        Icon(
          icon,
          size: 20 * _u,
          color: Colors.white.withOpacity(0.7),
        ),
        SizedBox(height: 4 * _u),
        Text(
          value,
          style: TextStyle(
            fontSize: 18 * _u,
            fontWeight: FontWeight.w600,
            color: Colors.white,
            fontFamily: 'Vazirmatn',
          ),
        ),
        SizedBox(height: 2 * _u),
        Text(
          label,
          style: TextStyle(
            fontSize: 11 * _u,
            color: Colors.white.withOpacity(0.6),
            fontFamily: 'Vazirmatn',
          ),
        ),
      ],
    );
  }
  
  Widget _buildBranchCard(BranchData branch) {
    return GlassPanel(
      borderRadius: 16 * _u,
      height: 120 * _u,
      child: Padding(
        padding: EdgeInsets.all(16 * _u),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    branch.fullPath,
                    style: TextStyle(
                      fontSize: 14 * _u,
                      color: Colors.white.withOpacity(0.9),
                      fontFamily: 'Vazirmatn',
                    ),
                  ),
                  SizedBox(height: 8 * _u),
                  Text(
                    'وضعیت: ${branch.status}',
                    style: TextStyle(
                      fontSize: 12 * _u,
                      color: Colors.white.withOpacity(0.7),
                      fontFamily: 'Vazirmatn',
                    ),
                  ),
                ],
              ),
            ),
            
            Container(
              width: 60 * _u,
              height: 60 * _u,
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.15),
                shape: BoxShape.circle,
              ),
              child: Icon(
                branch.icon,
                size: 30 * _u,
                color: Colors.white,
              ),
            ),
            
            SizedBox(width: 16 * _u),
            
            Text(
              branch.count.toString(),
              style: TextStyle(
                fontSize: 32 * _u,
                fontWeight: FontWeight.w600,
                color: Colors.white,
                fontFamily: 'Vazirmatn',
              ),
            ),
          ],
        ),
      ),
    );
  }
}
