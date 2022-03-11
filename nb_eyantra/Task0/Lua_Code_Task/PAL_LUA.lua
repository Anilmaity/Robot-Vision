--[[
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code PAL_LUA
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:			PAL_LUA.lua
*  Created:				10/10/2020
*  Last Modified:		13/10/2020
*  Author:				e-Yantra Team
*
*****************************************************************************************
]] --

-- palindrome function to check whether the input string is a palindrome or not with case insensitive
function palindrome(str)

    if 2 <= #str and #str <= 100 then
        local case = true
        local  strcase = true

        for i = 1, #str do
            local char = string.byte(string.upper(str), i)
            if char >= 48 and char <= 57 or char >= 65 and char <= 90 or char >= 97 and char <= 122 then
            else
                strcase = false
                print("str is not in given constrain")
            end
        end

        for i = 1, #str do
            local char = string.byte(string.upper(str), i)
            local char2 = string.byte(string.reverse(string.upper(str)), i)
            if char == char2 then
                case = true
            else
                case = false
            end
        end

        if strcase and case then
            print("It is a palindrome")
        elseif strcase then
            print("It is not a palindrome")
        else

        end
    else
        print("str length is not in given constrain")
    end
end

-- for each case, call the palindrome function to check whether the input string is a palindrome or not with case insensitive
tc = tonumber(io.read())
if 1 <= tc and tc <= 25 then
    for i = 1, tc
    do
        str = io.read()
        palindrome(str)
    end
else
    print("testcase is not in constrain")
end

