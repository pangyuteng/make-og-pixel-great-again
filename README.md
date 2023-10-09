
## Locate photos that takes up space in Google Photos, then upload using your OG Pixel.


### get photo urls

+ setup google-photos-api* using below links

```
refs-google-photos-api:

https://github.com/ido-ran/google-photos-api-python-quickstart
https://github.com/polzerdo55862/google-photos-api
https://console.cloud.google.com/apis/credentials

* redirect url (remember to add `/` after port 8000): `http://127.0.0.1:8000/`

```

+ fetch google photo urls to `all.csv` with below:

```
python fetchall.py
```

### find photos that takes up space.

+ determine if photo takes up space and save to `space.csv` with below:

```
python crawlall.py
```

```

refs-selenium:

https://stackoverflow.com/questions/66209119/automation-google-login-with-python-and-selenium-shows-this-browser-or-app-may
https://www.scrapingbee.com/blog/selenium-python


https://selenium-python.readthedocs.io/locating-elements.html

wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.337_amd64.deb

comment on selenium: had a hard time finding the right version and syntax to work - there are various tweaks online to make Google login work, and they will eventually not work, given Google actively updating to prevent automated logins and routing devs to their API - which at the time did not contain what i'm looking - the metadata per photo item does not show you if each image takes up google storage or not.

```

+ to save space, download then delete these photos, and reupload using below solution.

    + *** do not use broswer "save as" when downloading image *** , you will not retain the metadata in the jpgs!

### for new photos, sync photos using your old OG Pixel.

+ To take advantage of your old OG Pixel's unlimited photo storage functionality you can do a one way "sync" from new to old Pixel. *** i would only recommend the below solution to those who prefeer comfortable running linux commands than using guis. ***
    + for both phones:
        + install F-Droid
        + in F-Droid, install: Termux, Termux:API
        + allow file perm for Termux, run `termux-setup-storage`:
            + confirm file perm via `Settings --> Applications --> Termux --> Permissions` ( https://wiki.termux.com/wiki/Termux-setup-storage )
        + in Termux, install softwares, run `pkg install openssh rsync cronie termux-api jq`
        + in Termiux, setup password `passwd`.
    + in old phone:
        
        + setup cron job to trigger file scan

            ```
            */5 * * * * termux-media-scan -r ~/storage/dcim/Camera
            ```


        + run `crond`

        + run `sshd`

    + in new phone:

        + enable location perm for termux:api (to get wifi ssid)

        + setup cron job to rsync at set frequency, for example.

            + create file `~/sync-photos.sh`, MYWIFINAME will be your home wifie name, OGPIXELIP will be the ip of your OG Pixel phone.

                ```
                # sample sync-photos.sh content
                ssid=$(termux-wifi-connectioninfo | jq .ssid)
                echo $ssid
                if [ ${ssid} = '"${MYWIFINAME}"' ]
                then
                echo syncing...
                rsync -av -e 'ssh -p 8022' ~/storage/dcim/Camera/ root@${OGPIXELIP}:~/storage/dcim/Camera
                else
                echo not connected to home wifi
                fi
                ```

            + setup cron job

                ```
                */5 * * * * bash ~/sync-photos.sh
                ```

        + run `crond`


    + setup ssh keys and disable password login for ssh.
        
        ```
        https://www.ssh.com/academy/ssh/keygen
        https://stackoverflow.com/questions/20898384/disable-password-authentication-for-ssh
        ```     
    
