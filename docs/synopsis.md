# Synopsis - MÄR Heaven: Knockin' on Heaven's Door (GBA, Konami 2005)

For translators and reviewers. Story order, the scripts that belong to each part, who is who, and what must not be
given away early. Source: `work/tl/story.txt` (script text), `tools/debug/scenes.lua` (debug chapter select order).
Name spellings here are proposals; the binding list is `glossary.md` (proposals in `work/tl/terms_proposal.tsv`).

## The game in one paragraph

Ginta Toramizu, a weak, near-sighted Tokyo middle-schooler who has dreamed the same fairy-tale dream 102 times, is
pulled into the world of MÄR Heaven by the Gatekeeper Clown ÄRM. There he is strong and sharp-eyed. He wins the
talking ÄRM Babbo, befriends the farm boy Jack, meets the witch Dorothy, the princess Snow and her dog Ed, and
learns that the Chess Pieces, who nearly took the world six years ago, are back. The team names itself MÄR, frees
the village of Vestry, and then (the game's own story, not in the manga) helps a boy named Marl dig up the three
parts of an ancient giant Guardian ÄRM, Talos, which turns out to be a trap. The game ends with Peta announcing the
Chess Pieces' invasion and Ginta vowing to protect MÄR Heaven.

## Register

- Aimed at children: almost all text is kana, with furigana-style glosses in brackets (魔力（まりょく）, 魔女（まじょ）).
  Write plain, lively English a ten-year-old can read; no archaic words except where a character is meant to sound
  old-fashioned (Babbo, Ed the dog, Papa Rock).
- Many exclamation marks, trailing ーーー and ～～～, ♥ and ♪. Keep the energy, not the punctuation count.
- `{C0904}` / `{C0B04}` look like colour/style codes (C0B is used for Orco's stutter and the unseen voices; exact
  meaning unverified) and `C0F04` is an item-name variable: keep them where they are.
- Tutorial text is spoken in-character (Dorothy, Babbo, Merillo, townspeople, Ed): keep the button names exact.

## Story order

### 0. Prologue: Tokyo (OPEN)
- Ginta daydreams in class that he wields the holy sword "Holy Thunder Force"; the teacher sends him to run 100
  laps (he collapses after 8). Koyuki, his childhood friend, is the only one who doesn't laugh at his dream of a
  fairy-tale world (candy houses, talking trees, three-headed birds, fairies).
- The Gatekeeper Clown opens a tunnel in the classroom ("Tunnel... open!"). Only Ginta can see the other world;
  Koyuki can't, and makes him promise to tell her everything later. The opening narration ("This is... a gamble.
  ÄRM, lead the way! And answer, dweller of another world!") is the summoner's voice (Alviss, revealed in ch. 3).

### 1. Arrival and Babbo (EV_START, HI_M00, EV_RT01-03, CH_M00A, SP_M00, SP_M01, EV_BIN01-03, HI_M01_1, HI_M01_2, EV_BA01-04, CH_M01_3, EV_GTOB, EV_GTOB2, EV_IWA, OBJ_G, SP_M01_3)
- Ginta wakes in a field: "It's not a dream!" He can see without his glasses and runs without tiring.
- Papa Rock and Little Rock (talking rocks) ask him to fetch water from the stream to the north. A Ring Armor
  attacks; Ginta throws it bare-handed. Dorothy appears, amazed: he used no ÄRM. She explains ÄRM (accessories
  engraved with magic power that give special abilities) and lures him along with a promised dagger ÄRM. Papa Rock
  is terrified of her: "That's Dorothy... the infamous witch!"
- In a ruin she needs Babbo, a rare ÄRM sealed in a chest she can't open. Ginta opens it (it opens only for someone
  with zero magic power); a Guardian ÄRM trap appears; Babbo wakes up with no memory except his name, refuses to
  fight, then fights because it woke him. Battle tutorial: "B for Babbo".
- Babbo refuses to belong to Dorothy ("you reek of wicked magic"), so she gives "this cheeky ugly thing" to Ginta,
  teaches Magic Stones (ÄRM anyone can use), "A for ÄRM", the Synchro Gauge and the 20-ÄRM deck, and leaves with the
  Guardian ÄRM as her prize, warning that a living Weapon ÄRM will draw a lot of unwanted attention.
- EV_GTOB/2: Babbo stomps off alone, gets into trouble, is rescued, and "allows" Ginta to be his servant. Ginta calls
  him a useless ÄRM and a kendama. Their bickering friendship starts here.
