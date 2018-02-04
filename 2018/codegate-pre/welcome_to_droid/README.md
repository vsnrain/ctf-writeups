## Welcome to droid

__Type:__ RE  
__Solves:__ 24  
__Description:__  
```
> o <
```

__Files:__  
droid.apk

## Solution:
Ok, so we got an android apk, let's first unpack it and see whats inside.

```
$ ls droid

AndroidManifest.xml
classes.dex
res
META-INF
lib
resources.arsc
```

The most interesting thing here is that `lib` folder which contains library `libnative-lib.so` for different architectures. Now we know that the app uses JNI to some precompiled library. Let's move on and decompile Java classes to see what it is doing.

`$ d2j-dex2jar.sh droid/classes.dex`

Now we can see the decompiled code. It has package  
```
com.example.puing.a2018codegate
-- MainActivity.class  
-- Main2Activity.class
-- Main3Activity.class
-- Main4Activity.class
```

Then I started to analyse what this code is doing and execute it in my head. There was input field for a password, some string manipulation, and on successful check it loads next stage/class:

```Java
//MainActivity.class

if ((i >= 10) && (i <= 26))
{
    paramAnonymousView = new Intent(paramAnonymousView.getContext(), Main2Activity.class);
    paramAnonymousView.putExtra("edittext", str);
    MainActivity.this.startActivity(paramAnonymousView);
}
```

The same thing with the next class:

```Java
//Main2Activity.class

if (Main2Activity.a(paramBundle).equals(str))
{
  paramAnonymousView = new Intent(paramAnonymousView.getContext(), Main3Activity.class);
  paramAnonymousView.putExtra("id", paramBundle);
  paramAnonymousView.putExtra("pass", str);
  Main2Activity.this.startActivity(paramAnonymousView);
  return;
}
```

Ok, so we have a chain of classes, each doing some kind of check. As a proper REVERSE engineers, let's look at it backwards and look what's at the end of it.

```Java
//Main4Activity.class

System.loadLibrary("native-lib");
this.l = ((EditText)findViewById(2131230782));
this.l.setText(stringFromJNI());
```
Oh, just look at what we have here! A JNI call to previously found library. And on top of that without any parameters or manipulations. So it looks like this library is what returns the flag. Let's decompile it.


NOPE.JPG, ain't nobody got time to reverse that. We can do better, I hope you have prepared android environment with emulator/device and native libs.

Lets just attach that lib to our project, launch it and see what
```Java
public native String stringFromJNI();
```
returns. So let's create a new project, using the same package id and class name as droid.apk app, and link it to that library.

... a few minutes later ...

Ok, done.

```
build.gradle
...
sourceSets {
        main {
            jniLibs.srcDir file('jni/')
        }
    }
...
```

```Java
package com.example.puing.a2018codegate;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;

public class Main4Activity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main4);

        System.loadLibrary("native-lib");
        String s = stringFromJNI();
        Log.w("myApp", s);
    }

    public native String stringFromJNI();
}
```

Executing it we have a log message:

```
com.example.puing.a2018codegate W/myApp: Wol!! awesome!! FLAG{W3_w3r3_Back_70_$3v3n7een!!!} hahahah!!
```

Done.
