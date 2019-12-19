#lvl45ranker.py         12/19/2019
#This code gives you the pvp ranking & addl stats about pokemon in Pogo
#Run in python2.7

import math

#Attack = (Base Attack + Individual Attack) * CP_Multiplier
#Def...
#Sta...

#CPM = Base_CPM + Additional_CPM

#CP = (Attack * Defense^0.5 * Stamina^0.5 * CP_Multiplier^2) / 10

#Max CP = ((Base_Attack + 15) * ((Base_Defense + 15)^0.5 
#    * (Base_Stamina + 15)^0.5 * 0.7903001^2) / 10

'----------------------------  Notes/Header Above  =---------------------------'

#Relevant funcitons:
#   def getStat(name,stat,iv,lvl): Will return the stat for a pokemon given 
#                                  name/iv/lvl
#   def getCP(name,atkiv,dfiv,stiv,lvl): Will return the CP for a pokemon given
#                                        name/ivs/lvl
#   def evalPkmn(name, league, atkiv, dfiv, stiv):
#               Will return a the ranking and additional stats about a pokemon
#               given name, league ('great','ultra','master'), & ivs

#Note: put print before function calls to get output
def doFnCalls():
    print evalPkmn("Nidoking","ultra",0,13,15)
    #print getStat(name,stat,iv,lvl)
    #print getCP(name,atkiv,dfiv,stiv,lvl)

#Lists in output are of the form:
#   [cp, atk, df, st, statprod, lvl, atkiv, defiv, staiv]



doAnalysis = True
#^set this flag to True if you want the program to run analysis on which
#pokemon get significantly different from the buddy level boost
#(but it will take a while to crunch all the numbers)


'---------------------------  Implementation Below  ---------------------------'

#sourced from https://gamepress.gg/pokemongo/cp-multiplier
CPM = [[1, 0.094],
[1.5, 0.1351374318],
[2, 0.16639787],
[2.5, 0.192650919],
[3, 0.21573247],
[3.5, 0.2365726613],
[4, 0.25572005],
[4.5, 0.2735303812],
[5, 0.29024988],
[5.5, 0.3060573775],
[6, 0.3210876],
[6.5, 0.3354450362],
[7, 0.34921268],
[7.5, 0.3624577511],
[8, 0.3752356],
[8.5, 0.387592416],
[9, 0.39956728],
[9.5, 0.4111935514],
[10, 0.4225],
[10.5, 0.4329264091],
[11, 0.44310755],
[11.5, 0.4530599591],
[12, 0.4627984],
[12.5, 0.472336093],
[13, 0.48168495],
[13.5, 0.4908558003],
[14, 0.49985844],
[14.5, 0.508701765],
[15, 0.51739395],
[15.5, 0.5259425113],
[16, 0.5343543],
[16.5, 0.5426357375],
[17, 0.5507927],
[17.5, 0.5588305862],
[18, 0.5667545],
[18.5, 0.5745691333],
[19, 0.5822789],
[19.5, 0.5898879072],
[20, 0.5974],
[20.5, 0.6048236651],
[21, 0.6121573],
[21.5, 0.6194041216],
[22, 0.6265671],
[22.5, 0.6336491432],
[23, 0.64065295],
[23.5, 0.6475809666],
[24, 0.65443563],
[24.5, 0.6612192524],
[25, 0.667934],
[25.5, 0.6745818959],
[26, 0.6811649],
[26.5, 0.6876849038],
[27, 0.69414365],
[27.5, 0.70054287],
[28, 0.7068842],
[28.5, 0.7131691091],
[29, 0.7193991],
[29.5, 0.7255756136],
[30, 0.7317],
[30.5, 0.7347410093],
[31, 0.7377695],
[31.5, 0.7407855938],
[32, 0.74378943],
[32.5, 0.7467812109],
[33, 0.74976104],
[33.5, 0.7527290867],
[34, 0.7556855],
[34.5, 0.7586303683],
[35, 0.76156384],
[35.5, 0.7644860647],
[36, 0.76739717],
[36.5, 0.7702972656],
[37, 0.7731865],
[37.5, 0.7760649616],
[38, 0.77893275],
[38.5, 0.7817900548],
[39, 0.784637],
[39.5, 0.7874736075],
[40, 0.7903],
[40.5, 0.792803946731],
[41, 0.79530001],
[41.5, 0.797803921997],
[42, 0.8003],
[42.5, 0.802803892616],
[43, 0.8053],
[43.5, 0.807803863507],
[44, 0.81029999],
[44.5, 0.812803834725],
[45, 0.81529999]]


