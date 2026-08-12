set(CMAKE_CXX_STANDARD 17)

# Configure the C++ compiler to use static runtime linking.
set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

add_executable(${BINARY_NAME} WIN32
  "flutter_window.cpp"
  "main.cpp"
  "utils.cpp"
  "win32_window.cpp"
  "${FLUTTER_MANAGED_DIR}/generated_plugin_registrant.cc"
  "Runner.rc"
  "runner.exe.manifest"
)

# Apply the standard set of build settings.
apply_standard_settings(${BINARY_NAME})

# Add preprocessor definitions for the application ID.
target_compile_definitions(${BINARY_NAME} PRIVATE "NOMINMAX")

# Add dependency libraries.
target_link_libraries(${BINARY_NAME} PRIVATE
  flutter
  flutter_wrapper_app
  dwmapi
  ole32
  shell32
  user32
  uuid
)

include_directories("${CMAKE_SOURCE_DIR}")
