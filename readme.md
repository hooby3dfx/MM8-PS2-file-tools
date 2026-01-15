Basic tools for extracting and then rebuilding LDZ / FCAT file used by MM8 on PS2.

This file is an archive of zlib compressed text files.

The original text seems to be encoded as cp932 with windows CRLF line endings, and sometimes just LF is used for formatting.


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

Image files in ICONSJ.LDZ:
T_cred_up





T2X images
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



examples: 
fname		header	dimens		pixel_ct	fsize			bpp			psize	CLUT storage	
bt_loadH;	T2Q14;	106x37;		3922 px;	fsize 2160		//4bpp?		16
air1;		T2Q14;	100x100;	10000 px;	fsize 5680		//4bpp?
loading1;	T2S13;	640x448; 	286720 px;	fsize 287760	//8bpp		256		PAL_RGB32_CSM1
ARCOBG;		T21313;	640x480;	307200 px;	fsize 308240	//8bpp				PAL_RGB32_CSM1


ICONSJ.LDZ
	bt_loadU
		pos 17090A00	657687
		cs 32050000		1330
		us 70080000		2160
		dd if=bmpt2out_z of=ICONSJ_NEW.LDZ bs=1 count=1330 seek=657687 conv=notrunc
	T_cred_up
		pos 74770501	17135476
		cs 120D0000		3346
		us 10120000		4624
		dd if=bmpt2out_z of=ICONSJ_NEW.LDZ bs=1 count=3346 seek=17135476 conv=notrunc








