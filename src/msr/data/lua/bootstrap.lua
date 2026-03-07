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
        Game.AddSF(0, RL.GetInventoryAndSend, "")
        Game.AddSF(0.05, RL.GetCollectedIndicesAndSend, "")
    end
end
