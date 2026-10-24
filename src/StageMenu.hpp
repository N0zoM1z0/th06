#pragma once
#include "AnmVm.hpp"
#include "decomp.hpp"

namespace th06
{
class StageMenu
{
  public:
    i32 OnUpdateGameMenu();
    i32 OnUpdateRetryMenu();

    void OnDrawGameMenu();
    void OnDrawRetryMenu();

  private:
    // Current state of this menu.
    u32 curState;
    // Number of frames since last state change. Used to delay certain actions
    // until an animation is finished.
    i32 numFrames;
    AnmVm menuSprites[6];
    AnmVm menuBackground;
};
ZUN_ASSERT_TYPE(StageMenu, 0x778, 4);
} // namespace th06
