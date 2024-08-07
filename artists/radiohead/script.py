from lyriguessr.lyrics import save_album_lyrics

API_KEY = "sFB433-aPPAH8VpsfF9ETSr-9SQYsbxFBGMTd_XvqF6ED84O-fMYiGf_ENUtNLRn"
radiohead_albums = ["Pablo Honey", 
                    "The Bends",
                    "OK Computer",
                    "Kid A",
                    "Amnesiac",
                    "Hail To the Thief",
                    "In Rainbows",
                    "The King Of Limbs", 
                    "A Moon Shaped Pool"]

save_album_lyrics(API_KEY, radiohead_albums, "Radiohead")
