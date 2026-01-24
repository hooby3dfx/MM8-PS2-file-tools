Basic tools for extracting and then rebuilding LDZ / FCAT file used by MM8 on PS2.

Most of the original text seems to be encoded as cp932 with windows CRLF line endings, and sometimes just LF is used for formatting.

Files touched:

/SLPS_250.31
	This is the game binary in elf format, with some embedded strings

/DATA/TEXT.LDZ
	This file is an archive of zlib compressed text files.
	Text files in TEXT.LDZ:
	2devents.txt
	autonote.txt
	awards.txt
	class.txt
	credits.txt
	global.txt
	history.txt
	hostile.txt
	items.txt
	mapstats.txt
	merchant.txt
	monsters.txt
	npcdata.txt
	npcgreet.txt
	npcgroup.txt
	npcnews.txt
	npctext.txt
	npctopic.txt
	pcnames.txt
	placemon.txt
	potion.txt
	potnotes.txt
	quests.txt
	rnditems.txt
	roster.txt
	scroll.txt
	skilldes.txt
	spcitems.txt
	spells.txt
	stats.txt
	stditems.txt
	trans.txt

/INDOOR1/*/*.STR
/INDOOR2/*/*.STR
/OUTDOOR/*/*.STR
	Additional files for each area:
	D00.STR
	D05.STR
	D06.STR
	D07.STR
	D08.STR
	D09.STR
	D10.STR
	D11.STR
	D12.STR
	D13.STR
	D14.STR
	D15.STR
	D16.STR
	D17.STR
	D18.STR
	D19.STR
	D20.STR
	D21.STR
	D22.STR
	D23.STR
	D24.STR
	D25.STR
	D26.STR
	D27.STR
	D28.STR
	D29.STR
	D30.STR
	D31.STR
	D32.STR
	D33.STR
	D34.STR
	D35.STR
	D36.STR
	D37.STR
	D38.STR
	D39.STR
	D40.STR
	D41.STR
	D42.STR
	D43.STR
	D44.STR
	D45.STR
	D46.STR
	D47.STR
	D48.STR
	D49.STR
	D50.STR
	ELEMA.STR
	ELEME.STR
	ELEMF.STR
	ELEMW.STR
	OUT00.STR
	OUT01.STR
	OUT02.STR
	OUT03.STR
	OUT04.STR
	OUT05.STR
	OUT06.STR
	OUT07.STR
	OUT08.STR
	OUT13.STR
	OUT15.STR
	PBP.STR

/MM8DAT/ICONSJ.LDZ
	Image files in ICONSJ.LDZ:
	T_cred_up
	T_new_up
	T_load_up

/DATA/ARCOSPR.LDZ
	Sprite sheet for Arcomage mini game




T2XX image format
16 byte header?
	T 2 _ _ (magic number)
		x		0x51 ('Q'/81), 0x53 ('S'/83), 0x13 (19) ?
		  x		0x13 (19), 0x14 (20)
	8 bytes padding	       
	WWHH width, height

Palette/CLUT data
...
Pixel index data
...



Useful tools:
Apache 2 for inserting files into ISO
MMArchive to view the Windows MM8 LOD data files
ImHex hex editor
Notepad++ for editing text files (supports Shift-JIS encoding)
Wally for editing palette images
Kuriimu2 for viewing/understanding raw images
DeltaPatcher for creating patch/diff








