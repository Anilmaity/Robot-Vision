--[[
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code WLEN_LUA
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:			WLEN_LUA.lua
*  Created:				07/10/2020
*  Last Modified:		07/10/2020
*  Author:				e-Yantra Team
*
*****************************************************************************************
]] --

-- countChar function to count the characters in each word of given string
function countChar(str)
    -- write your code here
    local count = {}
    i = 1
    for word in string.gmatch(str, "[^%s]+") do
        count[i] = #word
        i = i + 1
        if string.find(word, "@") ~= nil then
            print("")
            io.write(#word - 1)


        else
            io.write(",", #word)
        end
    end
end


-- for each case, call countChar function to count the characters in each word of given string
tc = 0
tc = tonumber(io.read())

if 1 <= tc and tc <= 25 then
    for i = 1, tc
    do
        str = tostring(io.read());
        case = true
        for i = 1, #str do
            n = string.byte(str, i)
            if (64 <= n and n <= 90) or (97 <= n and n <= 122) or n == 32 then
            else
                case = false
            end
        end
        if case then
            countChar(str)
        else
             print("input are not all Alpabet")
        end
    end
else
    print(")")
end