#sourced from https://www.reddit.com/r/TheSilphRoad/comments/a3cl8b/pvp_spreadsheet_of_pok%C3%A9mon_stats/
# and https://gamepress.gg/pokemongo/pokemon/413-trash
#hp atk def
PKMNstatsStr = """#1 Bulbasaur    128 118 111
#2 Ivysaur  155 151 143
#3 Venusaur 190 198 189
#4 Charmander   118 116 93
#5 Charmeleon   151 158 126
#6 Charizard    186 223 173
#7 Squirtle 127 94  121
#8 Wartortle    153 126 155
#9 Blastoise    188 171 207
#10 Caterpie    128 55  55
#11 Metapod 137 45  80
#12 Butterfree  155 167 137
#13 Weedle  120 63  50
#14 Kakuna  128 46  75
#15 Beedrill    163 169 130
#16 Pidgey  120 85  73
#17 Pidgeotto   160 117 105
#18 Pidgeot 195 166 154
#19 Rattata 102 103 70
#19 ARattata  102 103 70
#20 Raticate    146 161 139
#20 ARaticate 181 135 154
#21 Spearow 120 112 60
#22 Fearow  163 182 133
#23 Ekans   111 110 97
#24 Arbok   155 167 153
#25 Pikachu 111 112 96
#26 Raichu  155 193 151
#26 ARaichu   155 201 154
#27 Sandshrew   137 126 120
#27 ASandshrew    137 125 129
#28 Sandslash   181 182 175
#28 ASandslash    181 177 195
#29 NidoranF    146 86  89
#30 Nidorina    172 117 120
#31 Nidoqueen   207 180 173
#32 NidoranM    130 105 76
#33 Nidorino    156 137 111
#34 Nidoking    191 204 156
#35 Clefairy    172 107 108
#36 Clefable    216 178 162
#37 Vulpix  116 96  109
#37 AVulpix   116 96  109
#38 Ninetales   177 169 190
#38 ANinetales    177 170 193
#39 Jigglypuff  251 80  41
#40 Wigglytuff  295 156 90
#41 Zubat   120 83  73
#42 Golbat  181 161 150
#43 Oddish  128 131 112
#44 Gloom   155 153 136
#45 Vileplume   181 202 167
#46 Paras   111 121 99
#47 Parasect    155 165 146
#48 Venonat 155 100 100
#49 Venomoth    172 179 143
#50 Diglett 67  109 78
#50 ADiglett  67  109 82
#51 Dugtrio 111 167 134
#51 ADugtrio  111 201 145
#52 Meowth  120 92  78
#52 AMeowth   120 99  78
#53 Persian 163 150 136
#53 APersian  163 158 136
#54 Psyduck 137 122 95
#55 Golduck 190 191 162
#56 Mankey  120 148 82
#57 Primeape    163 207 138
#58 Growlithe   146 136 93
#59 Arcanine    207 227 166
#60 Poliwag 120 101 82
#61 Poliwhirl   163 130 123
#62 Poliwrath   207 182 184
#63 Abra    93  195 82
#64 Kadabra 120 232 117
#65 Alakazam    146 271 167
#66 Machop  172 137 82
#67 Machoke 190 177 125
#68 Machamp 207 234 159
#69 Bellsprout  137 139 61
#70 Weepinbell  163 172 92
#71 Victreebel  190 207 135
#72 Tentacool   120 97  149
#73 Tentacruel  190 166 209
#74 Geodude 120 132 132
#74 AGeodude  120 132 132
#75 Graveler    146 164 164
#75 AGraveler 146 164 164
#76 Golem   190 211 198
#76 AGolem    190 211 198
#77 Ponyta  137 170 127
#78 Rapidash    163 207 162
#79 Slowpoke    207 109 98
#80 Slowbro 216 177 180
#81 Magnemite   93  165 121
#82 Magneton    137 223 169
#83 Farfetch'd  141 124 115
#84 Doduo   111 158 83
#85 Dodrio  155 218 140
#86 Seel    163 85  121
#87 Dewgong 207 139 177
#88 Grimer  190 135 90
#88 AGrimer   190 135 90
#89 Muk 233 190 172
#89 AMuk  233 190 172
#90 Shellder    102 116 134
#91 Cloyster    137 186 256
#92 Gastly  102 186 67
#93 Haunter 128 223 107
#94 Gengar  155 261 149
#95 Onix    111 85  232
#96 Drowzee 155 89  136
#97 Hypno   198 144 193
#98 Krabby  102 181 124
#99 Kingler 146 240 181
#100 Voltorb    120 109 111
#101 Electrode  155 173 173
#102 Exeggcute  155 107 125
#103 Exeggutor  216 233 149
#103 AExeggutor   216 230 153
#104 Cubone 137 90  144
#105 Marowak    155 144 186
#105 AMarowak 155 144 186
#106 Hitmonlee  137 224 181
#107 Hitmonchan 137 193 197
#108 Lickitung  207 108 137
#109 Koffing    120 119 141
#110 Weezing    163 174 197
#111 Rhyhorn    190 140 127
#112 Rhydon 233 222 171
#113 Chansey    487 60  128
#114 Tangela    163 183 169
#115 Kangaskhan 233 181 165
#116 Horsea 102 129 103
#117 Seadra 146 187 156
#118 Goldeen    128 123 110
#119 Seaking    190 175 147
#120 Staryu 102 137 112
#121 Starmie    155 210 184
#122 Mr.Mime   120 192 205
#123 Scyther    172 218 170
#124 Jynx   163 223 151
#125 Electabuzz 163 198 158
#126 Magmar 163 206 154
#127 Pinsir 163 238 182
#128 Tauros 181 198 183
#129 Magikarp   85  29  85
#130 Gyarados   216 237 186
#131 Lapras 277 165 174
#132 Ditto  134 91  91
#133 Eevee  146 104 114
#134 Vaporeon   277 205 161
#135 Jolteon    163 232 182
#136 Flareon    163 246 179
#137 Porygon    163 153 136
#138 Omanyte    111 155 153
#139 Omastar    172 207 201
#140 Kabuto 102 148 140
#141 Kabutops   155 220 186
#142 Aerodactyl 190 221 159
#143 Snorlax    330 190 169
#144 Articuno   207 192 236
#145 Zapdos 207 253 185
#146 Moltres    207 251 181
#147 Dratini    121 119 91
#148 Dragonair  156 163 135
#149 Dragonite  209 263 198
#150 Mewtwo 214 300 182
#151 Mew    225 210 210
#152 Chikorita  128 92  122
#153 Bayleef    155 122 155
#154 Meganium   190 168 202
#155 Cyndaquil  118 116 93
#156 Quilava    151 158 126
#157 Typhlosion 186 223 173
#158 Totodile   137 117 109
#159 Croconaw   163 150 142
#160 Feraligatr 198 205 188
#161 Sentret    111 79  73
#162 Furret 198 148 125
#163 Hoothoot   155 67  88
#164 Noctowl    225 145 156
#165 Ledyba 120 72  118
#166 Ledian 146 107 179
#167 Spinarak   120 105 73
#168 Ariados    172 161 124
#169 Crobat 198 194 178
#170 Chinchou   181 106 97
#171 Lanturn    268 146 137
#172 Pichu  85  77  53
#173 Cleffa 137 75  79
#174 Igglybuff  207 69  32
#175 Togepi 111 67  116
#176 Togetic    146 139 181
#177 Natu   120 134 89
#178 Xatu   163 192 146
#179 Mareep 146 114 79
#180 Flaaffy    172 145 109
#181 Ampharos   207 211 169
#182 Bellossom  181 169 186
#183 Marill 172 37  93
#184 Azumarill  225 112 152
#185 Sudowoodo  172 167 176
#186 Politoed   207 174 179
#187 Hoppip 111 67  94
#188 Skiploom   146 91  120
#189 Jumpluff   181 118 183
#190 Aipom  146 136 112
#191 Sunkern    102 55  55
#192 Sunflora   181 185 135
#193 Yanma  163 154 94
#194 Wooper 146 75  66
#195 Quagsire   216 152 143
#196 Espeon 163 261 175
#197 Umbreon    216 126 240
#198 Murkrow    155 175 87
#199 Slowking   216 177 180
#200 Misdreavus 155 167 154
#201 Unown  134 136 91
#202 Wobbuffet  382 60  106
#203 Girafarig  172 182 133
#204 Pineco 137 108 122
#205 Forretress 181 161 205
#206 Dunsparce  225 131 128
#207 Gligar 163 143 184
#208 Steelix    181 148 272
#209 Snubbull   155 137 85
#210 Granbull   207 212 131
#211 Qwilfish   163 184 138
#212 Scizor 172 236 181
#213 Shuckle    85  17  396
#214 Heracross  190 234 179
#215 Sneasel    146 189 146
#216 Teddiursa  155 142 93
#217 Ursaring   207 236 144
#218 Slugma 120 118 71
#219 Magcargo   137 139 191
#220 Swinub 137 90  69
#221 Piloswine  225 181 138
#222 Corsola    146 118 156
#223 Remoraid   111 127 69
#224 Octillery  181 197 141
#225 Delibird   128 128 90
#226 Mantine    163 148 226
#227 Skarmory   163 148 226
#228 Houndour   128 152 83
#229 Houndoom   181 224 144
#230 Kingdra    181 194 194
#231 Phanpy 207 107 98
#232 Donphan    207 214 185
#233 Porygon2   198 198 180
#234 Stantler   177 192 131
#235 Smeargle   146 40  83
#236 Tyrogue    111 64  64
#237 Hitmontop  137 173 207
#238 Smoochum   128 153 91
#239 Elekid 128 135 101
#240 Magby  128 151 99
#241 Miltank    216 157 193
#242 Blissey    496 129 169
#243 Raikou 207 241 195
#244 Entei  251 235 171
#245 Suicune    225 180 235
#246 Larvitar   137 115 93
#247 Pupitar    172 155 133
#248 Tyranitar  225 251 207
#249 Lugia  235 193 310
#250 Ho-Oh  214 239 244
#251 Celebi 225 210 210
#252 Treecko    120 124 94
#253 Grovyle    137 172 120
#254 Sceptile   172 223 169
#255 Torchic    128 130 87
#256 Combusken  155 163 115
#257 Blaziken   190 240 141
#258 Mudkip 137 126 93
#259 Marshtomp  172 156 133
#260 Swampert   225 208 175
#261 Poochyena  111 96  61
#262 Mightyena  172 171 132
#263 Zigzagoon  116 58  80
#264 Linoone    186 142 128
#265 Wurmple    128 75  59
#266 Silcoon    137 60  77
#267 Beautifly  155 189 98
#268 Cascoon    137 60  77
#269 Dustox 155 98  162
#270 Lotad  120 71  77
#271 Lombre 155 112 119
#272 Ludicolo   190 173 176
#273 Seedot 120 71  77
#274 Nuzleaf    172 134 78
#275 Shiftry    207 200 121
#276 Taillow    120 106 61
#277 Swellow    155 185 124
#278 Wingull    120 106 61
#279 Pelipper   155 175 174
#280 Ralts  99  79  59
#281 Kirlia 116 117 90
#282 Gardevoir  169 237 195
#283 Surskit    120 93  87
#284 Masquerain 172 192 150
#285 Shroomish  155 74  110
#286 Breloom    155 241 144
#287 Slakoth    155 104 92
#288 Vigoroth   190 159 145
#289 Slaking    284 290 166
#290 Nincada    104 80  126
#291 Ninjask    156 196 112
#292 Shedinja   1   153 73
#293 Whismur    162 92  42
#294 Loudred    197 134 81
#295 Exploud    232 179 137
#296 Makuhita   176 99  54
#297 Hariyama   302 209 114
#298 Azurill    137 36  71
#299 Nosepass   102 82  215
#300 Skitty 137 84  79
#301 Delcatty   172 132 127
#302 Sableye    137 141 136
#303 Mawile 137 155 141
#304 Aron   137 121 141
#305 Lairon 155 158 198
#306 Aggron 172 198 257
#307 Meditite   102 78  107
#308 Medicham   155 121 152
#309 Electrike  120 123 78
#310 Manectric  172 215 127
#311 Plusle 155 167 129
#312 Minun  155 147 150
#313 Volbeat    163 143 166
#314 Illumise   163 143 166
#315 Roselia    137 186 131
#316 Gulpin 172 80  99
#317 Swalot 225 140 159
#318 Carvanha   128 171 39
#319 Sharpedo   172 243 83
#320 Wailmer    277 136 68
#321 Wailord    347 175 87
#322 Numel  155 119 79
#323 Camerupt   172 194 136
#324 Torkoal    172 151 203
#325 Spoink 155 125 122
#326 Grumpig    190 171 188
#327 Spinda 155 116 116
#328 Trapinch   128 162 78
#329 Vibrava    137 134 99
#330 Flygon 190 205 168
#331 Cacnea 137 156 74
#332 Cacturne   172 221 115
#333 Swablu 128 76  132
#334 Altaria    181 141 201
#335 Zangoose   177 222 124
#336 Seviper    177 196 118
#337 Lunatone   207 178 153
#338 Solrock    207 178 153
#339 Barboach   137 93  82
#340 Whiscash   242 151 141
#341 Corphish   125 141 99
#342 Crawdaunt  160 224 142
#343 Baltoy 120 77  124
#344 Claydol    155 140 229
#345 Lileep 165 105 150
#346 Cradily    200 152 194
#347 Anorith    128 176 100
#348 Armaldo    181 222 174
#349 Feebas 85  29  85
#350 Milotic    216 192 219
#351 Castform   172 139 139
#352 Kecleon    155 161 189
#353 Shuppet    127 138 65
#354 Banette    162 218 126
#355 Duskull    85  70  162
#356 Dusclops   120 124 234
#357 Tropius    223 136 163
#358 Chimecho   181 175 170
#359 Absol  163 246 120
#360 Wynaut 216 41  86
#361 Snorunt    137 95  95
#362 Glalie 190 162 162
#363 Spheal 172 95  90
#364 Sealeo 207 137 132
#365 Walrein    242 182 176
#366 Clamperl   111 133 135
#367 Huntail    146 197 179
#368 Gorebyss   146 211 179
#369 Relicanth  225 162 203
#370 Luvdisc    125 81  128
#371 Bagon  128 134 93
#372 Shelgon    163 172 155
#373 Salamence  216 277 168
#374 Beldum 120 96  132
#375 Metang 155 138 176
#376 Metagross  190 257 228
#377 Regirock   190 179 309
#378 Regice 190 179 309
#379 Registeel  190 143 285
#380 Latias 190 228 246
#381 Latios 190 268 212
#382 Kyogre 205 270 228
#383 Groudon    205 270 228
#384 Rayquaza   213 284 170
#385 Jirachi    225 210 210
#386 DeoxysNorm  137 345 115
#386 DeoxysAtk  137 414 46
#386 DeoxysDef 137 144 330
#386 DeoxysSpd   137 230 218
#387 Turtwig    146 119 110
#388 Grotle 181 157 143
#389 Torterra   216 202 188
#390 Chimchar   127 113 86
#391 Monferno   162 158 105
#392 Infernape  183 222 151
#393 Piplup 142 112 102
#394 Prinplup   162 150 139
#395 Empoleon   197 210 186
#396 Starly 120 101 58
#397 Staravia   146 142 94
#398 Staraptor  198 234 140
#399 Bidoof 153 80  73
#400 Bibarel    188 162 119
#401 Kricketot  114 45  74
#402 Kricketune 184 160 100
#403 Shinx  128 117 64
#404 Luxio  155 159 95
#405 Luxray 190 232 156
#406 Budew  120 91  109
#407 Roserade   155 243 185
#408 Cranidos   167 218 71
#409 Rampardos  219 295 109
#410 Shieldon   102 76  195
#411 Bastiodon  155 94  286
#412 Burmy  120 53  83
#413 Wormadam   155 141 180
#413 WormadamT 155 127 175 
#414 Mothim 172 185 98
#415 Combee 102 59  83
#416 Vespiquen  172 149 190
#417 Pachirisu  155 94  172
#418 Buizel 146 132 67
#419 Floatzel   198 221 114
#420 Cherubi    128 108 92
#421 Cherrim    172 170 153
#422 Shellos    183 103 105
#423 Gastrodon  244 169 143
#424 Ambipom    181 205 143
#425 Drifloon   207 117 80
#426 Drifblim   312 180 102
#427 Buneary    146 130 105
#428 Lopunny    163 156 194
#429 Mismagius  155 211 187
#430 Honchkrow  225 243 103
#431 Glameow    135 109 82
#432 Purugly    174 172 133
#433 Chingling  128 114 94
#434 Stunky 160 121 90
#435 Skuntank   230 184 132
#436 Bronzor    149 43  154
#437 Bronzong   167 161 213
#438 Bonsly 137 124 133
#439 MimeJr.   85  125 142
#440 Happiny    225 25  77
#441 Chatot 183 183 91
#442 Spiritomb  137 169 199
#443 Gible  151 124 84
#444 Gabite 169 172 125
#445 Garchomp   239 261 193
#446 Munchlax   286 137 117
#447 Riolu  120 127 78
#448 Lucario    172 236 144
#449 Hippopotas 169 124 118
#450 Hippowdon  239 201 191
#451 Skorupi    120 93  151
#452 Drapion    172 180 202
#453 Croagunk   134 116 76
#454 Toxicroak  195 211 133
#455 Carnivine  179 187 136
#456 Finneon    135 96  116
#457 Lumineon   170 142 170
#458 Mantyke    128 105 179
#459 Snover 155 115 105
#460 Abomasnow  207 178 158
#461 Weavile    172 243 171
#462 Magnezone  172 238 205
#463 Lickilicky 242 161 181
#464 Rhyperior  251 241 190
#465 Tangrowth  225 207 184
#466 Electivire 181 249 163
#467 Magmortar  181 247 172
#468 Togekiss   198 225 217
#469 Yanmega    200 231 156
#470 Leafeon    163 216 219
#471 Glaceon    163 238 205
#472 Gliscor    181 185 222
#473 Mamoswine  242 247 146
#474 Porygon-Z  198 264 150
#475 Gallade    169 237 195
#476 Probopass  155 135 275
#477 Dusknoir   128 180 254
#478 Froslass   172 171 150
#479 Rotom  137 185 159
#480 Uxie   181 156 270
#481 Mesprit    190 212 212
#482 Azelf  181 270 151
#483 Dialga 204 275 211
#484 Palkia 188 280 215
#485 Heatran    209 251 213
#486 Regigigas  220 287 210
#487 GiratinaAlt   284 187 225
#487 GiratinaOrgn    284 225 187
#488 Cresselia  260 152 258
#489 Phione 190 162 162
#490 Manaphy    225 210 210
#491 Darkrai    172 285 198
#492 ShayminLand   225 210 210
#492 ShayminSky   225 261 166
#493 Arceus 236 238 238
#808 Meltan 130 118 130
#809 Melmetal   264 226 190"""

