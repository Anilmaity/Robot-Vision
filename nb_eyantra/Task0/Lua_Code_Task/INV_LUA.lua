--[[
*****************************************************************************************
*
*
*  This script is code stub for CodeChef problem code INV_LUA
*  under contest PYLT20TS in Task 0 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*
*  Filename:            INV_LUA.lua
*  Created:             07/10/2020
*  Last Modified:       07/10/2020
*  Author:              e-Yantra Team
*
*****************************************************************************************
]] --

-- manageInventory function to add, update / delete items to / from the Inventory
function manageInventory()
    -- reading total Items N
    N = tonumber(io.read())
    local invnamelist = {}
    local invitemlist = {}
    local invlist = {}
    if 1 <= N and N <= 100 then
        for L = 1, N do
            invlist[L] = tostring(io.read())

            local str = invlist[L]
            local num = ''
            for i = string.find(str, " "), #str - 1 do
                num = num .. string.char(string.byte(str, i + 1))
            end
            num = tonumber(num)

            if 1 <= num and num <= 100 then
                invitemlist[L] = num
            else

                os.exit()
                print("quantity overload")
            end

            local name = ''
            for j = 1, string.find(str, " ") - 1 do
                name = name .. string.char(string.byte(str, j))
            end
            invnamelist[L] = name
        end
    end


    -- write your code here




    -- reading total M operations to perform

    M = tonumber(io.read())
    if 1 <= M and M <= 100 then
        for i = 1, M do
            operation = tostring(io.read())
            local a = 1
            local ad = false
            local del = false
            local itemindex = 0
            local itemname = ''
            for values in string.gmatch(operation, "[^%s]+") do
                if a == 1 then
                    if values == "ADD" then
                        ad = true
                    elseif values == "DELETE" then
                        del = true
                    else
                        print("invalid cmd")

                        break
                    end
                elseif a == 2 then
                    for i = 1, #invnamelist do
                        if values == invnamelist[i] then
                            itemindex = i
                            itemname = values
                            break
                        else
                            itemindex = i + 1
                            itemname = values
                        end
                    end
                elseif a == 3 then
                    if #invnamelist <= itemindex then

                        if ad then
                            invitemlist[itemindex] = tonumber(values)
                        invnamelist[itemindex] = itemname
                            print("ADDED Item "..itemname)
                        elseif del then
                            print("Item " .. itemname .. " could not be DELETED")
                        end
                    else
                        if ad then
                            invitemlist[itemindex] = invitemlist[itemindex] + tonumber(values)
                              print("ADDED Item " .. itemname)
                        elseif del then
                            if invitemlist[itemindex] >= tonumber(values) then
                                invitemlist[itemindex] = invitemlist[itemindex] - tonumber(values)
                                print("DELETED Item "..itemname)
                            else
                                print("Item " .. itemname .. " could not be DELETED")
                            end
                        end

                    end
                end
                a = a + 1
            end 
        end
    else
        print("Cant do this much operation")
    end
    -- write your code here

    -- calculate the sum of items
    local sum = 0
for i=1,#invnamelist do
   -- print(invitemlist[i])
    sum = invitemlist[i] + sum
end
print(sum)

    -- write your code here
end

-- for each case, call the manageInventory function to add, update / delete items to / from the Inventory
tc = tonumber(io.read())
if 1 <= tc and tc <= 25 then
    i = 0
    while i < tc do
        manageInventory()
        i = i + 1
    end
end
