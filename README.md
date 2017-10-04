# Crusader Kings 2 to Europa Universalis 4 processing scripts

--Background--

I have been quite looking forward to the Nation Designer feature of the upcoming EU4 El Dorado expansion. Last week I thought it would be fun to start a short 1337-1444 vanilla CK2 game, transfer it into EU4 after El Dorado’s release and then modify some of the nations. 

Knowing how buggy the CK2 exporter has been, I figured it would be best to test it before starting my CK2 game. I started a year 1337 Vanilla game, ran it for a few in-game days, before exporting it.

Whilst the non-splitting of cultures has been an ever-present issue, I was horrified by the techgroup assignments.

Upon inspection of the exported files I felt I could use my extremely limited Python for-loop creating abilities to write a simple script that could use EU4 assets to update and correct some of the issues I have with my CK2 exports.

--Methodology--

The CK2-EU4 Python Post Processor assumes that an exported CK2 game somewhat resembles the vanilla EU4 1444 start date with regards to province cultures and nation techgroup assignments. It looks to form a compromise between the two games.

It uses the following methodology:

Record the primary culture and capital location of each CK2 export nation.
Go through each CK2 export province. Set a flag if the culture of the province is the primary culture of the owner nation.
Contrast each CK2 nation’s capital province with its corresponding 1444 EU4 province. Replace the CK2 nation’s primary culture with the culture of that specific 1444 EU4 province, and the CK2 nation’s tech group with the tech group of that 1444 EU4 province’s owner.
Look again at the CK2 export provinces. If the province is flagged as originally sharing the same culture as its owner, then replace its culture with the nation’s new primary culture from step 3. If the CK2 province is not flagged then simply set its culture to be that of its corresponding 1444 EU4 province.
For example:

In some exported CK2 game, the Golden Horde is ruled by someone who is Catholic, of Mongol culture, and who has their capital in Sarai. 

In vanilla EU4, the province Sarai, in the year 1444 is of Astrakhani culture, and has an owner in the Nomad techgroup. The imported CK2 Golden Horde will therefore remain Catholic, have all its provinces of Mongol culture become Astrakhani, have Astrakhani set as its primary culture, and finally be placed in the Nomad techgroup.

--Comments--

Keep in mind it is all still very much work in progress.

The post processor in its current state may not produce a desired outcome in instances where a CK2 nation’s capital is moved outside of the owner’s culture’s homelands i.e. If in CK2 the Golden Horde conquers Constantinople, sets it as its capital, and the province becomes Mongol, then the output of the post processor will have the every previously Mongol province in the Golden Horde nation become Greek, and the Golden Horde will be placed in the Eastern techgroup.

I don’t expect this to be so much of an issue with the AI lead realms, but players have a habit of moving their capitals about.

Additional logic in the script comparing CK2 country tags to available EU4 country tags may be able to mitigate this issue – I’ll add this later.

My graphics card died a few days ago, and I have been unable to test the script's output. If you are interested and versed in Python feel free to download it and tinker. The script was written in Python 2.7, CK2 was version 2.3.3, and EU4 was version 1.9.2.

--Testing instructions--

1. Unzip the zip file containing the Python script and folders.
2. From your CK2 export files, copy the contents of your history/countries and history/provinces folders into the 
CK2 EU4 post processor/fromCK2/countries, and CK2 EU4 post processor/fromCK2/provinces folders respectively.
3. Go into your main EU4 directory and copy the contents of your history/countries and history/provinces folders into 
CK2 EU4 post processor/fromEU4/countries and CK2 EU4 post processor/fromEU4/provinces folders respectively.
4. Run the script. New files will be created in the modded/ sub-folders. Overwrite your CK2 export country and province files with these new files to test!