PKMNstats = []
for oPkmn in PKMNstatsStr.split("\n"):
    oPkmn = oPkmn.split(" ")
    # print oPkmn
    pkmn = []
    for atr in xrange(len(oPkmn)):
        if atr == 0: pkmn.append(int(oPkmn[0][1:]))
        elif oPkmn[atr] == '': continue
        else:
            try:
                pkmn.append(int(oPkmn[atr]))
            except:
                pkmn.append(oPkmn[atr])

    PKMNstats.append(pkmn)

# print PKMNstats

def nameToPkmn(name):
    return PKMNstats[map(lambda x: x[1], PKMNstats).index(name)]

def getStat(name,stat,iv,lvl):
    pkmn = nameToPkmn(name)
    if stat == "atk": stat = pkmn[-2]
    elif stat == "df": stat = pkmn[-1]
    elif stat == "st": stat = pkmn[-3]
    else: 0/0
    return (stat+iv)*CPM[int(lvl*2)-2][1]

# print getStat("Sableye","atk",15,40)

#CP = (Attack * Defense^0.5 * Stamina^0.5 * CP_Multiplier^2) / 10
def getCP(name,atkiv,dfiv,stiv,lvl):
    pkmn = nameToPkmn(name)
    atk,df,st = pkmn[-2], pkmn[-1], pkmn[-3]
    return math.floor(((atk+atkiv) * (df+dfiv)**.5 * (st+stiv)**.5 * CPM[int(lvl*2)-2][1]**2)/10)