- SP_M01_3 (revisit, later): a chest only "the one who sealed it" can open (Ed/Alan; see ch. 6).

### 2. Jack and the Loup-Garou Brothers (EV_JA01-04, EV_JA04B, EV_JA04C, CH_M08A, SP_M40, J_VS_M)
- Ginta eats vegetables from a field (they are ÄRM vegetables; Jack can't believe he's alive). Jack and his mother
  are being robbed by the werewolf thieves Luga and Garu (the Loup-Garou Brothers). Jack, always too scared before,
  finally fights them with his shovel; Babbo stops Ginta from helping ("he is becoming a man!"). Then Ginta and Jack
  beat them together.
- Peta (Chess Piece; not named as such here) arrives to hire the brothers, notices Babbo: "So you're the one who
  broke the seal..." and drags them off. A quiet foreshadowing.
- Ginta remembers his own mother back home and decides to look for an ÄRM to get home. Jack's mother gives him
  Jack's hand-me-down clothes and sends Jack with him.
- J_VS_M: on later visits she gives ÄRM a traveller paid her with (Rafflesia, Djinn CL3).

### 3. Paz Town and Alviss (G_EV001, EV_PA01, CH_M09A, HI_M09, SHOPPA01-05, EV_AL01-04)
- Paz Town, the biggest town nearby, has a market. Townspeople explain decks and magic cost. Ginta asks the ÄRM
  dealer about Dimension ÄRM; his description of the ÄRM that brought him (cross-shaped eyes, tongue out) is the
  Gatekeeper Clown, a top-class Dimension ÄRM nobody owns but kings and witches. Ginta is secretly glad: more
  adventure, and more time with Jack.
- Thieves steal Babbo. Alviss beats them, then uses the Darkness ÄRM "Bird Cage" to turn Jack into a bird and
  reveals he summoned Ginta with the Gatekeeper Clown, hoping for someone strong: "the gamble failed".
- He explains the Chess Pieces (an evil army that tried to take MÄR Heaven 6 years ago; the leader of the army that
  beat them was also an otherworlder, now dead) and that Babbo was the ÄRM of Phantom, the Chess Pieces' leader.
  He means to destroy Babbo; Ginta punches him ("Babbo is my friend!") and loses.
- Alviss spares Babbo: "If you chose to be a target, get strong." Ginta resolves to get stronger.

### 4. Ed and the Ice Castle (EV_EDO01, EV_ICE01-12, HI_M04, SP_M04)
- Ginta finds a talking dog, Edward (Ed), who must sleep three times and can't; his princess is in danger. The
  princess sealed herself in ice inside a castle on this remote island to escape the new queen of her far-off
  country, who seized power and is removing everyone in her way.
- Dorothy turns up again, gushing over "Gintan", and helps from the shadows (clears a floor of monsters).
- Ginta sneezes "crystal snot". The Chess Pieces Loco and Ian wait at the top for Halloween to bring an ÄRM that can
  break the seal.
- The frozen girl looks exactly like Koyuki. She is Snow, heir of Lestava, the symbol of MÄR Heaven. Ginta fights
  Ian one-on-one and breaks his right arm.
- **Twist (EV_ICE10):** Ed's third sleep: a rough man comes out of the dog, Alan. Dog and man share a body (dog
  sleeps 3 times -> Alan; Alan sleeps once -> dog). Alan beats Ian, gives Ginta the fire ÄRM Melt Ice; Snow is freed.
- Halloween arrives: all Chess Pieces are recalled, the hunt for the princess is paused, because Phantom has said
  "I have returned". He knows Alan ("six years, huh?"). Alan calls him "tomato-head"; Halloween calls Ginta
  "spiky-head". Ginta finds Snow's voice and gestures oddly familiar.

### 5. Pelica: Cross Guard and resolve (G_EV010, G_EV011, G_EV011B, G_EV011C, G_EV012, G_EV013, SHOPPE01-02, SP_M42)
- In the diner (cheese and a few beans), Alan explains: they are on Pazurica, a small island; Lestava, Snow's home on
  the southern continent, ruled the small countries and is now a Chess base. Six years ago the otherworlder Danna led
  the Cross Guard against the Chess Pieces and died taking down Phantom.
- Alan on Snow: raised in a box, her mother dead, her stepmother wants her dead, yet she keeps smiling.
- Ginta: "Let's go beat the Chess boss!" Alan (to himself): "Danna... he says the same things you did."
- G_EV013: Ian and Gido ask townsfolk about "the group with a round, moustached ÄRM".

