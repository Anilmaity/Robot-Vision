--[[
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code SCOR_LUA
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:            SCOR_LUA.lua
*  Created:             07/10/2020
*  Last Modified:       07/10/2020
*  Author:              e-Yantra Team
*
*****************************************************************************************
]] --

-- getTheTopper function finds the student name who scored max, i.e. Topper's name from the scorelist created by readScoreList function
function getTheTopper(list)
    -- find the max score
    local scorelist = {}
    local namelist = {}
    if 2 <= N and N <= 100 then
        for i = 1, N do
            local a = 1
            list[i] = tostring(io.read())
            for values in string.gmatch(list[i], "[^%s]+") do
                if a == 2 then
                    if 1 <= tonumber(values) and tonumber(values) <= 100 then
                        scorelist[i] = tonumber(values)
                    else
                        print("Score is not in given constrain")
                    end
                else
                    a = a + 1
                    namelist[i] = values
                end
            end
        end
    else
        print("N is not in given constrain")


        local highscore = score_list[1]
        for i = 2, #score_list do
            if score_list[i] >= highscore then
                highscore = score_list[i]
                --print(score_list[i])
            end
        end

    local topper_names = {}
        local j = 1
        for i = 1, #namelist do
            if highscore == score_list[i] then
                topper_names[j] = namelist[i]
                j = j + 1
            end
        end

        for i = 1, #topper_names do
            print(topper_names[i])
        end
    end
end

-- readScoreList function creates the scorelist table from input
function readScoreList(N)
    -- write your code here
    local list = {}
    if 2 <= N and N <= 100 then
        for i = 1, N do
            list[i] = tostring(io.read())
        end
    end
    return list
end

-- for each case, call the readScoreList and getTheTopper functions to get the scores of students and then find the student name who scored max, i.e. Topper's name
tc = tonumber(io.read())

if 1 <= tc and tc <= 25 then
    for i = 1, tc
    do
        local N = tonumber(io.read())
        score_list= readScoreList(N);
        getTheTopper(score_list)
    end
else
    print("tc is greater than given constrain")
end



