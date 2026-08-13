local cv_printresults = CV_RegisterVar({
    name = "printresults",
    defaultvalue = "On",
    possiblevalue = CV_OnOff,
    flags = CV_NETVAR,
})

local printresults = false

addHook("IntermissionThinker", do
    if printresults then
        local str = ";"
        for i = 1, #players - 1 do
            local player = players[i]
            if player != nil then
                str = str + tostring(i) + ":" + player.name + ":" + tostring(player.kartstuff[k_position]) + ":" + tostring(player.realtime) + ":" + tostring(player.lives == 0) + ":" + tostring(player.mo == nil) + ";"
            end
        end
        CONS_Printf(server, "[RESULTS] " + str)
        printresults = false
    end
end)

addHook("MapLoad", do
    printresults = cv_printresults.value
end)
