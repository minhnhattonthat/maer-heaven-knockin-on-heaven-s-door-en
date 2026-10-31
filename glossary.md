# Glossary - MÄR Heaven: Knockin' on Heaven's Door

Binding for every translator and reviewer. Agents propose additions in reports; only the controller edits this file.
`tools/batches.py check` enforces every row whose English starts with a capital letter (or Ä) and whose notes don't
say `loose`: when the JP term is in a line, its English form (any of the `/`-separated forms) must be in the English.

## Rulings (asked of the user once; options and reasons in docs/decisions.md)
- Honorifics: kept, hyphenated (Ginta-kun, Jack-chan, Alan-san, Ginta-dono, -sama). Name order: Western.
- Romanisation source: official English (Viz manga / English anime "MÄR"), else an earlier fan patch, else Hepburn without macrons.
- Credits: English.
- Register: upbeat kid-friendly shonen, American spelling (savior, color), simple lively words (the Japanese is kana
  for children). Sound effects: as plain interjections in the line (*Bam!* style only if the Japanese is a pure SFX box).
- Abbreviations: full names and terms everywhere, prefer engine changes over shortening.
- Speaker labels: `[Name]` in the label colour (`tools/batches.py labels` fills them from the Characters table).

## Style rules
- Punctuation map: 「」 -> "...", 『』 -> '...', ・・・/… -> ..., ！？ -> !?, ～ -> ~ or dropped, ♥ kept.
- ÄRM always with the umlaut (also inside ÄRM names: Hammer ÄRM); MÄR Heaven; the team name メル -> MÄR.
- Voices: docs/style-reference.md.
- Name suffixes on ÄRM: ＣＬn -> " CLn", ＳＰ -> " SP" (part of the name, not abbreviations of ours: the game prints them).

