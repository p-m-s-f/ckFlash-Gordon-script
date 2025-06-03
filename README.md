A Python script that uses forced browsing to download the current week's Flash Gordon strips from the Comics Kingdom website!

The script works by reverse engineering Comics Kingdom's URL encoding method which they use on the comic strips syndicated on their website; image files follow the naming convention "ckFlash Gordon-ENG-xxxxxxx", where "ck" stands for Comics Kingdom, "Flash Gordon" corresponds to the name of the strip (e.g. the comic strip Zits uses "Zits"), "ENG" indicates the language of the strip (English), and "xxxxxxx" represents a seven digit number. This filename is then encoded in BASE64, and then encoded once more through Javascript URL encoding.

Given the URL for one of these strip images, the script undoes the Javascript encoding and translates the filename in the resulting URL from BASE64 back to english. Then, after isolating the seven digit number at the end of the filename, the script generates a sequence of identical URLs, changing only the seven digit number by adding or subtracting multiples of two within a set range (decided by a global variable). The strips within the same week (on days excluding Sunday) will fall within this range. The script then makes GET requests to the Comics Kingdom site with these URLs, downloading strip images where it finds them.

This script is most useful on Mondays, when the rest of the week's strips have not yet been publically released. The script becomes less and less useful as the week goes on, until Saturdays, when it has no use at all.

I've  uploaded [a video to YouTube](https://www.youtube.com/watch?v=4sBJFoyGJqs) which explains how I discovered this exploit, and how I automated it in the script.
