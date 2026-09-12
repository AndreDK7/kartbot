local playerskins = {}
local playercolors = {}
local playerspec = {}

local function printPlayerChar(player)
	for i = 0, #players-1 do
        	local player = players[i]
		if player and player.mo != nil then
			if player.mo.skin != playerskins[i] then
				playerskins[i] = player.mo.skin
				CONS_Printf(server, "[CHAR] [CHAR_COLOR] " + player.mo.color + " [CHAR_SKIN] "+player.mo.skin+" [NUMBER] " + tostring(i) + " [NAME] "+player.name)
			end
		end
	end
end

addHook("PlayerMsg", printPlayerChar)

addHook("MapLoad", printPlayerChar)

addHook("PlayerJoin", printPlayerChar)