## Characters
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ギンタ | Ginta |  | protagonist; full name Ginta Toramizu |  |
| 虎水ギンタ | Ginta Toramizu |  | EV_GO07; Western order |  |
| バッボ | Babbo |  | living Weapon ÄRM; official |  |
| ジャック | Jack |  | official; っス speech tic |  |
| ジャックの母 | Jack's Mom |  | speaker label; Jack calls her 母ちゃん "Ma" |  |
| ドロシー | Dorothy |  | official |  |
| ギンタン | Gintan |  | Dorothy's pet name for Ginta (official manga form); not an honorific, no hyphen |  |
| スノウ | Snow |  | official |  |
| スノウひめ | Princess Snow |  | EV_ICE09 |  |
| 小雪 | Koyuki |  | official; Ginta's friend in Tokyo |  |
| エド | Ed |  | speaker label for both the dog Ed and Alan (game keeps one label); see synopsis twist 3 |  |
| エドワード | Edward |  | official |  |
| アラン | Alan |  | official; revealed EV_ICE10 |  |
| ごうけつアラン | Alan the Mighty |  | G_EV021 epithet (豪傑); UNSURE |  |
| アルヴィス | Alviss |  | official |  |
| ナナシ | Nanashi |  | official; Kansai dialect |  |
| マール | Marl |  | game-original villain; UNSURE (Mahl/Maal possible; avoid "Mar" clash with MÄR) |  |
| 彫金師ベリーニ | Engraver Bellini |  | speaker label (16 chars); UNSURE: Bellini vs Berini; or label just "Bellini" |  |
| 彫金師 | Engraver |  | loose; speaker label before her name is given (L11_0_2); also the job (Items/terms) |  |
| ベリーニ | Bellini |  | game-original; UNSURE (Hepburn Berini) |  |
| イアン | Ian |  | official; Chess Piece (Rook) |  |
| ロコ | Loco |  | official |  |
| ギド | Gido |  | official |  |
| ハロウィン | Halloween |  | official |  |
| ペタ | Peta |  | official |  |
| ファントム | Phantom |  | official; Chess Pieces' leader |  |
| オルコ | Orco |  | Vestry Chess Piece; UNSURE spelling |  |
| ギロム | Girom |  | Vestry Chess Piece; UNSURE (Gyrom/Gillom) |  |
| ルーガ | Luga |  | werewolf thief; UNSURE; Luga+Garu = Loup-Garou pun |  |
| ガルー | Garu |  | werewolf thief; UNSURE |  |
| ルーガ＆ガルー | Luga & Garu |  | speaker label |  |
| ルーガルー | Loup-Garou |  | the brothers' gang name (French werewolf); EV_JA01/EV_JA04 |  |
| ルーガルーブラザーズ | Loup-Garou Brothers |  | EV_JA01 |  |
| トム | Tom |  | Vestry boy; see synopsis twist 7 |  |
| ダンナ | Danna |  | the previous otherworlder, Cross Guard leader; official name (also means "boss"); do not reveal he is Ginta's father |  |
| 王妃 | the Queen |  | loose; Snow's stepmother, never named in game; keep unnamed |  |
| ブモル | Bumol |  | Training Gate guide; official-ish; UNSURE |  |
| メリロ | Merillo |  | Training Gate guide; UNSURE (Merilo) |  |
| 門ばんピエロ | Gatekeeper Clown |  | speaker label and Dimension ÄRM; official |  |
| 親岩 | Papa Rock |  | talking rock (father); UNSURE (Father Rock) |  |
| 子岩 | Little Rock |  | talking rock (son) |  |
| 岩の親子 | the rock father and son |  | loose; EV_RT03 |  |
| 占い師 | Fortune-teller |  | loose; Lestava castle seer |  |
| ゆうれい | Ghost |  | loose; trapped spirit (EV_GO11) |  |
| 先生 | Teacher |  | loose; OPEN |  |
| クラスメート | Classmate |  | loose; OPEN; several speakers |  |
| ギンタ＆ドロシー | Ginta & Dorothy |  | speaker label |  |
| バッボ＆ジャック | Babbo & Jack |  | speaker label |  |
| 村の人 | Villager |  | loose; Vestry |  |
| 村の女の子 | Village Girl |  | loose; EV_UTA01 |  |
| 女の子 | Little Girl |  | loose; CH_M11 (crying child) |  |
| 街の人 | Townsperson |  | loose; Paz Town / Pelica |  |
| 店主 | Shopkeeper |  | loose; CH_M09A market stall owner |  |
| ÄＲＭ屋 | ÄRM Dealer |  | loose; shops and CH_M09A |  |
| マジックストーン屋 | Magic Stone Dealer |  | loose; 18 chars; check name box |  |
| 道具屋 | Item Dealer |  | loose; SHOPPA03 |  |
| 宿屋 | Innkeeper |  | loose; SHOPPA04 |  |
| 露天 | Street Vendor |  | loose; SHOPPA05 (露天 is the game's typo for 露店) |  |
| 手下 | Henchman |  | loose; Luberia thieves |  |
| 手下１ | Henchman 1 |  | loose; G_EV060 |  |
| 手下２ | Henchman 2 |  | loose; G_EV060 |  |
| おやぶん | Thief Boss |  | loose; EV_AL02 (Babbo thieves) |  |
| こぶん | Thief Lackey |  | loose; EV_AL02 |  |
| ？？？ | ??? |  | loose; unknown speaker; keep |  |
| －－－ | --- |  | loose; unseen voice (ghost EV_GO10, Cross Guard radio G_EV021); keep as dashes |  |
| ひめさま | Princess |  | Ed/Alan to Snow; "Your Highness" in direct address where natural |  |
| ボウヤ | kiddo |  | Dorothy to Ginta early on |  |
| ボッチャン | young sir |  | Papa Rock to Ginta; UNSURE (sonny) |  |
| ボウズ | kid |  | Alan to Ginta |  |
| 小僧 | boy |  | Babbo, Halloween (コゾウ) |  |
| 家来 | servant |  | Babbo calls Ginta his servant |  |

## Places
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| メルヘヴン | MÄR Heaven |  | official |  |
| パヅタウン | Paz Town |  | UNSURE (Pazu Town); market town near Jack's farm |  |
| パヅリカ | Pazurica |  | island of Paz Town, ice castle, Pelica (G_EV011); UNSURE |  |
| ペリカ | Pelica |  | town (debug menu name only, not in dialogue); UNSURE |  |
| レスターヴァ | Lestava |  | official; Snow's kingdom |  |
| カルデア | Caldia |  | official; the witches' islands |  |
| ヒルドたいりく | Hildo Continent |  | UNSURE spelling; Luberia and Vestry are here |  |
| ルベリア | Luberia |  | Nanashi's thieves' guild and hideout; UNSURE (Rubelia, Lubelia) |  |
| ヴェストリ | Vestry |  | official; "village of water and woods" |  |
| ちていこ | underground lake |  | 地底湖, by Vestry |  |
| 氷の城 | Ice Castle |  | Snow's frozen castle |  |
| 修練の門 | Training Gate |  | Dimension ÄRM / Dungeon Mode gate 1; official |  |
| 練磨の門 | Honing Gate |  | Dungeon Mode gate 2 (G_EV050); game-original; UNSURE |  |
| 鍛錬の門 | Tempering Gate |  | Dungeon Mode gate 3 (G_EV061); UNSURE |  |
| 練武の門 | Martial Gate |  | Dungeon Mode gate 4 (G_EV062); UNSURE |  |
| 最後の門 | Final Gate |  | Dungeon Mode gate 5 (DUNG_END) |  |
| 日本 | Japan |  | - |  |
| 東京 | Tokyo |  | - |  |
| いせかい | other world |  | 異界/いせかい; Ginta's world seen from MÄR Heaven |  |
| 異界の住人 | dweller of another world |  | OPEN; いかいの住人 Halloween; "otherworlder" in casual lines |  |

## Items/terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| ÄＲＭ | ÄRM |  | always with umlaut |  |
| あーむ | arm |  | EV_RT03 Ginta doesn't know the word; lowercase 'arm' in quotes |  |
| ÄＲＭつかい | ÄRM user |  | - |  |
| 魔力 | magic power |  | official; furigana まりょく |  |
| 魔女 | witch |  | - |  |
| 魔物 | monster |  | - |  |
| 魔法 | magic |  | - |  |
| まほうじん | magic circle |  | OBJ_D |  |
| まほうのかべ | magic wall |  | OBJ_D, SP_M26_5 |  |
| チェスの兵隊 | Chess Pieces |  | official; read チェスのコマ (EV_AL02B pun on reading) |  |
| チェス | Chess / the Chess |  | loose; short form; "the Chess" or "Chess Pieces" as fits |  |
| チェスのコマ | Chess Pieces |  | Orco's/Ginta's spelling of the same name |  |
| ポーン | Pawn |  | loose; Chess ranks (G_EV023) |  |
| ルーク | Rook |  | loose; - |  |
| ビショップ | Bishop |  | loose; - |  |
| ナイト | Knight |  | loose; - |  |
| しれいとう | commander |  | Phantom; 司令塔 |  |
| クロスガード | Cross Guard |  | official |  |
| クロスガード軍 | Cross Guard army |  | - |  |
| メル | MÄR |  | loose; team name; Ginta: "the eight warriors who save MÄR Heaven" -> MÄR |  |
| 八戦士 | eight warriors |  | G_EV025B |  |
| 七人のゆうしゃ | seven heroes |  | prophecy |  |
| 救世主 | savior |  | UNSURE spelling: saviour vs savior (pick one house style) |  |
| ガーディアンÄＲＭ | Guardian ÄRM |  | official class |  |
| ディメンションÄＲＭ | Dimension ÄRM |  | official class |  |
| ウェポンÄＲＭ | Weapon ÄRM |  | official class |  |
| ネイチャーÄＲＭ | Nature ÄRM |  | official class |  |
| ダークネスÄＲＭ | Darkness ÄRM |  | official class |  |
| マジックストーン | Magic Stone |  | - |  |
| デッキ | deck |  | capitalise as menu item "Deck" |  |
| デッキエディット | Deck Edit |  | menu command |  |
| コマンド | Command |  | loose; START menu |  |
| ステータス | Status |  | loose; - |  |
| セーブ | Save |  | loose; - |  |
| シンクロ | synchro |  | sync with an ÄRM |  |
| シンクロゲージ | Synchro Gauge |  | - |  |
| バトル | battle |  | - |  |
| パーティー | party |  | - |  |
| パーティーへんこう | Party Change |  | command (G_EV062) |  |
| 先頭 | lead |  | party leader on the field (SP_M42) |  |
| ダンジョン | dungeon |  | - |  |
| ダンジョンモード | Dungeon Mode |  | - |  |
| 対戦モード | Versus Mode |  | - |  |
| ゲームモード | game mode |  | - |  |
| フロア | floor |  | - |  |
| ゴール | goal |  | loose; Training Gate |  |
| スタートボタン | START Button |  | - |  |
| セレクトボタン | SELECT Button |  | - |  |
| Ａボタン | A Button |  | A for ÄRM |  |
| Ｂボタン | B Button |  | B for Babbo |  |
| Ｌボタン / Ｒボタン | L Button / R Button |  | - |  |
| Ｐ | P |  | loose; currency suffix (100 P) |  |
| ピューター | Pewter |  | currency name (SHOPPA04); UNSURE |  |
| 彫金 | engraving |  | making ÄRM; furigana ちょうきん |  |
| レシピ | recipe |  | - |  |
| 暗号 | code |  | recipe codes |  |
| 材料 | material |  | - |  |
| 封印 | seal |  | - |  |
| 宝ばこ | treasure chest |  | - |  |
| とうぞく | thief / thieves |  | 盗賊 |  |
| とうぞくギルド | thieves' guild |  | Luberia |  |
| 人狼 | werewolf |  | - |  |
| ゆうれい / ぼうれい | ghost / spirit |  | - |  |
| タロス | Talos |  | giant Guardian ÄRM in 3 parts |  |
| うで / あし / あたま | arms / legs / head |  | Talos parts; UNSURE: "arms" sits next to ÄRM; debug labels say hand/foot/head |  |
| 古代の秘術 | ancient secret art |  | - |  |
| 古文書 | ancient document |  | - |  |
| もんしょう | crest |  | - |  |
| 遺跡 | ruins |  | - |  |
| ホーリーサンダーフォース | Holy Thunder Force |  | Ginta's daydream holy sword (OPEN) |  |
| 聖剣 | holy sword |  | - |  |
| クリスタルはなみず | crystal snot |  | EV_ICE07 joke |  |
| ケン玉 | kendama |  | Ginta's insult for Babbo (he looks like the ball); UNSURE: "you yo-yo" if kendama too obscure |  |
| 紳士 | gentleman |  | Babbo's self-image |  |
| ぶれいもの | insolent fool |  | Babbo's catchphrase |  |
| シックスセンス | sixth sense |  | - |  |
| とっくん | training |  | CH_M05A |  |
| 修行 | training |  | - |  |
| ＥＭＰＴＹ | Empty |  | empty-slot placeholder |  |
| バッボ | Babbo |  | Ginta's living Weapon ÄRM (official) |  |
| バトルスコップ | Battle Shovel |  | Jack's weapon; スコップ = shovel (his father's, EV_MON04). UNSURE: some fan sources say 'Battle Scoop' |  |
| アースウェイブ | Earth Wave |  | Jack |  |
| アースビーンズ | Earth Beans |  | Jack |  |
| マジカルマッシュルーム | Magical Mushroom |  | Jack |  |
| ラフレシア | Rafflesia |  | Jack's Guardian; given by his mother (J_VS_M) |  |
| アースマグマ | Earth Magma |  | Jack |  |
| ドリアンシュート | Durian Shoot |  | Jack |  |
| ブーメランスコップ | Boomerang Shovel |  | Jack; shovel family |  |
| ドリルスコップ | Drill Shovel |  | Jack; shovel family |  |
| ドリルスコップ　ＳＰ | Drill Shovel SP |  | suffix rule: fullwidth space + ＳＰ -> " SP" |  |
| アイスリング | Ice Ring |  | Snow |  |
| スノーマンガード　ＣＬ２ | Snowman Guard CL2 |  | suffix rule: fullwidth space + ＣＬn -> " CLn" (class level, kept abbreviated like the original) |  |
| スノーマンガード　ＣＬ３ | Snowman Guard CL3 |  | - |  |
| スノーマンアタック　ＣＬ１ | Snowman Attack CL1 |  | Snow |  |
| スノーマンアタック　ＣＬ２ | Snowman Attack CL2 |  | - |  |
| スノーマンアタック　ＣＬ３ | Snowman Attack CL3 |  | - |  |
| スノーマンアタック　ＣＬ４ | Snowman Attack CL4 |  | - |  |
| スノーマンアタック　ＣＬ５ | Snowman Attack CL5 |  | - |  |
| スノーマンアタック　ＳＰ | Snowman Attack SP |  | - |  |
| １３トーテムポールチェーン | 13 Totem Pole Chain |  | Alviss's 13 Totem Pole (official); 'Chain' kept from JP |  |
| １３トーテムポールチェーン　ＳＰ | 13 Totem Pole Chain SP |  | 22 chars, longest-but-one: check 112 px |  |
| ゼピュロスブルーム | Zephyrus Broom |  | Dorothy's broom (official) |  |
| リングアーマー　ＣＬ１ | Ring Armor CL1 |  | Dorothy's Guardian (EV_RT03) |  |
| リングアーマー　ＣＬ２ | Ring Armor CL2 |  | - |  |
| リングアーマー　ＣＬ３ | Ring Armor CL3 |  | - |  |
| リングアーマー　ＣＬ４ | Ring Armor CL4 |  | - |  |
| リングダガー | Ring Dagger |  | - |  |
| リングナイフ | Ring Knife |  | - |  |
| リングフルーレ | Ring Foil |  | フルーレ = fencing foil (fleuret) |  |
| リングソード | Ring Sword |  | - |  |
| リングダブルソード | Ring Double Sword |  | - |  |
| フライングレオ | Flying Leo |  | Dorothy (official) |  |
| ブリキン　ＣＬ２ | Brikin CL2 |  | Dorothy Guardian; ブリキ = tin (Tin Man nod). UNSURE: official spelling |  |
| ブリキン　ＣＬ３ | Brikin CL3 |  | - |  |
| マジックミラーリング | Magic Mirror Ring |  | - |  |
| ５ダガーブレスレット | 5 Dagger Bracelet |  | - |  |
| １０ダガーブレスレット | 10 Dagger Bracelet |  | - |  |
| ２０ダガーブレスレット | 20 Dagger Bracelet |  | - |  |
| ネックレスブレード | Necklace Blade |  | - |  |
| カゴの鳥 | Bird Cage |  | Alviss's Darkness ÄRM, turns Jack into a caged bird (EV_AL02). UNSURE: 'Caged Bird' |  |
| パイソンウィップ | Python Whip |  | - |  |
| メルトアイス | Melt Ice |  | fire ÄRM Alan gives to free Snow (EV_ICE11) |  |
| 修練の門 | Training Gate |  | Dimension ÄRM (official Training Gate) |  |
| メリロさん | Merillo-san |  | Training Gate guide as an ÄRM; honorific kept |  |
| ブモルさん | Bumol-san |  | Training Gate guide as an ÄRM; honorific kept |  |
| エアハンマー | Air Hammer |  | - |  |
| エアハンマー　ＳＰ | Air Hammer SP |  | - |  |
| オクトパス | Octopus |  | - |  |
| 癒しの天使　ＣＬ１ | Healing Angel CL1 |  | official |  |
| 癒しの天使　ＣＬ２ | Healing Angel CL2 |  | - |  |
| 癒しの天使　ＣＬ３ | Healing Angel CL3 |  | Ian's trade (G_EV025) |  |
| 癒しの天使　ＣＬ５ | Healing Angel CL5 |  | - |  |
| マジックカーペット | Magic Carpet |  | Ed's travel Dimension ÄRM (G_EV030) |  |
| アンダータ | Andata |  | Nanashi's Dimension ÄRM (official) |  |
| ストーンボディ　ＣＬ１ | Stone Body CL1 |  | Orco's hardening ÄRM |  |
| ストーンボディ　ＣＬ２ | Stone Body CL2 |  | - |  |
| ストーンボディ　ＣＬ３ | Stone Body CL3 |  | - |  |
| ストーンボディ　ＣＬ５ | Stone Body CL5 |  | - |  |
| エレクトリック・アイ　ＣＬ２ | Electric Eye CL2 |  | Nanashi's lightning Nature ÄRM (official) |  |
| エレクトリック・アイ　ＣＬ３ | Electric Eye CL3 |  | - |  |
| エレクトリック・アイ　ＣＬ４ | Electric Eye CL4 |  | - |  |
| エレクトリック・アイ　ＳＰ | Electric Eye SP |  | - |  |
| アイスドアース　ＣＬ２ | Iced Earth CL2 |  | - |  |
| アイスドアース　ＣＬ３ | Iced Earth CL3 |  | - |  |
| アイスドアース　ＣＬ４ | Iced Earth CL4 |  | - |  |
| フレイムボール　ＣＬ２ | Flame Ball CL2 |  | - |  |
| フレイムボール　ＣＬ３ | Flame Ball CL3 |  | - |  |
| フレイムボール　ＣＬ４ | Flame Ball CL4 |  | - |  |
| パワーリング　ＣＬ１ | Power Ring CL1 |  | - |  |
| パワーリング　ＣＬ２ | Power Ring CL2 |  | - |  |
| パワーリング　ＣＬ３ | Power Ring CL3 |  | - |  |
| パワーリング　ＣＬ４ | Power Ring CL4 |  | - |  |
| ヴィンダールブ　ＣＬ３ | Vindalf CL3 |  | Norse dwarf name (Vindalfr), like Vestry. UNSURE |  |
| ヴィンダールブ　ＣＬ４ | Vindalf CL4 |  | - |  |
| ヴィンダールブ　ＣＬ５ | Vindalf CL5 |  | - |  |
| ジッパー | Zipper |  | gift from Papa Rock (D_VS_R) |  |
| レインドッグ | Rain Dog |  | gift from Papa Rock (D_VS_R) |  |
| レインドッグ　ＳＰ | Rain Dog SP |  | - |  |
| スクリューサーベル | Screw Saber |  | - |  |
| ストーンキューブ　ＣＬ２ | Stone Cube CL2 |  | - |  |
| ストーンキューブ　ＣＬ３ | Stone Cube CL3 |  | - |  |
| ストーンキューブ　ＣＬ４ | Stone Cube CL4 |  | - |  |
| ストーンキューブ　ＣＬ５ | Stone Cube CL5 |  | - |  |
| シャドーマン | Shadow Man |  | - |  |
| ナイフリング | Knife Ring |  | weapon-ring family: [Element] Knife/Club/Sword/Axe/Katana Ring |  |
| クラブリング | Club Ring |  | - |  |
| ソードリング | Sword Ring |  | - |  |
| アックスリング | Axe Ring |  | - |  |
| カタナリング | Katana Ring |  | - |  |
| ウォーターナイフリング | Water Knife Ring |  | elements: ウォーター Water, ファイア Fire, リーフ Leaf, ウィンド Wind, アース Earth, サンダー Thunder |  |
| ウォータークラブリング | Water Club Ring |  | - |  |
| ウォーターソードリング | Water Sword Ring |  | - |  |
| ウォーターアックスリング | Water Axe Ring |  | - |  |
| ウォーターカタナリング | Water Katana Ring |  | - |  |
| ファイアナイフリング | Fire Knife Ring |  | - |  |
| ファイアクラブリング | Fire Club Ring |  | - |  |
| ファイアソードリング | Fire Sword Ring |  | - |  |
| ファイアアックスリング | Fire Axe Ring |  | - |  |
| ファイアカタナリング | Fire Katana Ring |  | - |  |
| リーフナイフリング | Leaf Knife Ring |  | - |  |
| リーフクラブリング | Leaf Club Ring |  | - |  |
| リーフソードリング | Leaf Sword Ring |  | - |  |
| リーフアックスリング | Leaf Axe Ring |  | - |  |
| リーフカタナリング | Leaf Katana Ring |  | - |  |
| ウィンドナイフリング | Wind Knife Ring |  | - |  |
| ウィンドクラブリング | Wind Club Ring |  | - |  |
| ウィンドソードリング | Wind Sword Ring |  | - |  |
| ウィンドアックスリング | Wind Axe Ring |  | - |  |
| ウィンドカタナリング | Wind Katana Ring |  | - |  |
| アースナイフリング | Earth Knife Ring |  | - |  |
| アースクラブリング | Earth Club Ring |  | - |  |
| アースソードリング | Earth Sword Ring |  | - |  |
| アースアックスリング | Earth Axe Ring |  | - |  |
| アースカタナリング | Earth Katana Ring |  | - |  |
| サンダーナイフリング | Thunder Knife Ring |  | - |  |
| サンダークラブリング | Thunder Club Ring |  | - |  |
| サンダーソードリング | Thunder Sword Ring |  | - |  |
| サンダーアックスリング | Thunder Axe Ring |  | - |  |
| サンダーカタナリング | Thunder Katana Ring |  | - |  |
| ウォーターパワー　ＣＬ１ | Water Power CL1 |  | - |  |
| ウォーターパワー　ＣＬ２ | Water Power CL2 |  | - |  |
| ウォーターパワー　ＣＬ３ | Water Power CL3 |  | - |  |
| ウォーターパワー　ＣＬ４ | Water Power CL4 |  | - |  |
| ウォーターパワー　ＣＬ５ | Water Power CL5 |  | - |  |
| ファイアパワー　ＣＬ１ | Fire Power CL1 |  | - |  |
| ファイアパワー　ＣＬ２ | Fire Power CL2 |  | - |  |
| ファイアパワー　ＣＬ３ | Fire Power CL3 |  | - |  |
| ファイアパワー　ＣＬ４ | Fire Power CL4 |  | - |  |
| ファイアパワー　ＣＬ５ | Fire Power CL5 |  | - |  |
| リーフパワー　ＣＬ１ | Leaf Power CL1 |  | - |  |
| リーフパワー　ＣＬ２ | Leaf Power CL2 |  | - |  |
| リーフパワー　ＣＬ３ | Leaf Power CL3 |  | - |  |
| リーフパワー　ＣＬ４ | Leaf Power CL4 |  | - |  |
| リーフパワー　ＣＬ５ | Leaf Power CL5 |  | - |  |
| ウィンドパワー　ＣＬ１ | Wind Power CL1 |  | - |  |
| ウィンドパワー　ＣＬ２ | Wind Power CL2 |  | - |  |
| ウィンドパワー　ＣＬ３ | Wind Power CL3 |  | - |  |
| ウィンドパワー　ＣＬ４ | Wind Power CL4 |  | - |  |
| ウィンドパワー　ＣＬ５ | Wind Power CL5 |  | - |  |
| アースパワー　ＣＬ１ | Earth Power CL1 |  | - |  |
| アースパワー　ＣＬ２ | Earth Power CL2 |  | - |  |
| アースパワー　ＣＬ３ | Earth Power CL3 |  | - |  |
| アースパワー　ＣＬ４ | Earth Power CL4 |  | - |  |
| アースパワー　ＣＬ５ | Earth Power CL5 |  | - |  |
| サンダーパワー　ＣＬ１ | Thunder Power CL1 |  | - |  |
| サンダーパワー　ＣＬ２ | Thunder Power CL2 |  | - |  |
| サンダーパワー　ＣＬ３ | Thunder Power CL3 |  | - |  |
| サンダーパワー　ＣＬ４ | Thunder Power CL4 |  | - |  |
| サンダーパワー　ＣＬ５ | Thunder Power CL5 |  | - |  |
| ウォーターコート　ＣＬ１ | Water Coat CL1 |  | - |  |
| ウォーターコート　ＣＬ２ | Water Coat CL2 |  | - |  |
| ウォーターコート　ＣＬ３ | Water Coat CL3 |  | - |  |
| ウォーターコート　ＣＬ４ | Water Coat CL4 |  | - |  |
| ウォーターコート　ＣＬ５ | Water Coat CL5 |  | - |  |
| ファイアコート　ＣＬ１ | Fire Coat CL1 |  | - |  |
| ファイアコート　ＣＬ２ | Fire Coat CL2 |  | - |  |
| ファイアコート　ＣＬ３ | Fire Coat CL3 |  | - |  |
| ファイアコート　ＣＬ４ | Fire Coat CL4 |  | - |  |
| ファイアコート　ＣＬ５ | Fire Coat CL5 |  | - |  |
| リーフコート　ＣＬ１ | Leaf Coat CL1 |  | - |  |
| リーフコート　ＣＬ２ | Leaf Coat CL2 |  | - |  |
| リーフコート　ＣＬ３ | Leaf Coat CL3 |  | - |  |
| リーフコート　ＣＬ４ | Leaf Coat CL4 |  | - |  |
| リーフコート　ＣＬ５ | Leaf Coat CL5 |  | - |  |
| ウィンドコート　ＣＬ１ | Wind Coat CL1 |  | - |  |
| ウィンドコート　ＣＬ２ | Wind Coat CL2 |  | - |  |
| ウィンドコート　ＣＬ３ | Wind Coat CL3 |  | - |  |
| ウィンドコート　ＣＬ４ | Wind Coat CL4 |  | - |  |
| ウィンドコート　ＣＬ５ | Wind Coat CL5 |  | - |  |
| アースコート　ＣＬ１ | Earth Coat CL1 |  | - |  |
| アースコート　ＣＬ２ | Earth Coat CL2 |  | - |  |
| アースコート　ＣＬ３ | Earth Coat CL3 |  | - |  |
| アースコート　ＣＬ４ | Earth Coat CL4 |  | - |  |
| アースコート　ＣＬ５ | Earth Coat CL5 |  | - |  |
| サンダーコート　ＣＬ１ | Thunder Coat CL1 |  | - |  |
| サンダーコート　ＣＬ２ | Thunder Coat CL2 |  | - |  |
| サンダーコート　ＣＬ３ | Thunder Coat CL3 |  | - |  |
| サンダーコート　ＣＬ４ | Thunder Coat CL4 |  | - |  |
| サンダーコート　ＣＬ５ | Thunder Coat CL5 |  | - |  |
| エスケイプ　ＣＬ２ | Escape CL2 |  | - |  |
| エスケイプ　ＣＬ３ | Escape CL3 |  | - |  |
| エスケイプ　ＣＬ４ | Escape CL4 |  | - |  |
| 天使の口づけ | Angel's Kiss |  | - |  |
| フェニックス | Phoenix |  | - |  |
| スリーピーリング　ＣＬ１ | Sleepy Ring CL1 |  | - |  |
| スリーピーリング　ＣＬ２ | Sleepy Ring CL2 |  | - |  |
| スリーピーリング　ＣＬ３ | Sleepy Ring CL3 |  | - |  |
| スリーピーリング　ＣＬ４ | Sleepy Ring CL4 |  | - |  |
| スリーピーリング　ＣＬ５ | Sleepy Ring CL5 |  | - |  |
| アームフリーズ　ＣＬ１ | ÄRM Freeze CL1 |  | アーム = ÄRM in katakana |  |
| アームフリーズ　ＣＬ２ | ÄRM Freeze CL2 |  | - |  |
| アームフリーズ　ＣＬ３ | ÄRM Freeze CL3 |  | - |  |
| アームフリーズ　ＣＬ４ | ÄRM Freeze CL4 |  | - |  |
| カウントダウン　ＣＬ１ | Countdown CL1 |  | - |  |
| カウントダウン　ＣＬ２ | Countdown CL2 |  | - |  |
| カウントダウン　ＣＬ３ | Countdown CL3 |  | - |  |
| カウントダウン　ＣＬ４ | Countdown CL4 |  | - |  |
| カウントダウン　ＣＬ５ | Countdown CL5 |  | - |  |
| デッキダウン　ＣＬ２ | Deck Down CL2 |  | - |  |
| デッキダウン　ＣＬ３ | Deck Down CL3 |  | - |  |
| デッキダウン　ＣＬ４ | Deck Down CL4 |  | - |  |
| デッキダウン　ＣＬ５ | Deck Down CL5 |  | - |  |
| ミノタウロ　ＣＬ２ | Minotaur CL2 |  | JP ミノタウロ (Minotauro); English form chosen |  |
| ミノタウロ　ＣＬ３ | Minotaur CL3 |  | - |  |
| ミノタウロ　ＣＬ４ | Minotaur CL4 |  | - |  |
| ミノタウロ　ＣＬ５ | Minotaur CL5 |  | - |  |
| サーペント　ＣＬ２ | Serpent CL2 |  | - |  |
| サーペント　ＣＬ３ | Serpent CL3 |  | - |  |
| サーペント　ＣＬ４ | Serpent CL4 |  | - |  |
| サーペント　ＣＬ５ | Serpent CL5 |  | - |  |
| サラマンダー　ＣＬ２ | Salamander CL2 |  | - |  |
| サラマンダー　ＣＬ３ | Salamander CL3 |  | - |  |
| サラマンダー　ＣＬ４ | Salamander CL4 |  | - |  |
| サラマンダー　ＣＬ５ | Salamander CL5 |  | - |  |
| トレント　ＣＬ２ | Treant CL2 |  | tree giant (RPG トレント) |  |
| トレント　ＣＬ３ | Treant CL3 |  | - |  |
| トレント　ＣＬ４ | Treant CL4 |  | - |  |
| トレント　ＣＬ５ | Treant CL5 |  | - |  |
| ジン　ＣＬ２ | Djinn CL2 |  | UNSURE: Jinn/Djinn/Genie; CL3 given by Jack's mother (J_VS_M) |  |
| ジン　ＣＬ３ | Djinn CL3 |  | - |  |
| ジン　ＣＬ４ | Djinn CL4 |  | - |  |
| ジン　ＣＬ５ | Djinn CL5 |  | - |  |
| クエイク　ＣＬ２ | Quake CL2 |  | - |  |
| クエイク　ＣＬ３ | Quake CL3 |  | - |  |
| クエイク　ＣＬ４ | Quake CL4 |  | - |  |
| クエイク　ＣＬ５ | Quake CL5 |  | - |  |
| インドラ　ＣＬ２ | Indra CL2 |  | - |  |
| インドラ　ＣＬ３ | Indra CL3 |  | - |  |
| インドラ　ＣＬ４ | Indra CL4 |  | - |  |
| インドラ　ＣＬ５ | Indra CL5 |  | - |  |
| アイス＆ウォーター　ＣＬ１ | Ice & Water CL1 |  | - |  |
| アイス＆ウォーター　ＣＬ２ | Ice & Water CL2 |  | - |  |
| アイス＆ウォーター　ＣＬ３ | Ice & Water CL3 |  | - |  |
| アイス＆ウォーター　ＣＬ４ | Ice & Water CL4 |  | - |  |
| アイス＆ウォーター　ＣＬ５ | Ice & Water CL5 |  | - |  |
| ファイアバーニング　ＣＬ１ | Fire Burning CL1 |  | - |  |
| ファイアバーニング　ＣＬ２ | Fire Burning CL2 |  | - |  |
| ファイアバーニング　ＣＬ３ | Fire Burning CL3 |  | - |  |
| ファイアバーニング　ＣＬ４ | Fire Burning CL4 |  | - |  |
| ファイアバーニング　ＣＬ５ | Fire Burning CL5 |  | - |  |
| プランツアタック　ＣＬ１ | Plants Attack CL1 |  | UNSURE: Plant Attack reads better |  |
| プランツアタック　ＣＬ２ | Plants Attack CL2 |  | - |  |
| プランツアタック　ＣＬ３ | Plants Attack CL3 |  | - |  |
| プランツアタック　ＣＬ４ | Plants Attack CL4 |  | - |  |
| プランツアタック　ＣＬ５ | Plants Attack CL5 |  | - |  |
| デンジャラスストーム　ＣＬ１ | Dangerous Storm CL1 |  | - |  |
| デンジャラスストーム　ＣＬ２ | Dangerous Storm CL2 |  | - |  |
| デンジャラスストーム　ＣＬ３ | Dangerous Storm CL3 |  | - |  |
| デンジャラスストーム　ＣＬ４ | Dangerous Storm CL4 |  | - |  |
| デンジャラスストーム　ＣＬ５ | Dangerous Storm CL5 |  | - |  |
| アースフォース　ＣＬ１ | Earth Force CL1 |  | - |  |
| アースフォース　ＣＬ２ | Earth Force CL2 |  | - |  |
| アースフォース　ＣＬ３ | Earth Force CL3 |  | - |  |
| アースフォース　ＣＬ４ | Earth Force CL4 |  | - |  |
| アースフォース　ＣＬ５ | Earth Force CL5 |  | - |  |
| ライトニングボルト　ＣＬ１ | Lightning Bolt CL1 |  | - |  |
| ライトニングボルト　ＣＬ２ | Lightning Bolt CL2 |  | - |  |
| ライトニングボルト　ＣＬ３ | Lightning Bolt CL3 |  | - |  |
| ライトニングボルト　ＣＬ４ | Lightning Bolt CL4 |  | - |  |
| ライトニングボルト　ＣＬ５ | Lightning Bolt CL5 |  | - |  |
| スキャンリング | Scan Ring |  | - |  |
| ストックリング | Stock Ring |  | - |  |
| シャッフルリング | Shuffle Ring |  | - |  |
| ダミー | Dummy |  | unused/placeholder entry? |  |
| ビッグバッボ | Big Babbo |  | - |  |
| ハンマーアーム | Hammer ÄRM |  | Babbo Version 1 as a Magic Stone; アーム = ÄRM (EV_MON02) |  |
| ダガーアーム | Dagger ÄRM |  | Magic Stone (EV_MON02); アーム = ÄRM |  |
| バブルランチャー | Bubble Launcher |  | Magic Stone (EV_MON02) |  |
| ガーゴイル　ＣＬ４ | Gargoyle CL4 |  | Ginta's Guardian (official) |  |
| ガーゴイル　ＣＬ５ | Gargoyle CL5 |  | - |  |
| ガーゴイル　ＳＰ | Gargoyle SP |  | - |  |
| アリス | Alice |  | Ginta's Holy ÄRM (official) |  |
| ガトリングバッボ | Gatling Babbo |  | Babbo Version 2 (official Gatling); gift from Papa Rock (G_VS_R) |  |
| アーマーストーン　ＣＬ１ | Armor Stone CL1 |  | - |  |
| アーマーストーン　ＣＬ２ | Armor Stone CL2 |  | - |  |
| ５ダガーストーン | 5 Dagger Stone |  | - |  |
| １０ダガーストーン | 10 Dagger Stone |  | - |  |
| ２０ダガーストーン | 20 Dagger Stone |  | - |  |
| ブレードストーン | Blade Stone |  | - |  |
| メルトアイスストーン | Melt Ice Stone |  | - |  |
| 癒しの天使石　ＣＬ１ | Healing Angel Stone CL1 |  | 石 = Stone (Magic Stone family); 23 chars, longest: check 112 px |  |
| 癒しの天使石　ＣＬ２ | Healing Angel Stone CL2 |  | - |  |
| パワーストーン　ＣＬ１ | Power Stone CL1 |  | - |  |
| パワーストーン　ＣＬ２ | Power Stone CL2 |  | - |  |
| パワーストーン　ＣＬ３ | Power Stone CL3 |  | - |  |
| ナイフストーン | Knife Stone |  | - |  |
| クラブストーン | Club Stone |  | - |  |
| ソードストーン | Sword Stone |  | - |  |
| アックスストーン | Axe Stone |  | - |  |
| カタナストーン | Katana Stone |  | - |  |
| ウォーターナイフストーン | Water Knife Stone |  | - |  |
| ウォータークラブストーン | Water Club Stone |  | - |  |
| ウォーターソードストーン | Water Sword Stone |  | - |  |
| ウォーターアックスストーン | Water Axe Stone |  | - |  |
| ウォーターカタナストーン | Water Katana Stone |  | - |  |
| ファイアナイフストーン | Fire Knife Stone |  | - |  |
| ファイアクラブストーン | Fire Club Stone |  | - |  |
| ファイアソードストーン | Fire Sword Stone |  | - |  |
| ファイアアックスストーン | Fire Axe Stone |  | - |  |
| ファイアカタナストーン | Fire Katana Stone |  | - |  |
| リーフナイフストーン | Leaf Knife Stone |  | - |  |
| リーフクラブストーン | Leaf Club Stone |  | - |  |
| リーフソードストーン | Leaf Sword Stone |  | - |  |
| リーフアックスストーン | Leaf Axe Stone |  | - |  |
| リーフカタナストーン | Leaf Katana Stone |  | - |  |
| ウィンドナイフストーン | Wind Knife Stone |  | - |  |
| ウィンドクラブストーン | Wind Club Stone |  | - |  |
| ウィンドソードストーン | Wind Sword Stone |  | - |  |
| ウィンドアックスストーン | Wind Axe Stone |  | - |  |
| ウィンドカタナストーン | Wind Katana Stone |  | - |  |
| アースナイフストーン | Earth Knife Stone |  | - |  |
| アースクラブストーン | Earth Club Stone |  | - |  |
| アースソードストーン | Earth Sword Stone |  | - |  |
| アースアックスストーン | Earth Axe Stone |  | - |  |
| アースカタナストーン | Earth Katana Stone |  | - |  |
| サンダーナイフストーン | Thunder Knife Stone |  | - |  |
| サンダークラブストーン | Thunder Club Stone |  | - |  |
| サンダーソードストーン | Thunder Sword Stone |  | - |  |
| サンダーアックスストーン | Thunder Axe Stone |  | - |  |
| サンダーカタナストーン | Thunder Katana Stone |  | - |  |
| ウォーターパワーストーン　ＣＬ１ | Water Power Stone CL1 |  | - |  |
| ウォーターパワーストーン　ＣＬ２ | Water Power Stone CL2 |  | - |  |
| ウォーターパワーストーン　ＣＬ３ | Water Power Stone CL3 |  | - |  |
| ウォーターパワーストーン　ＣＬ４ | Water Power Stone CL4 |  | - |  |
| ファイアパワーストーン　ＣＬ１ | Fire Power Stone CL1 |  | - |  |
| ファイアパワーストーン　ＣＬ２ | Fire Power Stone CL2 |  | - |  |
| ファイアパワーストーン　ＣＬ３ | Fire Power Stone CL3 |  | - |  |
| ファイアパワーストーン　ＣＬ４ | Fire Power Stone CL4 |  | - |  |
| リーフパワーストーン　ＣＬ１ | Leaf Power Stone CL1 |  | - |  |
| リーフパワーストーン　ＣＬ２ | Leaf Power Stone CL2 |  | - |  |
| リーフパワーストーン　ＣＬ３ | Leaf Power Stone CL3 |  | - |  |
| リーフパワーストーン　ＣＬ４ | Leaf Power Stone CL4 |  | - |  |
| ウィンドパワーストーン　ＣＬ１ | Wind Power Stone CL1 |  | - |  |
| ウィンドパワーストーン　ＣＬ２ | Wind Power Stone CL2 |  | - |  |
| ウィンドパワーストーン　ＣＬ３ | Wind Power Stone CL3 |  | - |  |
| ウィンドパワーストーン　ＣＬ４ | Wind Power Stone CL4 |  | - |  |
| アースパワーストーン　ＣＬ１ | Earth Power Stone CL1 |  | - |  |
| アースパワーストーン　ＣＬ２ | Earth Power Stone CL2 |  | - |  |
| アースパワーストーン　ＣＬ３ | Earth Power Stone CL3 |  | - |  |
| アースパワーストーン　ＣＬ４ | Earth Power Stone CL4 |  | - |  |
| サンダーパワーストーン　ＣＬ１ | Thunder Power Stone CL1 |  | 23 chars: check 112 px |  |
| サンダーパワーストーン　ＣＬ２ | Thunder Power Stone CL2 |  | - |  |
| サンダーパワーストーン　ＣＬ３ | Thunder Power Stone CL3 |  | - |  |
| サンダーパワーストーン　ＣＬ４ | Thunder Power Stone CL4 |  | - |  |
| ウォーターコートストーン　ＣＬ１ | Water Coat Stone CL1 |  | - |  |
| ウォーターコートストーン　ＣＬ２ | Water Coat Stone CL2 |  | - |  |
| ウォーターコートストーン　ＣＬ３ | Water Coat Stone CL3 |  | - |  |
| ウォーターコートストーン　ＣＬ４ | Water Coat Stone CL4 |  | - |  |
| ファイアコートストーン　ＣＬ１ | Fire Coat Stone CL1 |  | - |  |
| ファイアコートストーン　ＣＬ２ | Fire Coat Stone CL2 |  | - |  |
| ファイアコートストーン　ＣＬ３ | Fire Coat Stone CL3 |  | - |  |
| ファイアコートストーン　ＣＬ４ | Fire Coat Stone CL4 |  | - |  |
| リーフコートストーン　ＣＬ１ | Leaf Coat Stone CL1 |  | - |  |
| リーフコートストーン　ＣＬ２ | Leaf Coat Stone CL2 |  | - |  |
| リーフコートストーン　ＣＬ３ | Leaf Coat Stone CL3 |  | - |  |
| リーフコートストーン　ＣＬ４ | Leaf Coat Stone CL4 |  | - |  |
| ウィンドコートストーン　ＣＬ１ | Wind Coat Stone CL1 |  | - |  |
| ウィンドコートストーン　ＣＬ２ | Wind Coat Stone CL2 |  | - |  |
| ウィンドコートストーン　ＣＬ３ | Wind Coat Stone CL3 |  | - |  |
| ウィンドコートストーン　ＣＬ４ | Wind Coat Stone CL4 |  | - |  |
| アースコートストーン　ＣＬ１ | Earth Coat Stone CL1 |  | - |  |
| アースコートストーン　ＣＬ２ | Earth Coat Stone CL2 |  | - |  |
| アースコートストーン　ＣＬ３ | Earth Coat Stone CL3 |  | - |  |
| アースコートストーン　ＣＬ４ | Earth Coat Stone CL4 |  | - |  |
| サンダーコートストーン　ＣＬ１ | Thunder Coat Stone CL1 |  | - |  |
| サンダーコートストーン　ＣＬ２ | Thunder Coat Stone CL2 |  | - |  |
| サンダーコートストーン　ＣＬ３ | Thunder Coat Stone CL3 |  | - |  |
| サンダーコートストーン　ＣＬ４ | Thunder Coat Stone CL4 |  | - |  |
| フリーズストーン　ＣＬ１ | Freeze Stone CL1 |  | - |  |
| フリーズストーン　ＣＬ２ | Freeze Stone CL2 |  | - |  |
| フリーズストーン　ＣＬ３ | Freeze Stone CL3 |  | - |  |
| カウントダウンストーン　ＣＬ１ | Countdown Stone CL1 |  | - |  |
| カウントダウンストーン　ＣＬ２ | Countdown Stone CL2 |  | - |  |
| カウントダウンストーン　ＣＬ３ | Countdown Stone CL3 |  | - |  |
| デッキダウンストーン　ＣＬ２ | Deck Down Stone CL2 |  | - |  |
| デッキダウンストーン　ＣＬ３ | Deck Down Stone CL3 |  | - |  |
| ミノタウロストーン　ＣＬ２ | Minotaur Stone CL2 |  | - |  |
| ミノタウロストーン　ＣＬ３ | Minotaur Stone CL3 |  | - |  |
| サーペントストーン　ＣＬ２ | Serpent Stone CL2 |  | - |  |
| サーペントストーン　ＣＬ３ | Serpent Stone CL3 |  | - |  |
| サラマンダーストーン　ＣＬ２ | Salamander Stone CL2 |  | - |  |
| サラマンダーストーン　ＣＬ３ | Salamander Stone CL3 |  | - |  |
| トレントストーン　ＣＬ２ | Treant Stone CL2 |  | - |  |
| トレントストーン　ＣＬ３ | Treant Stone CL3 |  | - |  |
| ジンストーン　ＣＬ２ | Djinn Stone CL2 |  | - |  |
| ジンストーン　ＣＬ３ | Djinn Stone CL3 |  | - |  |
| クエイクストーン　ＣＬ２ | Quake Stone CL2 |  | - |  |
| クエイクストーン　ＣＬ３ | Quake Stone CL3 |  | - |  |
| インドラストーン　ＣＬ２ | Indra Stone CL2 |  | - |  |
| インドラストーン　ＣＬ３ | Indra Stone CL3 |  | - |  |
| アイスストーン　ＣＬ１ | Ice Stone CL1 |  | - |  |
| アイスストーン　ＣＬ２ | Ice Stone CL2 |  | - |  |
| アイスストーン　ＣＬ３ | Ice Stone CL3 |  | - |  |
| ファイアストーン　ＣＬ１ | Fire Stone CL1 |  | - |  |
| ファイアストーン　ＣＬ２ | Fire Stone CL2 |  | - |  |
| ファイアストーン　ＣＬ３ | Fire Stone CL3 |  | - |  |
| プランツストーン　ＣＬ１ | Plants Stone CL1 |  | matches Plants Attack; UNSURE |  |
| プランツストーン　ＣＬ２ | Plants Stone CL2 |  | - |  |
| プランツストーン　ＣＬ３ | Plants Stone CL3 |  | - |  |
| ストームストーン　ＣＬ１ | Storm Stone CL1 |  | - |  |
| ストームストーン　ＣＬ２ | Storm Stone CL2 |  | - |  |
| ストームストーン　ＣＬ３ | Storm Stone CL3 |  | - |  |
| アースストーン　ＣＬ１ | Earth Stone CL1 |  | - |  |
| アースストーン　ＣＬ２ | Earth Stone CL2 |  | - |  |
| アースストーン　ＣＬ３ | Earth Stone CL3 |  | - |  |
| ライトニングストーン　ＣＬ１ | Lightning Stone CL1 |  | - |  |
| ライトニングストーン　ＣＬ２ | Lightning Stone CL2 |  | - |  |
| ライトニングストーン　ＣＬ３ | Lightning Stone CL3 |  | - |  |
| 素手 | Bare Hands |  | no ÄRM equipped |  |
| サックリの実 | Crisp Fruit |  | healing fruit Ginta picks (HI_M00); サックリ = crunchy. UNSURE |  |
| ジュクした実 | Ripe Fruit |  | - |  |
| ニガい実 | Bitter Fruit |  | - |  |
| ヘブンズリーフ | Heaven's Leaf |  | - |  |
| 大きなヘブンズリーフ | Big Heaven's Leaf |  | - |  |
| ライフシード | Life Seed |  | - |  |
| マジックシード | Magic Seed |  | - |  |
| パワーシード | Power Seed |  | - |  |
| ガードシード | Guard Seed |  | - |  |
| アームシルバー | ÄRM Silver |  | engraving material? UNSURE |  |
| アームゴールド | ÄRM Gold |  | engraving material? |  |
| アームプラチナ | ÄRM Platinum |  | engraving material? |  |
| アームジュエル | ÄRM Jewel |  | engraving material? |  |

## Decisions from earlier batches
- (none yet)
