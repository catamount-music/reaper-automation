--[[ 
  Batch apply ReaComp (Compressor) to all selected items.
  Intended to be run in Reaper after importing files.
--]]

-- Select all media items in project
local num_items = reaper.CountMediaItems(0)
for i = 0, num_items-1 do
  local item = reaper.GetMediaItem(0, i)
  local take = reaper.GetMediaItemTake(item, 0)
  if take ~= nil then
    -- Insert FX: ReaComp (Compressor)
    local fx_index = reaper.TakeFX_AddByName(take, "ReaComp (Cockos)", 1)
    -- Optionally set some parameters (default is often fine for demo)
  end
end
reaper.UpdateArrange()
