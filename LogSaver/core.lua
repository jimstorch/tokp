local Verbose = 1;

local options = { 
    type='group',
    args = {
        toggle = {
            type = 'execute',
            name = 'toggle',
            desc = 'Toggle logging for the current zone.',
            usage = "/logsaver toggle",
            func = "ToggleCurrentZone",
        },
        list = {
            type = 'execute',
            name = 'list',
            desc = 'List zones for logging.',
            usage = "/logsaver list",
            func = "ListZones",
        },
        chat = {
            type = 'toggle',
            name = 'chat',
            desc = 'Toggle chat logging.',
            usage = "/logsaver chat",
            get = "IsChat",
            set = "ToggleChat",
        },
        combat = {
            type = 'toggle',
            name = 'combat',
            desc = 'Toggle combat logging.',
            usage = "/logsaver combat",
            get = "IsCombat",
            set = "ToggleCombat",
        },
        range = {
            type = 'range',
            name = 'range',
            desc = "Change the combat/chat log range.",
            usage = "/logsaver range",
            get = "ShowCurrentRange",
            set = "SetCurrentRange",
            min = 0,
            max = 250,
            step = 5,
            isPercent = false,
        },
    },
}

local RANGE_VARS = {
   "CombatDeathLogRange",
   "CombatLogRangeCreature",
   "CombatLogRangeParty",
   "CombatLogRangePartyPet",
   "CombatLogRangeFriendlyPlayers",
   "CombatLogRangeFriendlyPlayersPets",
   "CombatLogRangeHostilePlayers",
   "CombatLogRangeHostilePlayersPets"
}

local OLD_RANGE_VALUES = {}

-- Sets ranges to range or to default if range is nil
local function SetLoggingRange(range)
    for i,var in ipairs(RANGE_VARS) do
        OLD_RANGE_VALUES[i] = GetCVar(var)
        SetCVar(var, range)
    end
end

-- Sets logging ranges to defaults
local function SetDefaultLoggingRange()
    for i,var in ipairs(RANGE_VARS) do
        -- SetCVar(var, GetCVarDefault(var))
        SetCVar(var, OLD_RANGE_VALUES[i])
    end
end

LogSaver = AceLibrary("AceAddon-2.0"):new("AceConsole-2.0", "AceEvent-2.0", "AceDB-2.0")
LogSaver:RegisterChatCommand("/logsaver", options)

LogSaver:RegisterDB("LogSaverDB", "LogSaverDBPC")
LogSaver:RegisterDefaults("profile", {
    LogChatFile = false,
    LogCombatFile = false,
    LogRange = 150,
    Zones = {},
} )

function LogSaver:OnInitialize()
    -- Called when the addon is loaded
end

function LogSaver:OnEnable()
    -- Called when the addon is enabled
    self:RegisterEvent("ZONE_CHANGED_NEW_AREA")
    SetLoggingRange(self.db.profile.LogRange)
    self:Reconfigure()
end

function LogSaver:OnDisable()
    -- Called when the addon is disabled
    -- SetDefaultLoggingRange()
end

function LogSaver:ZONE_CHANGED_NEW_AREA()
    if (Verbose >= 2) then
        self:Print("You have changed zones!")
    end
    self:Reconfigure()
end

function LogSaver:IsChat()
    return self.db.profile.LogChatFile
end

function LogSaver:ToggleChat()
    self.db.profile.LogChatFile = not self.db.profile.LogChatFile
    self:Reconfigure()
end

function LogSaver:IsCombat()
    return self.db.profile.LogCombatFile
end

function LogSaver:ToggleCombat()
    self.db.profile.LogCombatFile = not self.db.profile.LogCombatFile
    self:Reconfigure()
end

function LogSaver:LogCurrentZone()
    return self.db.profile.Zones[self.current_zone] and true or false
end

function LogSaver:ToggleCurrentZone()
    self.current_zone = GetRealZoneText()
    if self.db.profile.Zones[self.current_zone] then
        self.db.profile.Zones[self.current_zone] = nil
        if (Verbose >= 1) then
            self:Print("Logging off for " .. self.current_zone)
        end
    else
        self.db.profile.Zones[self.current_zone] = true
        if (Verbose >= 1) then
            self:Print("Logging on for " .. self.current_zone)
        end
    end
    self:Reconfigure()
end

function LogSaver:ShowCurrentRange()
    return self.db.profile.LogRange
end

function LogSaver:SetCurrentRange(new_range)
    self.db.profile.LogRange = new_range
    SetLoggingRange(self.db.profile.LogRange)
end

function LogSaver:ListZones()
    if next(self.db.profile.Zones) then
        self:Print("Logging on in zones:")
        for z,s in pairs(self.db.profile.Zones) do
            self:Print("* " .. z)
        end
    else
        self:Print("Logging is off for all zones.")
    end
end

function LogSaver:Reconfigure()
    if (Verbose >= 2) then
        self:Print("Reconfiguring...")
    end
    self.current_zone = GetRealZoneText()
    if (self:LogCurrentZone()) then
        if (self.db.profile.LogChatFile and not LoggingChat()) then
            -- UIErrorsFrame:AddMessage("ChatLog ON", 0.2, 1.0, 0.2, 1.0, UIERRORS_HOLD_TIME)
            if (Verbose >= 1) then
                self:Print("ChatLog ON")
            end
            assert(not LoggingChat())
            LoggingChat(true)   
        end
        if (self.db.profile.LogCombatFile and not LoggingCombat()) then
            -- UIErrorsFrame:AddMessage("CombatLog ON", 0.2, 1.0, 0.2, 1.0, UIERRORS_HOLD_TIME)
            if (Verbose >= 1) then
                self:Print("CombatLog ON")
            end
            assert(not LoggingCombat())
            LoggingCombat(true)
        end
    else
        if (self.db.profile.LogChatFile and LoggingChat()) then
            -- UIErrorsFrame:AddMessage("ChatLog OFF", 1.0, 0.0, 0.0, 1.0, UIERRORS_HOLD_TIME)
            if (Verbose >= 1) then
                self:Print("ChatLog OFF")
            end
            assert(LoggingChat())
            LoggingChat(false)
        end
        if (self.db.profile.LogCombatFile and LoggingCombat()) then
            -- UIErrorsFrame:AddMessage("CombatLog OFF", 1.0, 0.0, 0.0, 1.0, UIERRORS_HOLD_TIME)
            if (Verbose >= 1) then
                self:Print("CombatLog OFF")
            end
            assert(LoggingCombat())
            LoggingCombat(false)
        end   
    end
end