# Generative-art-generator
Generative Art Generator: Creates unique random assets with layered sprites along with Opensea compliant .json for each one.

The first set of folders inside "/assets" referes to different breeds for the art generation. For example: If you would create a collection with different breads of dogs, but not every breed would have the same selectable assets such as nose or tail, you would place those assets inside the layers of each respectable breed. In case there is only one breed, only one folder is needed in the directory.

Create breed name along with respectable rarity value in the format "breedname_rarityValue". Keep in mind all rarity values are relative to the rarity of other breeds.

Place all assets in apropriate folders inside "/assets". Should you wish to create more layers, they should be named in the same fashion as the existing folders. (Ex: 3_hats("3" being the order in which it would be placed in the final image and "hats" for the metadata generation.))

All assets should be placed in the respectable layer folder using the following syntax: numberOfAsset_rarity Ex: 1_10
Keep in mind that the rarity value is relative to that of other assets.

Use the incompatibilities.txt file to state possible visualy incompatible sprites Ex: A mask and a beard.
To state such incompatibilities use the following syntax: mask:1-beard:2
Mask and beard being layer folder titles and 1 and 2 being the asset number

Change number of assets generated in the POPULATION_COUNT variable.

Change get_metadata information for the appropriate information to be placed inside each respectable json

Change last lines to save files with appropriate names in collection and collectionjson folder

Have Fun!!! :)



