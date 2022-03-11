--[[score_list = { 1, 2, 3, 4, 65, 7, 498, 4, 498, 48, 41, 65 ,498}
namelist = { 'a', 'b', 'c', 'd', 'p', 'o', 'e', 'f', 'g', 'h', 'j', 'k','u'}


topper_names={}
highscore = score_list[1]
for i = 2, #score_list do
    if score_list[i] >= highscore then
        highscore = score_list[i]
        print(score_list[i])
    end
end
j = 1
for i = 1, #namelist do
    if highscore == score_list[i] then
        topper_names[j] = namelist[i]
        j = j + 1

    end
end

for i=1 , #topper_names do
    print(topper_names[i])
end

str = 'wieowppwoeiw'
for i=1 , #str do
io.write(string.byte(string.upper(string.reverse(str)), i))
end
str = 'wieowppwoeiw'
print('')
for i=1 , #str do
io.write(string.byte(string.upper(str), i))
end
case = true
for i = 1, #str do
            local char = string.byte(string.upper(str), i)
            local char2 = string.byte(string.reverse(string.upper(str)), i)
            if char == char2 then

            else
                case = false
            end
        end

        if  case then
            print("It is a palindrome")
        else
            print("It is not a palindrome")
        end
]]--

--[[
str= 'aasd 132'
print(string.find(str , " "))
print(string.char(string.byte(str,6)))

local num = ''
for i = string.find(str ," ") , #str-1 do
num = num..string.char(string.byte(str,i+1))
end
num= tonumber(num)

local name = ''
for i = 1 , string.find(str ," ")-1 do
name = name..string.char(string.byte(str,i))
end

print(num)
print(name)

if str == 'aasd 132' then
    print('good')
end

]]--

cellvalue = 7
    cellBinaryValue = ''
    if cellvalue <= 15 then
        for i = 1 , 4 do
        if cellvalue / (2^(4-i)) >= 1 then
            cellvalue = cellvalue - 2^(4-i)
            cellBinaryValue = cellBinaryValue..'1'
        else
            cellBinaryValue = cellBinaryValue..'0'
        end

        end
        print(cellBinaryValue)


    end