### 6. The Training Gate; MÄR is formed (G_EV020, G_EV020B, G_EV020C, EV_MON01, EV_MON02, EV_MON04, EV_MON05, EV_MON06, G_EV021, G_EV023, G_EV023C, CH_M05A, G_EV024, G_EV025, G_EV025B)
- Alan sealed Babbo himself (a chest only zero-magic can open, a Guardian only zero-magic can't beat... yet Ginta
  got it with Dorothy). Dorothy is caught spying; Snow stops the fight; Dorothy senses a love rival in Snow.
- Magic power: "a kind of 'ki' every ÄRM user has". Ginta and Jack: zero. Alan sends everyone through the Dimension
  ÄRM "Training Gate": Ginta and Snow with Merillo, Jack and Dorothy with Bumol (no saving inside!). Jack takes up
  the shovel his late father left him. Gates later become Dungeon Mode.
- G_EV020C: Alviss visits Alan ("Alan-san"); he has little time left and must defeat Phantom. Alan bets Ginta may be
  the saviour.
- G_EV021: Cross Guard radio: towns burning, "the Chess Pieces are back", "where is Alan, Cross Guard's No. 2?".
  Alviss asks Alan to help; Alan stays to keep the gate open. Alviss: "You disappoint me!"
- After 3 sleepless days Alan is beaten by Ian (rank lesson: Pawn < Rook < Bishop < Knight; Ian is a Rook). Ginta
  comes out of the gate and beats Ian, now Bishop-level; Jack (with Dorothy) beats Gido. Ian trades Healing Angel for
  his escape and vows to rise higher.
- G_EV025B: Ed the dog is back. Snow recalls the castle fortune-teller: "Build a new army... seek seven heroes."
  The team is formed; Ginta names it MÄR, "the warriors who save MÄR Heaven".

### 7. Magic Carpet and Luberia (G_EV030, G_EV031, G_EV002, G_EV003, G_EV004, G_EV005, G_EV006, G_EV007, SP_M06_1)
- Ed flies them by Magic Carpet to the Hildo continent. Ed explains witches live isolated on the Caldia islands;
  Dorothy is the infamous one, basically a thief. Dorothy overhears; Ed: "...I said beautiful!"
- They are shot down by Nanashi's men: Nanashi, boss of the thieves' guild Luberia, takes them for Chess Pieces
  ("Death penalty!"), then apologises. He shows them his comrades' graves: all MÄR Heaven is becoming a graveyard.
- News: Chess Pieces rampaging at Vestry, northwest Hildo. Nanashi joins and takes them there by Dimension ÄRM.

### 8. Vestry and the underground lake (EV_VE01, EV_VE02, CH_M11, HI_M11, S_MAP11, EV_GO01-12, HI_M07, SP_M07_1, EV_UTA01)
- Vestry, "village of water and woods", is in ruins; villagers have given up. One was a Cross Guard member. Two Chess
  Pieces went into the underground lake for a hidden ÄRM; legend says its ghosts bring disaster. A villager gives
  Gargoyle CL4 (it needs a special ÄRM to work). Snow and Ed stay to heal; Jack rebuilds and plants.
- Ginta, Nanashi and Dorothy go in; the path splits (Babbo insists he counts as a person, not "one item").
- Nanashi beats Orco with Electric Eye. Tom, a Vestry boy, guides Ginta. Ginta beats Girom on a wrecked ship, hears a
  voice ("help me"), and uses Gargoyle to free the trapped ghosts, who give him Gargoyle CL5 and Alice.
- EV_UTA01: the victory party. Nanashi flirts, Ed sobs at Snow's kindness, the villagers find courage again.

