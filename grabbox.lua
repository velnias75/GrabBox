--[[
 Copyright 2019 by Heiko Schäfer <heiko@rangun.de>

 This file is part of GrabBox.

 GrabBox is free software: you can redistribute it and/or modify
 it under the terms of the GNU Lesser General Public License as
 published by the Free Software Foundation, either version 3 of
 the License, or (at your option) any later version.

 GrabBox is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Lesser General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License
 along with GrabBox.  If not, see <http://www.gnu.org/licenses/>.
--]]

function probe()

    if vlc.access ~= "http" and vlc.access ~= "https" then
        return false
    end

    return string.match(vlc.path, "^grabbox@.*srf.ch.*") ~= nil or
            string.match(vlc.path, "^grabbox@.*servus.com.*") ~= nil or
            string.match(vlc.path, "^grabbox@.*arte.tv.*") ~= nil or
            string.match(vlc.path, "^grabbox@.*tele5.de.*") ~= nil
end

function parse()

    local title = string.match(vlc.path, "grabbox@(.*)")
    local source = guessSource()
    local url = nil
    local item = {}
    local cmd = "/home/heiko/.local/bin/grabbox url \""..source..":"..vlc.access.."://"..title.."\""

    if source ~= nil then
        vlc.msg.info("Executing command: "..cmd)

        local f = assert(io.popen("grabbox url \""..source..":"..vlc.access.."://"..title.."\" \"vlc\" \"\""))

        for line in f:lines() do
            url = line
        end -- for loop

        f:close()

        item.path = fixSRFUrl(url)
        item.name = "GrabBox@"..string.upper(source)..": "..vlc.access.."://"..title
    else
        item.name = "GrabBox: unsupported url"
    end

    return { item }
end

function guessSource()

    if string.match(vlc.path, ".*(srf.ch).*") then
        return "srf"
    elseif string.match(vlc.path, ".*(servus.com).*") then
        return "servus"
    elseif string.match(vlc.path, ".*(arte.tv).*") then
        return "arte"
    elseif string.match(vlc.path, ".*(tele5.de).*") then
        return "tele5"
    end

    return nil
end

function fixSRFUrl(url)

    local base = string.match(url, "(http.?://srf.*csmil).*")

    if base == nil then
        return url
    end

    return base.."/index_5_av.m3u8"
end
