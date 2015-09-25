label pyt_city:
    
    # Music related:
    if not "pytfall" in ilists.world_music:
        $ ilists.world_music["pytfall"] = [track for track in os.listdir(content_path("sfx/music/world")) if track.startswith("pytfall")]
    if not global_flags.has_flag("keep_playing_music"):
        play world choice(ilists.world_music["pytfall"])
    $ global_flags.del_flag("keep_playing_music")
    
    # TS Dropdown var:
    # $ pytfall.city_dropdown = False
    
    scene bg humans
    show screen pyt_city_screen
    with dissolve
    
    python:
        while 1:
            result = ui.interact()
            if result[0] == 'control':
                if result[1] == 'return':
                    break
            elif result[0] == 'location':
                renpy.hide_screen("pyt_city_screen")
                jump(result[1])
                
    $ global_flags.set_flag("keep_playing_music")            
    hide screen pyt_city_screen
    jump mainscreen


screen pyt_city_screen():
    
    default tt = Tooltip(None)
    default loc_list = ["main_street", "arena_outside", "slave_market", "city_jail", "tavern_town",
                                "city_parkgates", "academy_town", "mages_tower",
                                "graveyard_town", "city_beach", "forest_entrance", "hiddenvillage_entrance"]
    add "content/gfx/images/m_1.png" align (1.0, 0.0)
    
    for key in pytfall.maps("pytfall"):
        if not key.get("hidden", False):
            # if "img" in key:
                # $ rx = int(key["rx"]) if "rx" in key else 25
                # $ ry = int(key["ry"]) if "ry" in key else 25
                # $ img = ProportionalScale(key["img"], rx, ry)
                # imagebutton:
                    # pos (key["x"], key["y"])
                    # idle img
                    # hover im.MatrixColor(img, im.matrix.brightness(0.25))
                    # focus_mask True
                    # hovered tt.action(key['name'])
                    # action Return(['location', key["id"]])
            # else: # Map-cut-style:
            imagebutton:
                idle "".join([pytfall.map_pattern, key["id"], ".png"])
                hover "".join([pytfall.map_pattern, key["id"], "_hover.png"])
                focus_mask True
                hovered tt.action(key['name'])
                action Return(['location', key["id"]])
                    
    add "content/gfx/frame/h2.png"
    if tt.value:
        fixed:
            xysize (164, 78)
            pos (1111, 321)
            text (u"[tt.value]") style "TisaOTMolxm" size 24 align (0.5, 0.5)
            
    # Right frame
    
    ### ----> Top buttons <---- ###
    hbox:
        pos (979, 4)
        spacing 4
        imagebutton:
            idle im.Scale("content/gfx/interface/buttons/journal1.png", 36, 40)
            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/journal1.png", 36, 40), im.matrix.brightness(0.15))
            hovered tt.Action("Quest Journal!")
            action ShowMenu("pyt_quest_log")
        imagebutton:
            idle im.Scale("content/gfx/interface/buttons/MS.png", 38, 37)
            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/MS.png", 38, 37), im.matrix.brightness(0.15))
            action (Hide(renpy.current_screen().tag), Function(global_flags.del_flag, "keep_playing_music"),  Jump("mainscreen"))
            hovered tt.Action("Return to Main Screen!")
        imagebutton:
            idle im.Scale("content/gfx/interface/buttons/profile.png", 35, 40)
            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/profile.png", 35, 40), im.matrix.brightness(0.15))
            action [SetField(pytfall.hp, "came_from", last_label), Hide(renpy.current_screen().tag), Jump("hero_profile")]
            hovered tt.Action("View Hero Profile!")
        imagebutton:
            idle im.Scale("content/gfx/interface/buttons/save.png", 40, 40)
            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/save.png", 40, 40), im.matrix.brightness(0.15))
            hovered tt.Action("QuickSave!")
            action QuickSave()
        imagebutton:
            idle im.Scale("content/gfx/interface/buttons/load.png", 38, 40)
            hover im.MatrixColor(im.Scale("content/gfx/interface/buttons/load.png", 38, 40), im.matrix.brightness(0.15))
            hovered tt.Action("QuickLoad!")
            action QuickLoad()
    
    ### ----> Mid buttons <---- ###
    add "coin_top" pos (1015, 58)
    text "[hero.gold]" size 18 color gold pos (1052, 62) outlines [(1, "#3a3a3a", 0, 0)]
    button:
        style "sound_button"
        pos (1138, 55)
        xysize (35, 35)
        action [SelectedIf(not (_preferences.mute["music"] or _preferences.mute["sfx"])),
        If(_preferences.mute["music"] or _preferences.mute["sfx"],
        true=[Preference("sound mute", "disable"), Preference("music mute", "disable")],
        false=[Preference("sound mute", "enable"), Preference("music mute", "enable")])]
        
    add ProportionalScale("content/gfx/frame/frame_ap.png", 155, 50) pos (1040, 90)
    text "[hero.AP]" style "TisaOTM" color "#f1f1e1" size 24 outlines [(1, "#3a3a3a", 0, 0)] pos (1143, 85)
    fixed:
        pos (1202, 99)
        xsize 72
        text "Day [day]" style "TisaOTMolxm" color "#f1f1e1" size 18
    add "content/gfx/interface/buttons/compass.png" pos (1187, 15)
    
    add "content/gfx/images/m_2.png"
    
    ### ----> Lower buttons <---- ###
    side "c r":
        pos (1104, 132)
        xysize(172, 188)
        viewport id "locations":
            draggable True
            mousewheel True
            has vbox style_group "dropdown_gm2" spacing 2 ysize 10000
            $ prefix = "content/gfx/interface/buttons/locations/"
            for loc in pytfall.maps("pytfall"):
                if loc["id"] in loc_list and not key.get("hidden", False):
                    button:
                        xysize (160, 28)
                        idle_background Frame(im.MatrixColor(prefix + loc["id"] + ".png", im.matrix.brightness(0.10)), 5, 5)
                        hover_background Frame(im.MatrixColor(prefix + loc["id"] + "_hover.png", im.matrix.brightness(0.15)), 5, 5)
                        hovered tt.action(loc['name'])
                        action Return(['location', loc["id"]])
                    
        vbar value YScrollValue("locations")
    
    #use pyt_top_stripe(True, use_hide_transform=True, normal_op=False)
            