### 9. The three dungeons and Marl (L11_0_0, G_EV040, L11_0_2, L11_0_3, L24_0_0, CH_M24_A, HI_M24, HI_M24_2, HI_M24_4, G_EV041, G_EV042, HI_M24_1, SP_M24, SP_M24_3, SP_M24_4, EV_T1KIL, G_EV043, G_EV044, G_EV050, HI_M25_1, HI_M25_2, G_EV051, G_EV052, L25_4_0, SP_M25_4, SP_M25_5, EV_T2KIL, G_EV060, G_EV061, G_EV063, HI_M26_2, SP_M26_2)
- Ginta and Jack follow a figure to a strange "space cut out from somewhere else" with three doors. Bellini, an
  apprentice engraver who ends every sentence with ですのん, explains engraving (combine materials into new ÄRM) and
  that she lost her recipes to the other world (the player's world: real-life codes unlock recipes).
- Marl, a timid boy in glasses, says he studies ruins; an ancient giant Guardian ÄRM in 3 parts lies sealed here,
  usable even with little magic power; the Gargoyle blast at the lake broke the door seal. Chess destroyed his
  country, he says. Ginta promises to help.
- A huge ice block bars the way. Dorothy arrives, gets "oh, it's just you" looks, tries to out-do Snow, freezes her
  skirt and fails; Ginta fetches Snow. Dorothy sulks for several scenes (ふんだ!).
- The arms part (EV_T1KIL): Marl grins in an aside; Snow feels something nasty. Nanashi joins for the legs; the team
  must flatter Dorothy into helping (Babbo's "praise": "the terrifying witch who silences crying babies"). Legs
  (EV_T2KIL): Dorothy senses evil magic. Nanashi recognises the crest on the chest and goes back to Luberia to check
  an old document (his men can't read his drawing).
- G_EV061: Dorothy accuses Marl. Ginta snaps that Dorothy, the ÄRM thief, is more suspicious; Snow: "I hate you,
  Ginta!" Ginta goes on alone with Marl.

### 10. Betrayal: Talos (EV_T3KIL, G_EV062, SP_M26_5, OBJ_D, OBJ_J, OBJ_S, OBJ_V, OBJ_G, CH_M26_6, EV_T4KIL)
- **Twist (EV_T3KIL):** with the head, Marl drops the act: he is "an ordinary Chess Piece". The three parts form
  Talos, a Guardian ÄRM engraved with an ancient secret art that obeys its wielder's desires. Dorothy shields Ginta
  and is hurt; Ginta carries her away. Marl wants Babbo, "Phantom's ÄRM".
- G_EV062: Nanashi learned the seal opens only for one with wicked desire. Alviss returns. Ginta apologises to
  Dorothy (she kisses him; Snow pinches). Party Change unlocks.
- SP_M26_5: friends clear the way (Alviss fills holes, Dorothy removes magic walls, Snow melts ice); Jack: "I'd still
  be a coward without you". CH_M26_6: Talos absorbed Babbo's power (arms, head) and Dorothy's (legs). Alan: "You
  sowed it, you reap it!"
- EV_T4KIL: Talos falls. Marl breaks down crying: he only wanted Phantom to praise him. Alan lets him go but keeps the
  ÄRM. Vestry's people go back above ground.

### 11. Ending (END2, SROLL, DUNG_END)
- Exhausted, everyone turns in; Ginta sulks. Under the moon Snow tells him she is weak and scared too, but his promise
  ("I'll do my best and save Snow!") saved her heart; now she'll "do her best and save Ginta". Ginta: he must go home
  someday, but not this weak; he promised Alan he'd get strong.
- The moon shows Peta: the Chess Pieces' advance begins; the world shall fear, despair and kneel. Ginta: "However big
  MÄR Heaven is... I'll crush every one of you! I'll protect this MÄR Heaven I love!" Staff roll; password screen
  "SNOW PRINCESS". DUNG_END: clearing Dungeon Mode adds the Final Gate and makes Phantom playable.

### Side, system and debug scripts
- Shops: SHOPPA01 ÄRM dealer, 02 Magic Stone dealer, 03 item dealer, 04 inn (100 P), 05 street vendor (Paz Town);
  SHOPPE01 ÄRM dealer, 02 Magic Stone dealer (Pelica).
- Rewards on revisits: G_VS_R (Papa Rock gives Gatling Babbo), D_VS_R (with Dorothy; see jokes), J_VS_M (Jack's mother).
- Chests and field: SP_M00/M01/M04/M07_1/M10_1/M40/M42, SP_M08 (PIN-locked chest: unlocks school-uniform Ginta for
  Versus/Dungeon Mode, L/R to switch), SPR_DUNG, DITEMCOM (inventory full / obtained), HI_DUNG, W_MAP.
- Debug only (never seen by players): DBG_FACE (portrait names), FULL_ITM, SROLL ("staff roll starting"), the
  CH_ESC chapter select. Translate plainly; low priority.

## Who is who

| JP | EN | What | How they talk |
|---|---|---|---|
| ギンタ (虎水ギンタ) | Ginta (Ginta Toramizu) | Tokyo middle-schooler, hero; weak and bespectacled at home, strong in MÄR Heaven | オレ, rough boyish, ぜ/だぜ, shouts; calls Alan/Ed オッサン "old man", Dorothy by name, Babbo "kendama" when cross. Honest, hot-headed, never gives up |
| バッボ | Babbo | living Weapon ÄRM, round with a moustache (looks like a kendama ball); amnesiac; once Phantom's ÄRM | Pompous old gentleman: ワシ, じゃ/のう, ぶれいもの "insolent!", calls Ginta 小僧 "boy" and his 家来 "servant", Jack サル "monkey", Dorothy ブス/バカ女; insists he is a 紳士 "gentleman" and not an object |
| ジャック | Jack | farm boy, Ginta's first friend; Earth ÄRM, shovel from his late father | オイラ, ends sentences with っス/スよ (rustic, deferential "-ssu"): give him a consistent folksy tic; calls his mum 母ちゃん "Ma"; was a coward, becomes brave |
| ジャックの母 | Jack's Mom | farmer, widow | Warm, scolding, old-fashioned: およし, たんとお食べ; calls Ginta ギンタちゃん |
| ドロシー | Dorothy | witch from Caldia, notorious ÄRM thief/collector; Zephyrus Broom, Ring Armor | Flirty, cocky, ♥ everywhere; calls Ginta ボウヤ "kiddo" at first, then ギンタン "Gintan"; わたし/あたし; jealous of Snow; scared of ghosts; sulks |
| スノウ | Snow | Princess of Lestava; ice ÄRM; healer; Koyuki's double | Gentle, cheerful, わたし, ♥; calls Babbo バッボさん; can be firm ("I hate you!") |
| 小雪 | Koyuki | Ginta's childhood friend in Tokyo (OPEN only) | Teasing, kind |
| エド / エドワード | Ed / Edward | Snow's loyal retainer, a dog | Archaic, very polite knight-retainer: ですかな, ありませぬぞ, かたじけない, ギンタどの "Ginta-dono", ひめさま "Princess"; cries easily (ワダクシ sob joke) |
| アラン (label エド) | Alan | the man sharing Ed's body; ex-Cross Guard No. 2, "Alan the Mighty"; sealed Babbo | Gruff: オレ, てめぇ, ガキども "brats", ボウズ "kid"; calls Dorothy クソ魔女 "damn witch", Halloween トマトやろう |
| アルヴィス | Alviss | ex-Cross Guard youth; summoned Ginta; Darkness ÄRM user | Cool, curt, condescending to Ginta (キミ/おまえ "you"); polite to Alan (アランさん, ぼく) |
| ナナシ | Nanashi | boss of the thieves' guild Luberia; lightning ÄRM Electric Eye; Andata | Kansai dialect (ワイ, や, へん, あかん, で, まかしとき); uses 自分/じぶん to mean "I/me"; womaniser (ドロシーちゃん, カワイコチャン); a comic but capable big brother |
| 彫金師ベリーニ | Bellini (the Engraver) | apprentice engraver girl hidden in the dungeon space | Ends sentences with ですのん/のん; blunt and touchy ("I'll punch you, nonn"). Needs an English verbal tic |
| マール | Marl | boy "ruin researcher"; actually a Chess Piece (see twists) | Before: timid, polite ボク, です/ます. After: smug, オレ, "I like things tidy". Defeated: sobbing child. Alan calls him ちびメガネ "four-eyed shrimp" |
| トム | Tom | Vestry boy who guides Ginta in the lake | Shy, friendly; speaks of Vestry in the past tense |
| イアン | Ian | Chess Piece (Rook); rival of Ginta | Breezy, cocky: オレっち, だよーん, ♪; calls Alan 犬のおじさん "doggy mister"; calls Loco ロコちゃん |
| ロコ | Loco | Chess Piece, small girl, older than she looks | Polite ですます, cool; "please stop calling me -chan" |
| ギド | Gido | Chess Piece with Ian | Polite to Ian |
| ハロウィン | Halloween | senior Chess Piece, pumpkin head; knows Alan | Laughs ひゅはははは, says "YES!" in English, マジ? "Seriously?" |
| ペタ | Peta | Phantom's right hand | Cold, grandiose proclamations |
| ファントム | Phantom | leader/commander of the Chess Pieces; revived | Only quoted |
| オルコ | Orco | Chess Piece at Vestry, Stone Body; dim | Broken words, colour-coded stutter, おれ |
| ギロム | Girom | Chess Piece at Vestry, "killing specialist" | Thug: てめぇ, ぶっころす, バーーーカ |
| ルーガ / ガルー | Luga / Garu | werewolf thief brothers; together "Loup-Garou" | Rough bullies |
| ブモル | Bumol | Training Gate guide (old man) | ぢゃ old-man speech, grumpy |
| メリロ | Merillo | Training Gate guide | Polite, sweet ♥ |
| 門ばんピエロ | Gatekeeper Clown | the summoning Dimension ÄRM | Sing-song katakana-mixed speech ("カイツウでーーース♪"): quirky capitals or stretched vowels |
| 親岩 / 子岩 | Papa Rock / Little Rock | talking rocks, father and son | Papa: polite old-fashioned ですな, calls Ginta ボッチャン "young sir"; Little Rock echoes the end of his father's lines |
| 占い師 | Fortune-teller | Lestava castle seer (quoted) | Prophetic, formal |
| ゆうれい, －－－ | Ghost; unseen voice | trapped spirits in the lake; also the Cross Guard radio voices | Faint, pleading / panicked |
| 先生, クラスメート | Teacher, Classmate | OPEN | Teacher: gruff gym-teacher yelling |
| 村の人, 街の人, 店主, shops | villagers etc. | NPCs | Shopkeepers each have a quirk: Magic Stone dealer stretches syllables (くっださい, かっしら), item dealer is a brisk "らっしゃい!", street vendor gruff |

## Relationships
- Ginta and Babbo: bickering master/"servant" who are really best friends ("Babbo is my friend!").
- Ginta and Jack: first friend; Jack looks up to him. Jack's late father; his mother lets him go.
- Dorothy loves Ginta (one-sided, loud); Ginta likes Snow, who resembles Koyuki; Dorothy and Snow are rivals, but
  Snow defends Dorothy when Ginta insults her.
- Ed (dog) and Snow: devoted retainer and princess. Alan and Alviss: old Cross Guard comrades. Alan was second to
  Danna, the previous otherworlder; he sees Danna in Ginta.
- Ian sees Ginta as his rival. Marl idolises Phantom.

## Twists and late reveals (do not hint earlier than the game does)
1. Alviss is the summoner (opening voice, "?" lines): revealed EV_AL02B.
2. Babbo was Phantom's ÄRM: told in EV_AL02B; Babbo denies it, has amnesia, and others note a "different
   personality" (EV_AL03, EV_ICE09). The game never says more; don't invent.
3. Ed is two people: Alan appears in EV_ICE10. Before that, keep Ed's sleep counting and "the other me inside me"
   (EV_ICE07) mysterious. The speaker label stays エド for both; consider the label "Ed" throughout.
4. Snow is the princess and Koyuki's double (EV_ICE09). Who the "new queen" is is never named here: say "queen".
5. Phantom has returned (EV_ICE12, G_EV021).
6. Marl is a Chess Piece (EV_T3KIL). Before it his asides are only (へへ), (くくく): keep them small and sly, and
   Dorothy's/Snow's warnings vague ("a nasty feeling").
7. Implied only: Tom says he *used to* live in Vestry and vanishes after the ghosts are freed; he may be one of them.
   Keep his past tense, add nothing.
8. Manga facts the game does not reveal: Danna is Ginta's father (Alan only says Ginta has a "familiar scent",
   EV_ICE12); Alviss's "not much time left" (G_EV020C) is his curse. Do not spell either out.

## Recurring jokes and motifs
- Babbo the "gentleman" is called ugly (ブサイク) and a kendama; he won't be counted as an object (イッコ "one item").
- Ed must sleep three times, Alan only once; Alan watches everything "from inside the dog". Ed's tearful ワダクシ.
- Dorothy's ♥ "Gintan", her jealousy of Snow, her sulking, and flattery that works; Babbo's flattery that doesn't.
- Nanashi's Kansai patter and womanising; his useless drawing for his men; his "Chou Kinshi" misreading of
  彫金師 (ちょう・きんし, sounds like "super-forbidden"): needs an English pun on "engraver".
- Bellini's ですのん, which makes everyone dizzy (の、のん?).
- Papa Rock and Dorothy: in D_VS_R (Dorothy in the party) he blurts "ド…!!" (start of "Dorothy!") and covers it
  with weather small talk that starts with ド (ドッチ, ドウキ, ドコ). An English version needs "Dor-..." starts.
- Ginta's dream counter (102 times, today 103), "Holy Thunder Force", eating ÄRM vegetables, "crystal snot".
- Field actions per hero (OBJ_*): Ginta smashes boulders with Babbo ("Me again!?"), Jack digs, Snow melts ice,
  Dorothy dispels magic walls, Alviss fills holes.
