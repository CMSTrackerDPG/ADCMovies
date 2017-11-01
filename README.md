# ADCMovies tool
## What does it do?
The tool extracts 2D ADC maps from root files and puts them into the animated gif.

## Configuration and running

You need to modify ```config.py```:
1. You need to have a decrypted version of your Grid Certificate Private Key. [Here is the tutorial how to do it.](https://support.citrix.com/article/CTX122930)
2. Modify ```cert_file_path``` and ```key_file_path``` so that they point to your certificate and decrypted version of private key.
3. Put your run query into ```customQueryPiece``` to which common flag checking will be added inside the script. ```r``` is a ```runreg_tracker.runs``` table from the Run Registry. For more information [follow TWiki Guide](https://twiki.cern.ch/twiki/bin/view/CMS/DqmRrApi).
4. Decide whether you want plots from the longest run in the fill or not (```isSelectLongestRunInFill```)
4. As an option you can change the size of output plots(```histWidth```, ```histHeight```), output directory(```outputDir```), desired output file type(```fileType```) and the way the gif conversion works (```conversionOptions```, [convert guide](https://www.lifewire.com/convert-linux-command-unix-command-4097060))

## It is not working
First and above all most important: make sure your private key is decrypted and you have the correct path in ```config.py```.

Second very common reason is that Run Registry service is off or data in ```"https://cmsweb.cern.ch/dqm/online/data/browse/Original/"``` became inaccessible. Waiting for some time helps.