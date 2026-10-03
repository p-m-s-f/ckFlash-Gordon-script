# Flash Gordon Forced Browsing Attack Script

This Python script launches a forced browsing attack on the Comics Kingdom website to download [*Flash Gordon*](https://comicskingdom.com/flash-gordon) comic strips up to five days in advance.

## How does it work?

According to their website, Comics Kingdom uploads their comic strips at least a week in advance. By reverse-engineering their image URL encoding method, I discovered Comics Kingdom's image files follow a predictable naming convention.

Take *Flash Gordon*. The image URLS for *Flash* strips follow the naming convention `ckFlash Gordon-ENG-xxxxxxx`, where

- `ck` stands for Comics Kingdom
- `Flash Gordon` corresponds to the name of the strip (e.g., the strip *Zits* uses `Zits`)
- `ENG` indicates the strip's language (i.e., English)
- `xxxxxxx` is a seven digit number.

This filename is encoded in BASE64, before undergoing a final round of JavaScript URL encoding.

There are some parts of this convention I couldn't decipher; namely, the seven digit number identifying an image. One might assume images are named in ascending/descending order depending on their date of release (e.g., if Monday's *Flash* ends `0000004`, then Tuesdays ends `0000006`, Wednesday's `0000008` and so on), but that isn't the case. The seven-digit identifier randomly increases or decreases throughout the week.

Additionally, there are large gaps in identifier numbers preventing this script from guessing at certain strips. For example, the gap between Saturday's strip and Sunday's strip is large enough to prevent a guess on Sunday's strip using Saturday's image URL (the same is true of Sunday and Monday).

However, I did discover a relation between the image names for strips released Monday through Saturday. Their seven digit number always increments/decrements in multiples of $2$, allowing us to predict the names of yet-to-be-released strips through brute-force guessing.

## What the script does.

When passed the URL for a *Flash Gordon* image, the script undoes the JavaScript encoding and translates the filename in the resulting URL from BASE64 back to English. Then the script isolates the seven digit number at the end of the filename and generates a sequence of identical URLs, changing only the seven digit number by adding or subtracting multiples of $2$ within a set range (decided by global variable `RANGE`). The strips within the same week (excluding Sunday) fall within this range. The script makes GET requests to the Comics Kingdom site using these guesses, downloading strip images if the guess corresponds to a real URL.

This script is most useful on Mondays, when the rest of the week's strips have not yet been publicly released. The script becomes less and less useful as the week goes on, until Saturdays when it has no use at all.

I  uploaded [a video to YouTube](https://www.youtube.com/watch?v=4sBJFoyGJqs) explaining how I discovered this exploit and automated it using the script. However, I've updated the script since then, so it's a little outdated.
