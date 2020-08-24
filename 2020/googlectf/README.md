## ANDROID

## Type: RE/Android  

## Files:  
[reverse.apk](reverse.apk)

## Solution:
First thing I did was unpack application and look what we have here.
```
apktool d reverse.apk
```
Looks quite simplistic, no native libs, no 3rd party frameworks etc.  
Lets try loading it with Bytecode Viever. Immediately we see that something is not right.

**ő.class**
```java
package com.google.ctf.sandbox;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import com.google.ctf.sandbox.ő.1;

public class ő extends Activity {
	long[] class;
	int ő;
	long[] ő;

	public ő() {
		throw new RuntimeException("d2j fail translate: java.lang.NullPointerException\n\tat java.base/java.lang.String.rangeCheck(String.java:298)\n\tat java.base/java.lang.String.<init>(String.java:294)\n\tat org.a.a.t.e(Unknown Source)\n\tat com.googlecode.d2j.converter.IR2JConverter.toInternal(Unknown Source)\n\tat com.googlecode.d2j.converter.IR2JConverter.reBuildTryCatchBlocks(Unknown Source)\n\tat com.googlecode.d2j.converter.IR2JConverter.convert(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2jar$2.ir2j(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2Asm.convertCode(Unknown Source)\n\tat com.googlecode.d2j.dex.ExDex2Asm.convertCode(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2jar$2.convertCode(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2Asm.convertMethod(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2Asm.convertClass(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2Asm.convertDex(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2jar.doTranslate(Unknown Source)\n\tat com.googlecode.d2j.dex.Dex2jar.to(Unknown Source)\n\tat com.googlecode.dex2jar.tools.Dex2jarCmd.doCommandLine(Unknown Source)\n\tat com.googlecode.dex2jar.tools.BaseCmd.doMain(Unknown Source)\n\tat com.googlecode.dex2jar.tools.Dex2jarCmd.main(Unknown Source)\n\tat the.bytecode.club.bytecodeviewer.util.Dex2Jar.dex2Jar(Dex2Jar.java:54)\n\tat the.bytecode.club.bytecodeviewer.BytecodeViewer$8.run(BytecodeViewer.java:957)\n");
	}

	protected void onCreate(Bundle var1) {
		super.onCreate(var1);
		this.setContentView(2131034112);
		EditText var3 = (EditText)this.findViewById(2130968582);
		TextView var2 = (TextView)this.findViewById(2130968597);
		((Button)this.findViewById(2130968578)).setOnClickListener(new 1(this, var3, var2));
	}
}
```

Also we can see a function that does some DIY encoding, which we focus on later:

```java
package com.google.ctf.sandbox;

public final class R {
	public static long[] ő(long var0, long var2) {
		if (var0 == 0L) {
			return new long[]{0L, 1L};
		} else {
			long[] var4 = ő(var2 % var0, var0);
			return new long[]{var4[1] - var2 / var0 * var4[0], var4[0]};
		}
	}
}

```

Exception description tells us that `dex2jar` is failing to translate dex bytecode, and the likely reason is here `com.googlecode.d2j.converter.IR2JConverter.reBuildTryCatchBlocks`. It seems that challenge author used some undefined behavior or bug in dex2jar implementation to obfuscate constructor of `class ő` and implementation of method `ő.onCreate`, so we have to work with smali code directly.  

First I tried reading it manually, considered using some existing frameworks to buid AST of smali code to translate it to more readable format. Then I had the idea that it would be much easier to just fix smali code causing `dex2jar` to throw exception, compile it, and then decompile to readable java code, and (spoiler alert) that actually worked.  

We already got that `dex2jar` is failing somewhere in `reBuildTryCatchBlocks`, lets look at `class ő` in smali.
As we scroll through it, casually looking for try/catch, one weird thing immediately pops up:  

```smali
iput v0, p0, Lcom/google/ctf/sandbox/ő;->ő:I
:try_end_0
.catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0
.catch Ljava/lang/Error; {:try_start_0 .. :try_end_0} :catch_0
.catch I {:try_start_0 .. :try_end_0} :catch_1
```

\* naming scheme for reference:  
```
boolean             Z
byte                B
char                C
double              D
float               F
int                 I
long                J
short               S 
class or interface  Lclassname;
```

So we can see that there is a try/catch block that tries to catch `class Exception`, `class Error` and `int`.
I assume this is what causes `dex2jar` to crash as `int` is not a subcalss of `java.lang.Throwable`, thus cannot be thrown/caught. And dalvik bytecode is still fine as any possible case (except perhaps `android.os.strictmode.Violation` ?) will be covered by two previous catch blocks.

```
Throwable
public class Throwable 
extends Object implements Serializable

java.lang.Object
	↳ java.lang.Throwable

Known direct subclasses
Error, Exception, Violation
```

Other than that, we have to get rid of `ő` in the `AndroidManifest.xml` as it seems `apktool` have issues building apk with weird characters in manifest.  

And indeed, this fixed `dex2jar` issue and now we can see readable java code:

