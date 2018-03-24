## be_back

__Type:__ RE/iOS  

__Files:__  
[beback.ipa](beback.ipa)

## Solution:
As usual, let's start with the static analysis of the app. Right after unpacking this app we can see something interesting. Specifically, `Settings.plist` file.

```XML
Settings.plist

<plist version="1.0">
<dict>
	<key>secret.srv</key>
	<string>http://beback.insomni.hack</string>
	<key>app.secret</key>
	<string>s3cret1NS1800000</string>
</dict>
</plist>
```

Some server address and a secret key. The server seems to detect access from desktop and returns
```
ARE YOU KIDDING ME?!!
```
so we'll see how it is used by the app later.

Also we can see that the app was written in Swift, judging by all those `libswift*.dylib` in Frameworks folder.

Now let's take a look at the binary.

```
$ file be_back
be_back: Mach-O universal binary with 2 architectures: [arm_v7:Mach-O executable arm_v7] [arm64:Mach-O 64-bit executable arm64]  
be_back (for architecture armv7):	Mach-O executable arm_v7  
be_back (for architecture arm64):	Mach-O 64-bit executable arm64  
```
Well fine, no simulator, we will have to use the real device then. Let's continue with disassembly, I used Hopper.

Searching for strings, besides a lot of ObjC methods, revealed some interesting things. The most suspicious looking strings was following:
```
flagLbl
hflagLbl
...
fakeflag
flag
...
8929343685299874
...
INS{**************}
...
"Jailbreaked Device!
/Applications/Cydia.app
/Library/MobileSubstrate/MobileSubstrate.dylib
/bin/bash
/usr/sbin/sshd
/etc/apt
cydia://package/com.example.package
```

First, we can see that app tries to perform simple Jailbreak detection, which is only a bit more useful than completely useless.
Second, we can guess from it that there is two variables/textlabels for the flag, and one of them is fake, which is probably the string nearby, and that may be really useful.
Then, there is a really suspicious 16 char/digit string which may be some encryption key or iv.

Ok, time to see the disassembly. Searching for the refs to found strings lead us to some relatively big and interesting procedure. Just by glancing at it we can see that it starts with reading the `Settings.plist` we found earlier.

By intercepting the traffic from the device we can see following:
```
>>>
GET / HTTP/1.1
Host: beback.insomni.hack
Accept: */*
User-Agent: be_back/1 CFNetwork/894 Darwin/17.4.0
Accept-Language: en-us
Accept-Encoding: gzip, deflate
Connection: close

<<<
HTTP/1.1 200 OK
Date: Fri, 23 Mar 2018 20:46:09 GMT
Server: Apache/2.4.18 (Ubuntu)
Content-Length: 44
Connection: close
Content-Type: text/html; charset=UTF-8

iP8/kFDsdzx6tZo7vk65HlIgC7cTaTj+HmoG4EMouo0=
```

Base64 encoded string. Decoded it looks like encrypted data, most likely the flag. By now we already have everything that we need to get the flag. But let's continue to see what we still can do.

By following the disassembly we can see that closer to the end two variables is used. First `objc_ivar_offset__TtC7be_back14ViewController_flag` then `objc_ivar_offset__TtC7be_back14ViewController_fakeflag` right next to `INS{**************}`. So it indeed looks like it saves the real flag after decryption, but displays only the fake flag. Now we have different choices - we can modify property in binary, or add dylib to the app and reflect needed property in runtime. (Then repack it and resign with valid certificate).

Also one of the ways may be to attach a debugger after the decryption is done and just do   
```po [[[UIApplication sharedApplication] keyWindow] recursiveDescription]```

which will return
```
(lldb) po [[[UIApplication sharedApplication] keyWindow] recursiveDescription]
<UIWindow: 0x113d648e0; frame = (0 0; 375 667); autoresize = W+H; gestureRecognizers = <NSArray: 0x113d658e0>; layer = <UIWindowLayer: 0x113d64d50>>
   | <UIView: 0x113d739b0; frame = (0 0; 375 667); autoresize = W+H; layer = <CALayer: 0x113d73890>>
   |    | <UIImageView: 0x113d71bc0; frame = (0 0; 320 568); hidden = YES; autoresize = RM+BM; userInteractionEnabled = NO; layer = <CALayer: 0x113d71df0>>
   |    | <UIImageView: 0x113d72b60; frame = (36 73; 248 259); clipsToBounds = YES; hidden = YES; opaque = NO; layer = <CALayer: 0x113d72d90>>
   |    | <UIButton: 0x113d6a170; frame = (124 376; 72 72); hidden = YES; opaque = NO; autoresize = RM+BM; layer = <CALayer: 0x113d6a710>>
   |    |    | <UIImageView: 0x113eb4760; frame = (0 0; 72 72); clipsToBounds = YES; opaque = NO; userInteractionEnabled = NO; layer = <CALayer: 0x113ea2960>>
   |    | <UIView: 0x113ebf960; frame = (-1 0; 321 568); autoresize = RM+BM; layer = <CALayer: 0x113ebfd40>>
   |    |    | <UIImageView: 0x113ebfd60; frame = (0 20; 375 402); autoresize = RM+BM; userInteractionEnabled = NO; layer = <CALayer: 0x113ebff90>>
   |    |    | <UIImageView: 0x113ec0eb0; frame = (0 232; 321 336); autoresize = RM+BM; userInteractionEnabled = NO; layer = <CALayer: 0x113ec0a60>>
   |    |    | <UILabel: 0x113ec1d80; frame = (49 429; 235 68); text = 'INS{**************}'; opaque = NO; autoresize = RM+BM; userInteractionEnabled = NO; layer = <\_UILabelLayer: 0x113ec23e0>>
   |    |    | <UILabel: 0x113ec85c0; frame = (49 429; 235 68); text = 'INS{1 Am a Mach1ne}'; hidden = YES; opaque = NO; autoresize = RM+BM; userInteractionEnabled = NO; layer = <\_UILabelLayer: 0x113ec8aa0>>
   |    | <\_UILayoutGuide: 0x113d73b90; frame = (0 0; 0 20); hidden = YES; layer = <CALayer: 0x113d72aa0>>
   |    | <\_UILayoutGuide: 0x113ec96c0; frame = (0 667; 0 0); hidden = YES; layer = <CALayer: 0x113e03d80>>
```

And we can see there is indeed hidden property with a value  
`INS{1 Am a Mach1ne}`

Done.