# print getCP("Sableye",0,0,0,45)

def calcAllCombs(name, league, doAnalysis = False):
    if not(doAnalysis): print "Calculating for " + name + ":"#\nConsidering level...."
    pkmn = nameToPkmn(name)
    cpCombs = [] #[[cp, atk, df, st, prod, lvl, atkiv, defiv, staiv], ...]
    for dlvl in xrange(2,91):
        # print lvl
        lvl = dlvl*1.0/2
        minCP = getCP(name,0,0,0,lvl)
        maxCP = getCP(name,15,15,15,lvl)
        if (dlvl < 80):
            if league == "great":
                if ((maxCP < 1400) or (1501 < minCP)): continue
            elif league == "ultra":
                if ((maxCP < 2200) or (2501 < minCP)): continue
            else: continue
        # if not(doAnalysis): print lvl
        for atk in xrange(0,16):
            for df in xrange(0,16):
                for st in xrange(0,16):
                    cp = getCP(name,atk,df,st,lvl)
                    atkVal = getStat(name,"atk",atk,lvl)
                    dfVal = getStat(name,"df",df,lvl)
                    stVal = math.floor(getStat(name,"st",st,lvl))
                    prod = atkVal * dfVal * stVal
                    if ((league == "great") and (cp > 1500)): continue
                    elif ((league == "ultra") and (cp > 2500)): continue
                    cpCombs.append([cp,
                        atkVal,
                        dfVal,
                        stVal,
                        prod,
                        lvl, atk, df, st
                        ])
                    # print cpCombs[-1]
    return cpCombs

