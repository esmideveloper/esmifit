import 'package:flutter_riverpod/flutter_riverpod.dart';

enum UserRole {
  admin,      // مدیر
  reception,  // پذیرش
  trainer,    // مربی
  accountant, // حسابدار
}

class User {
  final String id;
  final String name;
  final String username;
  final UserRole role;
  final String? avatarPath;
  
  const User({
    required this.id,
    required this.name,
    required this.username,
    required this.role,
    this.avatarPath,
  });
  
  String get roleLabel {
    switch (role) {
      case UserRole.admin: return 'مدیر';
      case UserRole.reception: return 'پذیرش';
      case UserRole.trainer: return 'مربی';
      case UserRole.accountant: return 'حسابدار';
    }
  }
}

class UserState {
  final User? currentUser;
  final bool isAuthenticated;
  final List<User> allUsers;
  
  const UserState({
    this.currentUser,
    this.isAuthenticated = false,
    this.allUsers = const [],
  });
  
  UserState copyWith({
    User? currentUser,
    bool? isAuthenticated,
    List<User>? allUsers,
  }) {
    return UserState(
      currentUser: currentUser ?? this.currentUser,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      allUsers: allUsers ?? this.allUsers,
    );
  }
}

final userProvider = StateNotifierProvider<UserNotifier, UserState>((ref) {
  return UserNotifier();
});

class UserNotifier extends StateNotifier<UserState> {
  UserNotifier() : super(const UserState());
  
  void login(String username, String password) {
    // Mock login - replace with actual auth logic
    final user = User(
      id: '1',
      name: 'مدیر باشگاه تکاور',
      username: username,
      role: UserRole.admin,
    );
    state = state.copyWith(
      currentUser: user,
      isAuthenticated: true,
    );
  }
  
  void logout() {
    state = const UserState();
  }
  
  void updateCurrentUser(User user) {
    state = state.copyWith(currentUser: user);
  }
}
