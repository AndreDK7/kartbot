local playerskins = {}
local playercolors = {}
local playerspec = {}

local function checkPlayerChar()
    for i = 0, #players - 1 do
        local player = players[i]
        if player and player.mo then
            if player.mo.skin ~= playerskins[i] or player.skincolor ~= playercolors[i] then
                playerskins[i] = player.mo.skin
                playercolors[i] = player.skincolor

                CONS_Printf(server, "[CHAR] [CHAR_COLOR] "..player.skincolor.." [CHAR_SKIN] "..player.mo.skin.." [NUMBER] "..tostring(i).." [NAME] "..player.name)
            end
        end
    end
end

addHook("ThinkFrame", checkPlayerChar)
addHook("MapLoad", checkPlayerChar)
addHook("PlayerJoin", checkPlayerChar)
