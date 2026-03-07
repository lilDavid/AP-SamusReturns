RL.LocationMapping = {}
function RL.GetCollectedIndicesAndSend()
    local playerSection = Game.GetPlayerBlackboardSectionName()
    local locations = {}
    for id, propName in pairs(RL.LocationMapping) do
        if Blackboard.GetProp(playerSection, propName) then
            table.insert(locations, tostring(id))
        end
    end
    RL.SendIndices(table.concat(locations, ","))
end

RL.Items = {}
function RL.GetInventoryAndSend()
    local items = {}
    for _, item in ipairs(RL.Items) do
        table.insert(items, string.format("%s=%s", item, RandomizerPowerup.GetItemAmount(item)))
    end
    RL.SendInventory(table.concat(items, ","))
end

function RL.ReceivedPickups()
    local playerSection = Game.GetPlayerBlackboardSectionName()
    return Blackboard.GetProp(playerSection, "ReceivedPickups") or 0
end

function RL.GetReceivedPickupsAndSend(reset)
    if reset then
        RL.PendingPickup = nil
    end
    RL.SendReceivedPickups(tostring(RL.ReceivedPickups()))
end

function RL.ReceivePickup(msg, code, index)
    if RL.PendingPickup then
        return
    end
    if index ~= RL.ReceivedPickups() then
        Game.AddSF(0, "RL.GetInventoryAndSend", "")
        Game.AddSF(0.05, "RL.GetReceivedPickupsAndSend", "")
        return
    end

    RL.PendingPickup = {msg = msg, code = assert(loadstring(code))}
    Game.AddSF(0, RL.GivePendingPickup, "")
end

function RL.GivePendingPickup()
    if not Scenario.IsUserInteractionEnabled(true) then
        Game.AddSF(0.5, RL.GivePendingPickup, "")
        return
    end

    Scenario.QueueAsyncPopup(RL.PendingPickup.msg, 5.0)
    Game.AddSF(5.5, RL.GetReceivedPickupsAndSend, "b", true)
    RL.PendingPickup.code()
    Scenario.WriteToPlayerBlackboard("ReceivedPickups", "f", RL.ReceivedPickups() + 1)
end

function RL.SendRandoIdentifier()
    RL.SendNewGameState(string.format("rando_id:%s", Init.sThisRandoIdentifier))
end

function RL.GetGameStateAndSend()
    local game_mode = Game.GetCurrentGameModeID()
    local scenario
    if game_mode == "INGAME" then
        scenario = Game.GetScenarioID()
    else
        scenario = game_mode
    end
    RL.SendNewGameState(string.format("scenario:%s", scenario))
end

function RL.UpdateRDVClient(new_scenario)
    RL.GetGameStateAndSend()
    if Game.GetCurrentGameModeID() == "INGAME" then
        local playerSection = Game.GetPlayerBlackboardSectionName()
        local currentSaveRandoIdentifier = Blackboard.GetProp(playerSection, "THIS_RANDO_IDENTIFIER")
        if currentSaveRandoIdentifier ~= Init.sThisRandoIdentifier then
            return
        end

        Game.AddSF(0, RL.GetInventoryAndSend, "")
        Game.AddSF(0.05, RL.GetCollectedIndicesAndSend, "")
        if new_scenario then
            RL.PendingPickup = nil
        end
        if RL.PendingPickup == nil then
            Game.AddSF(0.05, RL.GetReceivedPickupsAndSend, "b", false)
        end
    end
end
