import 'package:flutter_riverpod/flutter_riverpod.dart';

// Gym Data Models
class KpiData {
  final int value;
  final String label;
  final IconData icon;
  
  const KpiData({
    required this.value,
    required this.label,
    required this.icon,
  });
}

class BranchData {
  final String city;
  final String area;
  final String status;
  final int count;
  final IconData icon;
  
  const BranchData({
    required this.city,
    required this.area,
    required this.status,
    required this.count,
    required this.icon,
  });
  
  String get fullPath => '$city / $area / وضعیت: $status';
}

class GymDataState {
  // Forecast strip KPIs
  final List<KpiData> todayKpis;
  
  // Right rail data
  final int activeMembers;
  final int todayRevenue; // in millions
  final double debtRatio;
  final int classCapacity;
  final List<BranchData> branches;
  
  // Chart data points (for wave chart)
  final List<double> weeklyData;
  final List<String> weekDays;
  final int activeDayIndex;
  
  const GymDataState({
    required this.todayKpis,
    required this.activeMembers,
    required this.todayRevenue,
    required this.debtRatio,
    required this.classCapacity,
    required this.branches,
    required this.weeklyData,
    required this.weekDays,
    required this.activeDayIndex,
  });
  
  static const defaultData = GymDataState(
    todayKpis: [
      KpiData(value: 24, label: 'ورود امروز', icon: Icons.accessibility),
      KpiData(value: 13, label: 'تمدید', icon: Icons.refresh),
      KpiData(value: 14, label: 'ثبت‌نام جدید', icon: Icons.person_add),
      KpiData(value: 10, label: 'جلسه PT', icon: Icons.fitness_center),
      KpiData(value: 19, label: 'کلاس گروهی', icon: Icons.groups),
      KpiData(value: 12, label: 'فاکتور', icon: Icons.receipt),
    ],
    activeMembers: 10,
    todayRevenue: 19,
    debtRatio: 0.40,
    classCapacity: 15,
    branches: [
      BranchData(
        city: 'ایران',
        area: 'تهران',
        status: 'شلوغ',
        count: 12,
        icon: Icons.trending_up,
      ),
      BranchData(
        city: 'ایران',
        area: 'کرج',
        status: 'معمولی',
        count: 10,
        icon: Icons.trending_flat,
      ),
      BranchData(
        city: 'ایران',
        area: 'شهریار',
        status: 'خلوت',
        count: 14,
        icon: Icons.trending_down,
      ),
    ],
    weeklyData: [65, 78, 52, 89, 73, 95, 82],
    weekDays: ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه'],
    activeDayIndex: 4, // چهارشنبه
  );
  
  GymDataState copyWith({
    List<KpiData>? todayKpis,
    int? activeMembers,
    int? todayRevenue,
    double? debtRatio,
    int? classCapacity,
    List<BranchData>? branches,
    List<double>? weeklyData,
    List<String>? weekDays,
    int? activeDayIndex,
  }) {
    return GymDataState(
      todayKpis: todayKpis ?? this.todayKpis,
      activeMembers: activeMembers ?? this.activeMembers,
      todayRevenue: todayRevenue ?? this.todayRevenue,
      debtRatio: debtRatio ?? this.debtRatio,
      classCapacity: classCapacity ?? this.classCapacity,
      branches: branches ?? this.branches,
      weeklyData: weeklyData ?? this.weeklyData,
      weekDays: weekDays ?? this.weekDays,
      activeDayIndex: activeDayIndex ?? this.activeDayIndex,
    );
  }
}

final gymDataProvider = StateNotifierProvider<GymDataNotifier, GymDataState>((ref) {
  return GymDataNotifier();
});

class GymDataNotifier extends StateNotifier<GymDataState> {
  GymDataNotifier() : super(GymDataState.defaultData);
  
  void updateKpis(List<KpiData> kpis) {
    state = state.copyWith(todayKpis: kpis);
  }
  
  void updateActiveMembers(int count) {
    state = state.copyWith(activeMembers: count);
  }
  
  void updateRevenue(int amount) {
    state = state.copyWith(todayRevenue: amount);
  }
  
  void updateDebtRatio(double ratio) {
    state = state.copyWith(debtRatio: ratio);
  }
  
  void updateClassCapacity(int capacity) {
    state = state.copyWith(classCapacity: capacity);
  }
  
  void updateBranches(List<BranchData> branches) {
    state = state.copyWith(branches: branches);
  }
  
  void updateWeeklyData(List<double> data) {
    state = state.copyWith(weeklyData: data);
  }
  
  void setActiveDayIndex(int index) {
    state = state.copyWith(activeDayIndex: index);
  }
}
