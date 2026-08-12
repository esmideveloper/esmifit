#ifndef RUNNER_WIN32_WINDOW_H_
#define RUNNER_WIN32_WINDOW_H_

#include <windows.h>

#include <functional>
#include <memory>
#include <string>

// A class abstraction for a high DPI-aware Win32 Window.
class Win32Window {
 public:
  // Point and size commonly used for window positioning.
  struct Point {
    Point(int x, int y) : x(x), y(y) {}
    int x;
    int y;
  };

  struct Size {
    Size(int w, int h) : w(w), h(h) {}
    int w;
    int h;
  };

  Win32Window();
  virtual ~Win32Window();

  // Creates a win32 window with the given title, origin and size.
  bool Create(const std::wstring& title, const Point& origin, const Size& size);

  // Shows the current window.
  void Show();

  // Hides the current window.
  void Hide();

  // Focuses the current window.
  void Focus();

  // Sets the icon for the window.
  void SetIcon(HICON icon);

  // Returns true if the window is currently showing.
  bool IsShowing() const;

  // Protects the members of this class from being accessed concurrently.
  void EnableThreadSafeMemberFunctions(bool enable);

 protected:
  // Registers a window class upon object creation.
  static wchar_t window_class_;

  // The Windows message loop.
  static LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wparam,
                                  LPARAM lparam);

  // Processes and route salient window messages for mouse handling,
  // size change and DPI. Delegates handling of these to member overloads that
  // inheriting classes can handle.
  virtual LRESULT MessageHandler(HWND hwnd, UINT msg, WPARAM wparam,
                                 LPARAM lparam);

  // Called when Create has successfully created a window.
  virtual void OnCreate();

  // Called when the window is destroyed.
  virtual void OnDestroy();

  // Called when the window's size has changed.
  virtual void OnSize(int width, int height);

  // Retrieve the HWND for the current window.
  HWND GetHandle() const { return hwnd_; }

  // Set the child content.
  void SetChildContent(HWND child_content) { child_content_ = child_content; }

 private:
  // Attributes for the window class registration.
  static constexpr const wchar_t* kClassName = L"FlutterApp";

  // The HWND for the window.
  HWND hwnd_ = nullptr;

  // The content for the window.
  HWND child_content_ = nullptr;
  
  // True if the window is currently showing.
  bool showing_ = false;
};

#endif  // RUNNER_WIN32_WINDOW_H_
