AP = {
    LocationMapping = {},
    ItemMapping = {}
}

function AP.CheckLocations()
    local playerSection = Game.GetPlayerBlackboardSectionName()
    local locations = ""
    for id, data in pairs(AP.LocationMapping) do
        local propName = RandomizerPowerup.PropertyForLocation(string.format("%s_%s", data[1], data[2]))
        if Blackboard.GetProp(playerSection, propName) then
            locations = locations .. "," .. tostring(id)
        end
    end
    return string.sub(locations, 2)
end

function AP.GetInventory()
    local items = ""
    for id, item in pairs(AP.ItemMapping) do
        if item == "ITEM_MISSILE_TANKS" and RandomizerPowerup.GetItemAmount("ITEM_WEAPON_MISSILE_LAUNCHER") > 0 then
            item = "ITEM_WEAPON_MISSILE_MAX"
        elseif item == "ITEM_SUPER_MISSILE_TANKS" and RandomizerPowerup.GetItemAmount("ITEM_WEAPON_SUPER_MISSILE") > 0 then
            item = "ITEM_WEAPON_SUPER_MISSILE_MAX"
        elseif item == "ITEM_POWER_BOMB_TANKS" and RandomizerPowerup.GetItemAmount("ITEM_WEAPON_POWER_BOMB") > 0 then
            item = "ITEM_WEAPON_POWER_BOMB_MAX"
        elseif item == "ITEM_ENERGY_TANKS" then
            item = "ITEM_MAX_LIFE"
        end
        items = string.format("%s,%d=%s", items, id, RandomizerPowerup.GetItemAmount(item))
    end
    return string.sub(items, 2)
end
