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
function getTheTopper(score_list)
    -- find the max score
    local scorelist = {}
    local namelist = {}

    for i = 1, #score_list do
        local a = 1
        for values in string.gmatch(score_list[i], "[^%s]+") do
            if a == 2 then
                    scorelist[i] = tonumber(values)
            else
                a = a + 1
                namelist[i] = values
            end
        end
    end

    local highscore = scorelist[1]
    for i = 2, #scorelist do
        if scorelist[i] >= highscore then
            highscore = scorelist[i]
            --  print(scorelist[i])
        end
    end

    -- write your code here

    local topper_names = {}
    local j = 1
    for i = 1, #namelist do
        if highscore == scorelist[i] then
            topper_names[j] = namelist[i]
            j = j + 1
        end
    end

    for i = 1, #topper_names do
        print(topper_names[i])
    end
end

-- readScoreList function creates the scorelist table from input
function readScoreList(N)
    local scorelist = {}
    -- write your code here
    if 2 <= N and N <= 100 then
        for i = 1, N do
            scorelist[i] = tostring(io.read())
            local a = 1
            for values in string.gmatch(scorelist[i], "[^%s]+") do
                if a == 2 then
                    if 0 <= tonumber(values) and tonumber(values) <= 100 then
                    else
                        print("Score is not in given constrain")
                        os.exit()
                    end
                else
                    a = a+1
                end
            end
        end
    else
        print("N is not in given constrain")
        os.exit()
    end
    return scorelist
end


-- for each case, call the readScoreList and getTheTopper functions to get the scores of students and then find the student name who scored max, i.e. Topper's name
tc = tonumber(io.read())
if 1 <= tc and tc <= 25 then
    for i = 1, tc
    do
        local N = tonumber(io.read())
        score_list = readScoreList(N);
        getTheTopper(score_list)
    end
end

--[[
8
7
Sam 40.08
Riya 30.7
Harry 41
Anne 35.2
Peter 36
Harry 41
peter 42
5
Sam 40.08
Riya 30.7
Harry 41
Anne 35.2
Peter 36.6
5
Sam 100
Riya 0
Harry 41
Anne 35.2
Peter 36.6
1
Sam 40.08
7
Sam 40.08
Riya 30.7
Harry 41
Anne 35.2
Peter 36
Harry 41
peter 42
5
Sam 40.08
Riya 30.7
Harry 41
Anne 35.2
Peter 36.6
5
Sam 100
Riya 0
Harry 41
Anne 35.2
Peter 36.6
1
Sam 40.08
]]--