```java
package com.google.ctf.sandbox;

import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import com.google.ctf.sandbox.ő.1;

public class ő extends Activity {
	long[] class;
	int ő;
	long[] ő;

	public ő() {
		while(true) {
			try {
				this.class = new long[]{40999019L, 2789358025L, 656272715L, 18374979L, 3237618335L, 1762529471L, 685548119L, 382114257L, 1436905469L, 2126016673L, 3318315423L, 797150821L};
				this.ő = new long[12];
				this.ő = 0;
				return;
			} catch (Error | Exception var2) {
			}
		}
	}

	protected void onCreate(Bundle var1) {
		super.onCreate(var1);
		this.setContentView(2131034112);
		EditText var3 = (EditText)this.findViewById(2130968582);
		TextView var2 = (TextView)this.findViewById(2130968597);
		((Button)this.findViewById(2130968578)).setOnClickListener(new 1(this, var3, var2));
	}
}
```

There is another one invalid catch block in `ő$1.smali` trying to catch `long`, lets remove that too:
```smali
.catch J {:try_start_0 .. :try_end_0} :catch_0
```

Now that we have readable code, lets analyze it:  
- we have a class `ő` that has a few properties with same name (but different types, thus being legal)  
`long[] class; int ő; long[] ő;`
- `long[] class` is set in constructor to some magic values (spoiler alert, its encoded flag).
- `int ő;` and `long[] ő;` initialized to empty values, perhaps it is temporary variables.

Now lets look at `ő$1.class`.  
At first sight it may look complex, but it is actually extremely simple once you remove all try/catch/goto trash.  
Lets analyse it block by block.

First block of code is not much useful, it just constructs a string that is not used or referenced anywhere else.  
`Apparently this is not the flag. What's going on?`  

```java
var2 = new Object[]{65, 112, 112, 97, 114, 101, 110, 116, 108, 121, 32, 116, 104, 105, 115, 32, 105, 115, 32, 110, 111, 116, 32, 116, 104, 101, 32, 102, 108, 97, 103, 46, 32, 87, 104, 97, 116, 39, 115, 32, 103, 111, 105, 110, 103, 32, 111, 110, 63};
var15 = new StringBuilder();
var3 = var2.length;

for(var4 = 0; var4 < var3; ++var4) {
	var15.append((Character)var2[var4]);
}
```

Second block of code seems more useful. It is checking if input is not 48 chars long, in that case it returns.  
So we can assume flag is 48 char long and `var16` will be our input.

```java
var16 = this.val$editText.getText().toString();
if (var16.length() != 48) {
	this.val$textView.setText("❌");
	return;
}
```

Third block of code looks like actual encoding. It iterates over user input 4 char at a time and creates `long[]` array of 12 values (suspiciously similar to what we have found in class constructor)
```java
var4 = 0;

while(true) {

	if (var4 >= var16.length() / 4) {
		break;
	}

	this.this$0.ő[var4] = (long)(var16.charAt(var4 * 4 + 3) << 24);
	long[] var18 = this.this$0.ő;
	var18[var4] |= (long)(var16.charAt(var4 * 4 + 2) << 16);
	var18 = this.this$0.ő;
	var18[var4] |= (long)(var16.charAt(var4 * 4 + 1) << 8);
	var18 = this.this$0.ő;
	var18[var4] |= (long)var16.charAt(var4 * 4);

	++var4;
}
```

And finally we see that it is indeed checking array of encoded user input against `this.class` which is a `long[]` of 12 magic values.

```java
ő var17;

var17 = this.this$0;
if ((R.ő(this.this$0.ő[this.this$0.ő], 4294967296L)[0] % 4294967296L + 4294967296L) % 4294967296L != this.this$0.class[this.this$0.ő]) {
	this.val$textView.setText("❌");
	return;
}

var17 = this.this$0;
++var17.ő;
if (this.this$0.ő >= this.this$0.ő.length) {
	this.val$textView.setText("🚩");
	return;
}

```

So now, we need to find all 4 char inputs that after operations in block 3 above, will be equal to each number in `long[] this.class`. We can try reverseing math, but bruteforcing each 4 char block will be much faster and easier.  

The solution is listed below:
```java
public class Solution{

	public static long[] RZ(long var0, long var1) {
		if (var0 == 0L) {
			return new long[]{0L, 1L};
		} else {
			long[] var4 = RZ(var1 % var0, var0);
			long[] mm = new long[]{var4[1] - var1 / var0 * var4[0], var4[0]};
			return mm;
		}
	}

	public static void main(String []args){


		long[] flag = new long[]{40999019L, 2789358025L, 656272715L, 18374979L, 3237618335L, 1762529471L, 685548119L, 382114257L, 1436905469L, 2126016673L, 3318315423L, 797150821L};

		for (int i =0; i<12; i++){

			out:
			for (char a0=32; a0<=128; a0++){
				for (char a1=32; a1<=128; a1++){
					for (char a2=32; a2<=128; a2++){
						for (char a3=32; a3<=128; a3++){

							long s = (long)(a3 << 24);
							s |= (long)(a2 << 16);
							s |= (long)(a1 << 8);
							s |= (long)(a0);

							long[] x = RZ(s, 4294967296L);
							if ((x[0]% 4294967296L + 4294967296L) % 4294967296L == flag[i]){
								System.out.print("" + a0 + a1 + a2 + a3);
								break out;
							}

						}
					}
				}
			}

		}

	}
}
```

```
$ javac Solution.java && java Solution
CTF{y0u_c4n_k3ep_y0u?_m4gic_1_h4Ue_laser_b3ams!}  
```
Done.
