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
end
