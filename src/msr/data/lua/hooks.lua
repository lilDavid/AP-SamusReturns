RL.Hooks = RL.Hooks or {}

function RL.SendPlayerDeath()
    RL.SendNewGameState("player_death:")
end

RL.Hooks.OnPlayerDead = RL.Hooks.OnPlayerDead or guicallbacks.OnPlayerDead
function guicallbacks.OnPlayerDead(_ARG_0_)
    RL.Hooks.OnPlayerDead(_ARG_0_)
    RL.SendPlayerDeath()
end

function RL.SendHint(scenario, sealName)
    RL.SendNewGameState(string.format("hint:%s,%s", scenario, sealName))
end

function RL.AddReloadableHooks()
    RL.Hooks.ChozoSealDialog = RL.Hooks.ChozoSealDialog or ChozoSeal.ShowDialogChoice
    function ChozoSeal.ShowDialogChoice(_ARG_0_, _ARG_1_)
        RL.Hooks.ChozoSealDialog(_ARG_0_, _ARG_1_)
        if _ARG_0_ == nil then
            return
        end
        local sealName = _ARG_0_.sName
        local scenario = Scenario.CurrentScenarioID
        if sealName == nil or scenario == nil then
            return
        end
        RL.SendHint(scenario, sealName)
    end
end

RL.Hooks.ScenarioInit = RL.Hooks.ScenarioInit or Scenario.InitScenario
function Scenario.InitScenario(_ARG_0_, _ARG_1_, _ARG_2_, _ARG_3_)
    RL.Hooks.ScenarioInit(_ARG_0_, _ARG_1_, _ARG_2_, _ARG_3_)
    RL.AddReloadableHooks()
end

RL.AddReloadableHooks()
