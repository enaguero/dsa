-- strip-advanced.lua
-- Pandoc Lua filter for the two-track build of notes/ram_model.md.
--
-- When applied (via `pandoc --lua-filter=templates/strip-advanced.lua`), this
-- filter removes every fenced Div whose class list contains `advanced`,
-- producing the "essentials" subset of the document. Without the filter,
-- the same source compiles unchanged into the full reference.
--
-- Tag deep material in the markdown like this:
--
--     ::: {.advanced}
--     ## Some advanced section
--     ... content that should NOT appear in the essentials build ...
--     :::
--
-- Divs without the `advanced` class are left alone, so essentials-only
-- content needs no annotation — the default is "included in both builds".

function Div(el)
  if el.classes:includes("advanced") then
    return {}        -- drop the div and everything inside it
  end
  return nil          -- otherwise keep
end
