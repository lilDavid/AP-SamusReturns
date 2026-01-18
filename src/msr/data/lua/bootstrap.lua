AP = {
    LocationMapping = {}
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