# Sab = calcAllCombs("Sableye", "great")
# Sab.sort(key = lambda x: x[4], reverse = True)
# print Sab[0]

def evalPkmn(name, league, atkiv, dfiv, stiv, doAnalysis = False):
    combs = calcAllCombs(name, league)
    combs.sort(key = lambda x: x[4], reverse = True)
    
    relLvls = []
    for comb in combs:
        if (atkiv,dfiv,stiv) == (comb[-3],comb[-2],comb[-1]): relLvls.append(comb)
    relLvls.sort(key = lambda x: x[4], reverse = True)
    lvl = relLvls[0][5]
    atkVal = getStat(name,"atk",atkiv,lvl)
    dfVal = getStat(name,"df",dfiv,lvl)
    stVal = math.floor(getStat(name,"st",stiv,lvl))
    prod = atkVal * dfVal * stVal

    combs.sort(key = lambda x: x[4], reverse = True)
    # PKMNstats[map(lambda x: x[1], PKMNstats).index(name)]
    rank = map(lambda x: x[4], combs).index(prod) + 1
    perfPct = prod/combs[0][4]

    if not(doAnalysis):
        print
        print("Stats:\t"),
        print combs[rank-1]
        print("Percent Perfect:\t"),
        print perfPct
        print("Rank:"),
        print "\t" + str(rank)

    combs.sort(key = lambda x: x[4], reverse = True)

    print
    print("Best Spread <= lvl40:\t"),
    print filter(lambda x: x[5]<=40, combs)[0]

    # combs.sort(key = lambda x: x[4], reverse = True)

    # perfPct = prod/combs[0][4]
    
    # if not(doAnalysis):
        

    print("Percent Improvement:\t"),
    print combs[0][4]/filter(lambda x: x[5]<=40, combs)[0][4]-1
        

    print("Rank 1 <= lvl45:\t"),
    print combs[0]

    combs.sort(key = lambda x: x[1], reverse = True)

    print("Max Atk:"),
    print('\t'),
    print combs[0]

    combs.sort(key = lambda x: x[2], reverse = True)

    print("Max Def:"),
    print('\t'),
    print combs[0]

    combs.sort(key = lambda x: x[3], reverse = True)

    print("Max Stam:"),
    print('\t'),
    print combs[0]

    # for n in xrange(0,25):
    #     print combs[n]
    #     pass

    # print perfPct
    # print rank
    # print len(combs)
    # for n in xrange(0,11):
    #     print combs[rank-6+n] + [rank-5+n]

    #Note: ranks are a little off from GoStadium, not sure why...
    #      current theories are rounding differences, or that the > lvl40 pkmn affect my ranks

    return ""


