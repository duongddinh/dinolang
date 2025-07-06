# DinoLang: From the before

> Scientist had to use advanced technology to bring this programming language back to life.
---

## What in the Mesozoic is DinoLang?

DinoLang is a **tiny, fossil-fuelled toy language** that predates [ApeLang](https://github.com/duongddinh/apelang) by several geological epochs (ApeLang is, frankly, a newborn mammal in comparison). Dino was dug up by brave archaeologists wielding Vim and bad puns. Use it when you need:

| Keyword  | What it does                                     | Paleolithic analogy                           |
| -------- | ------------------------------------------------ | --------------------------------------------- |
| `FOSSIL` | Declare & optionally initialize a variable       | Bury treasure for future archaeologists       |
| `ROAR`   | Print an int **or** string                       | The dino equivalent of shouting into the void |
| `HERD`   | Read a line of user input into a string variable | Wrangling velociraptors, but with fgets       |
| `GROW`   | Integer addition                                 | Watch the hatchling get swole                 |
| `SHRINK` | Integer subtraction                              | 🦖 → 🐣                                       |
| `HATCH`  | Integer multiplication                           | Eggs *everywhere*                             |
| `SPLIT`  | Integer division                                 | Meteor hits, population halves                |

> DinoLang only supports what it supports.
> **It’s prehistoric, not feature-rich.**

---

## System Requirements

* **Hardware:** Intel-based macOS machine (any Apple Silicon needs Rosetta 2—and a sense of humor).
* **OS:** macOS 10.13+ (64-bit).
* **Toolchain:**

  * Python 3.x (to run `dinoc.py`)
  * Xcode command-line tools (`gcc`, `ld`, etc.)
  * Thick skin for dino jokes

 **  Linux users:** The assembler will hiss, the linker will bite, and everything bursts into tar. Stick to macOS.

---

## How to Compile This Relic

1. **Write your masterpiece**

   ```dino
   # hello.dino
   FOSSIL greeting = "Hello, Dino!";
   ROAR greeting;
   ```

2. **Generate assembly**

   ```bash
   python dinoc.py hello.dino
   produces hello.s
   ```

3. **Assemble & link**

   ```bash
   gcc -o hello hello.s      # Mach-O only!
   ./hello
   ```

4. **Bask in Jurassic glory**

   ```
   Hello, Dino!
   ```

If a T-rex crashes through your terminal, it’s probably a segmentation fault. (Check that you passed a *pointer*, not the fossilized remains of one.)

---

## Example: The Full Paleontology Tour

```dino
FOSSIL myString = "Welcome to DinoLang!";
ROAR myString;

FOSSIL name = "";
ROAR "What's your name, Dino?";
HERD name;
ROAR "Nice to meet you, ";
ROAR name;
ROAR "!";

FOSSIL result = GROW 10 5;
ROAR result;
```

Terminal dig-site:

```bash
python dinoc.py tour.dino
gcc -o tour tour.s
./tour
```

Output (after you type “Spike”):

```
Welcome to DinoLang!
What's your name, Dino?
Spike
Nice to meet you, Spike!
15
```

---

## Why Dino over ApeLang?

| DinoLang                   | ApeLang                                   |
| -------------------------- | ----------------------------------------- |
| Written in stone tablets   | Written on banana peels                   |
| Emits pure x86-64 assembly | Emits bytecode with modern conveniences   |
| Only runs on macOS Intel   | Runs *everywhere* but smells like bananas |
| **Roars**                  | *Hoots*                                   |

> Remember: **prehistoric != obsolete**—it just means *fewer moving parts to break* (and more bones to trip over).

---


“**Code like a caveman, roar like there’s no asteroid coming.**”
