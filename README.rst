============
wechat-tools
============

A simple command line utility to retrieve and decrypt WeChat databases from Android phones.

Requirements
============
You will need:

* adb (the `Android Debug Bridge <http://developer.android.com/tools/help/adb.html>`__) installed and on your ``PATH``
* a rooted Android phone, connected to your computer
* WeChat installed on the phone
* a couple of Python packages (run ``pip install -r requirements.txt``)

This code was last tested with **WeChat Android 6.3.13**

Examples
========
Run this to find possible WeChat databases on your phone::

    python main.py find

If no databases were found, perhaps your phone is not rooted, or you don't have WeChat installed? Or maybe it's not a compatible version of WeChat? If you're convinced you've got your ducks in a row, file an issue with details, or investigate and propose a patch!

If more than one database was found, take a note of the path for the one you want to retrieve, because you'll need to give it to `pull` as the `--database-path` argument.

If only one database was found, when you go to pull, it will automatically pull that one.

OK, now let's pull the (encrypted) database to your computer::

    python main.py pull imported.db

This will take a while -- we are first moving the DB to a user-readable location (likely on the SD card), then using plain old `adb pull` to get it to your computer.

Once it's done, you should have ``imported.db`` in your local directory, almost there. But it's encrypted!

::

    $ xxd -g 1 -l 128 imported.db
    0000000: a2 4a 1c 74 52 75 fd 65 0b 0e 67 83 25 ef f4 17  .J.tRu.e..g.%...
    0000010: 97 74 a3 fa 34 2a b3 55 d7 37 08 d4 90 a5 f0 47  .t..4*.U.7.....G
    0000020: f1 03 ca 0c cb 41 7b 3b bf 2a 31 8a 19 42 be 52  .....A{;.*1..B.R
    0000030: 4e 7d 08 d3 91 57 2d 2a 96 23 88 fb ff 3a 3a 32  N}...W-*.#...::2
    0000040: 7c bf e4 ac 50 dc 03 5a 6d 71 a8 da bb ae cf 97  |...P..Zmq......
    0000050: 5a ac 8e c4 79 c3 9e 8f c8 3b 54 e8 3c c1 09 d2  Z...y....;T.<...
    0000060: c1 33 15 fe 00 27 62 5b c9 33 e4 cb 1c 8b 69 fb  .3...'b[.3....i.
    0000070: 97 6a 34 ac 52 b9 e8 95 42 b6 c5 33 bc b7 a5 52  .j4.R...B..3...R

The encryption key is derived from your WeChat UIN and your phone's IMEI. There are many ways to find your phone's IMEI, just Google it. To find your WeChat UIN, do this::

    python main.py get_uin

Then finally, decrypt the database with your UIN and IMEI::

    python main.py decrypt 1234567890 888888888888888 imported.db decrypted.db

And now you have a cleartext SQLite database!

::

    $ xxd -g 1 -l 128 decrypted.db
    0000000: 53 51 4c 69 74 65 20 66 6f 72 6d 61 74 20 33 00  SQLite format 3.
    0000010: 04 00 01 01 00 40 20 20 00 00 01 29 00 06 2d 2f  .....@  ...)..-/
    0000020: 00 00 00 00 00 00 00 00 00 00 00 ea 00 00 00 04  ................
    0000030: 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00  ................
    0000040: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................
    0000050: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 29  ...............)
    0000060: 00 2d e2 26 05 00 00 00 42 02 97 00 00 00 01 81  .-.&....B.......
    0000070: 03 fb 03 f6 03 f1 03 ec 03 e7 03 e2 03 dd 03 d8  ................

Migrating to a new device
=========================
It's possible to use these tools to migrate your WeChat history from one (rooted, Android) device to another (also rooted, Android) device. This process is not exact, but roughly it looks like this:

#. Make sure you have the IMEIs for your old and new device (check Google for how to find this).
#. Make sure you know your WeChat UIN (use ``python main.py get_uin`` with your old device hooked up to ADB).
#. Install WeChat on your new device (preferably the same version of WeChat to avoid any possible schema or migration issues). Don't sign in yet.
#. Enable Airplane Mode on your old device.
#. Log in to WeChat on your new device (this will create the requisite data directories for your account).
#. Once you are logged in, immediately enable Airplane Mode on your new device, too. (**If you don't, any messages you receive between this moment and completing the transfer will be lost!**)
#. Force-close WeChat on your new device.
#. Plug in your old device and pull the database: ``python main.py pull``.
#. Decrypt the database with your old device's IMEI, and your WeChat UIN: ``python main.py decrypt``.
#. Re-encrypt the database with your new device's IMEI, and (the same as for decryption step) WeChat UIN: ``python main.py encrypt``.
#. Push the database to your new phone's data directory, in the same location: ``python main.py push`` (use ``python main.py find`` to find the likely database location).
#. Disable Airplane Mode and open WeChat. It will take a long time to read the database the first time! But when it's done, you'll have all your conversation history!

Migrating other information like voice messages, emojis, images, etc. is also possible (and has been tested!), but is outside the scope of this document at present.

Credits
=======
* Based on `this article on decrypting WeChat's SQLite database on Android <https://articles.forensicfocus.com/2014/10/01/decrypt-wechat-enmicromsgdb-database/>`__, and the script linked therein.