# print evalPkmn("Sableye", "great", 13, 15, 15)

# PKMNstats = [[33, 'Nidorino'   ,156, 137, 111],
# [8, 'Wartortle',    153 ,126, 155]]

# doAnalysis = False

def analyze():
    for pkmn in PKMNstats:
        lvl40cp = getCP(pkmn[1],15,15,15,40)
        atkVal = getStat(pkmn[1],"atk",15,40)
        dfVal = getStat(pkmn[1],"df",15,40)
        stVal = math.floor(getStat(pkmn[1],"st",15,40))
        prod = atkVal * dfVal * stVal
        if ((1350 < lvl40cp) and (lvl40cp < 1650)):
            print pkmn[1] + " GL"
            print "Stats @ lvl40 15/15/15:\t\t",
            print [lvl40cp, atkVal, dfVal, stVal, prod, 40, 15, 15, 15]
            evalPkmn(pkmn[1],"great",15,15,15, doAnalysis = True)
            print "-----------"
            print
        elif((2300 < lvl40cp) and (lvl40cp < 2700)):
            print pkmn[1] + " UL"
            print "Stats @ lvl40 15/15/15:\t\t",
            print [lvl40cp, atkVal, dfVal, stVal, prod, 40, 15, 15, 15]
            evalPkmn(pkmn[1],"ultra",15,15,15, doAnalysis = True)
            print "-----------"
            print


def fnCallsWrapper():
    doFnCalls()
    print "-----------"
    print "-----------"
    print
    if doAnalysis: analyze()


fnCallsWrapper()
