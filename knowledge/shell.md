# Shell and file tools

> Auto-maintained by the ai_session_skills background writer. One `###` entry
> per distinct action. `sig` comments are dedupe keys — never delete them.

## Looking around

### List a directory with permissions, sizes and dotfiles
<!-- sig: 8719517b7fea -->
<!-- sig: 279ce10d71b6 -->
<!-- sig: 5aa5b11fa86f -->
<!-- sig: 0794839cb37d -->
<!-- sig: ece76cdf30ce -->
<!-- sig: 105849062548 -->
<!-- sig: 8afac0459650 -->
<!-- sig: a145ac34420d -->
<!-- sig: eabac1f5e0f6 -->
<!-- sig: 24b8a4ec0a99 -->
<!-- sig: 85a6ec9d8df4 -->
<!-- sig: bff1611eb8ba -->
<!-- sig: 1dd188a9b85b -->
<!-- sig: edae71a8697e -->
<!-- sig: 30c3b9f3b17f -->
<!-- sig: 32a2ec32c785 -->
<!-- sig: a36c2289b5ad -->
<!-- sig: 525a6f3fb5ab -->
<!-- sig: 4631dca3ae33 -->
<!-- sig: d5ebf2af4ccd -->
<!-- sig: 6cfba2dbd234 -->
<!-- sig: 355bf9167eb4 -->
<!-- sig: df42042d6dad -->
<!-- sig: 5339e859d1b3 -->
<!-- sig: 6bfb5a90f2b2 -->
<!-- sig: 72e0157382f2 -->
<!-- sig: 03e791d14ac7 -->
<!-- sig: 4adf4c86c429 -->
<!-- sig: 34319e4faa10 -->
<!-- sig: 8eaa80e8519e -->
<!-- sig: 1774c01ebfd6 -->
<!-- sig: fbcef18ff278 -->
<!-- sig: 09c64080c99d -->
<!-- sig: 0a857f4ca05b -->
<!-- sig: a9b53b79fb2e -->
<!-- sig: 57c8f7e2c657 -->
<!-- sig: dd28d76e4f6a -->
<!-- sig: 677ef56c512f -->
<!-- sig: d94b6ee047ff -->
<!-- sig: 83cb2412d2cd -->
<!-- sig: a4ddeeb0e341 -->
<!-- sig: 843ef52c2182 -->
<!-- sig: c2a11822c7c6 -->
<!-- sig: fd4ed7e2a317 -->
<!-- sig: 47e8fb79a546 -->
<!-- sig: 1c7c3c2d591e -->

```bash
ls -la /Users/sraj/git_apps/personal
```

- **What it does:** Long listing (`-l`) including hidden entries (`-a`): mode, owner, size, mtime, name.
- **Why:** Confirms a parent directory exists and is the intended location *before* creating files in it, and reveals dotfiles like `.git`, `.env`, `.devin`.
- **Notes:** On macOS add `-h` for human-readable sizes; `-lt` sorts newest first, which is handy for finding the most recent log or download.

### List only specific directories, not their contents
<!-- sig: 145f07a1464a -->

```bash
ls -d ~/.claude/skills/session-skills ~/.config/devin/skills/session-skills ~/.copilot/skills/session-skills 2>/dev/null
```

- **What it does:** Given one or more directory paths, prints each path itself if it exists; without `-d`, `ls` would list the files inside it.
- **Why:** A quick existence check for directories you expect to be present, such as installed agent skill paths.
- **Notes:** Add `2>/dev/null` to keep missing directories from producing an error message. `ls -d */` lists only the directories in the current one.

### Read a whole small file
<!-- sig: fc88421c4fee -->
<!-- sig: 68a00ed3e5a3 -->
<!-- sig: 9f27bb8f3e50 -->
<!-- sig: 7aafb8ff15a2 -->
<!-- sig: 785aea8d5416 -->
<!-- sig: 62e952959e0b -->
<!-- sig: e1adaed13ba1 -->
<!-- sig: 4962f5319fdc -->
<!-- sig: 1077781fb7c0 -->
<!-- sig: 1b76136cc085 -->
<!-- sig: e8c828545e75 -->
<!-- sig: 3b9face5e860 -->
<!-- sig: a50aebc89441 -->
<!-- sig: 0fef951a928e -->
<!-- sig: 2c75614583f9 -->
<!-- sig: e45f3ea2dda1 -->
<!-- sig: 29d8bf5c19ff -->
<!-- sig: 7174f1e377a1 -->
<!-- sig: 7ea6e725caf7 -->
<!-- sig: 1a7485180733 -->
<!-- sig: 915410735981 -->
<!-- sig: 2b9c6b14a8cb -->
<!-- sig: ef8dd4ea39f8 -->
<!-- sig: 32f0f10323e1 -->
<!-- sig: b4b00c2d0e02 -->
<!-- sig: 1e675a303e82 -->
<!-- sig: 51f69e1f9036 -->
<!-- sig: 31753e25c9cd -->
<!-- sig: 3594e8958f0a -->
<!-- sig: 2e249ba68657 -->
<!-- sig: c0c3e540c97e -->
<!-- sig: adf8f6839819 -->
<!-- sig: 91e2b01bcd51 -->
<!-- sig: 52ef9b2409c3 -->
<!-- sig: 046135ad2b27 -->
<!-- sig: f5c88ed9decc -->

```bash
cat config.json
```

- **What it does:** Streams the file to stdout.
- **Why:** Fine for short config files; for anything large, `head`/`sed -n` avoid flooding the terminal.

### Read only the first N lines
<!-- sig: d8b3b7013f13 -->
<!-- sig: d9db06bd8076 -->
<!-- sig: 0926e1fcbe08 -->
<!-- sig: d64a43183ffe -->
<!-- sig: 0f8ca7ee894b -->
<!-- sig: e09cd363fa1a -->
<!-- sig: 309ee9159a20 -->
<!-- sig: c7facca824ba -->
<!-- sig: bb73fa797198 -->
<!-- sig: b7c735936704 -->
<!-- sig: a6067e6acb07 -->
<!-- sig: b2b7b01819ae -->
<!-- sig: 2937dfcf0e4e -->
<!-- sig: 2126ee85aacf -->
<!-- sig: 6dc786901c5a -->
<!-- sig: decbd66eacc6 -->
<!-- sig: ec97a2060723 -->
<!-- sig: cef85889b45a -->
<!-- sig: a340c526b15a -->
<!-- sig: 966f9bcae919 -->
<!-- sig: aceaf8f6b72e -->
<!-- sig: 50c77fee1bfd -->
<!-- sig: 03be9679d8d8 -->
<!-- sig: 5bad58810e14 -->
<!-- sig: 6e4338ec010f -->
<!-- sig: 6ecac8046049 -->
<!-- sig: b0e87ac85314 -->
<!-- sig: 397e8fde5bd9 -->
<!-- sig: 0112a4326c3a -->
<!-- sig: a249b357c524 -->
<!-- sig: 60b7e3b26611 -->
<!-- sig: a60f241e1c94 -->
<!-- sig: 31dadb60ecfa -->
<!-- sig: 4926167df81a -->
<!-- sig: 965069453069 -->
<!-- sig: d9ef6e225420 -->
<!-- sig: 31e4c1e596ec -->
<!-- sig: 9e947ec8a535 -->
<!-- sig: 125d5349188e -->
<!-- sig: 32fd8ec22c37 -->
<!-- sig: a3d4d3adaa13 -->
<!-- sig: 51a83b3ca5e0 -->
<!-- sig: 75f620009c08 -->
<!-- sig: 4d44c999efb2 -->
<!-- sig: 209a0b717465 -->
<!-- sig: eb315a277007 -->
<!-- sig: 0585a988c212 -->
<!-- sig: e37d3d5d6366 -->
<!-- sig: 01ee5c5b38e2 -->
<!-- sig: ca04bc479ec5 -->
<!-- sig: 4b7b4b67b9f6 -->
<!-- sig: fb5808ded881 -->
<!-- sig: bd85b7385c72 -->
<!-- sig: 864e8cccaef6 -->
<!-- sig: 9e1fdb7afd7c -->
<!-- sig: c555c4635f34 -->
<!-- sig: f4021d0fe9ba -->
<!-- sig: 53f0d0292243 -->
<!-- sig: 72b7a63e9f66 -->
<!-- sig: 4906022572ce -->
<!-- sig: be6eefeab399 -->
<!-- sig: a7f39314ec36 -->
<!-- sig: 80a832947cf2 -->
<!-- sig: 4eebc7fb9214 -->
<!-- sig: 11eee1e30b84 -->
<!-- sig: f398ff2818d3 -->
<!-- sig: ee5f98b0d467 -->
<!-- sig: c4b57846c1b8 -->
<!-- sig: b7d8f7c5997b -->
<!-- sig: 9e6e997972c1 -->
<!-- sig: bfa5e86ba947 -->
<!-- sig: 4c0539d8a25c -->
<!-- sig: 3c938099932c -->
<!-- sig: e0ee0e26d605 -->
<!-- sig: b1187c4ff6ce -->
<!-- sig: d332a317a646 -->
<!-- sig: 12d5d2b05c1f -->
<!-- sig: 7e1ac5d45eba -->
<!-- sig: 3a6707e937c8 -->
<!-- sig: aa9741d847c3 -->
<!-- sig: a3a073ed86ae -->
<!-- sig: 1559db4c6a8b -->
<!-- sig: b801bf68f788 -->
<!-- sig: c019175dc9c5 -->
<!-- sig: 2a142779e09a -->
<!-- sig: 86a2bd831327 -->
<!-- sig: 780db66d41bd -->
<!-- sig: df7b2524f97d -->
<!-- sig: db2022c900c9 -->
<!-- sig: 157335a6f78d -->
<!-- sig: e23e01dfe716 -->
<!-- sig: 74c53e40769a -->
<!-- sig: b7a40b857848 -->
<!-- sig: 9881755a1110 -->
<!-- sig: ff504a1cf7a0 -->
<!-- sig: e51375925d1e -->
<!-- sig: edc80958a978 -->
<!-- sig: 204fc7a8cd73 -->
<!-- sig: e523ca0ec577 -->
<!-- sig: 8a062fc66ff9 -->
<!-- sig: b44c911ecdb9 -->
<!-- sig: ee081a58c1c0 -->
<!-- sig: f30a37efec11 -->
<!-- sig: 37cd2eff0a22 -->
<!-- sig: 43e9e59c5b34 -->
<!-- sig: 097a7752c4e0 -->
<!-- sig: 2a3a43a190f3 -->
<!-- sig: c0d400fcca19 -->
<!-- sig: 56f61e0f668c -->
<!-- sig: 7abf680edf47 -->
<!-- sig: 55c4779f6118 -->
<!-- sig: 59c1cd1ce23e -->
<!-- sig: f3570d7ac936 -->
<!-- sig: c0d9966fa2be -->
<!-- sig: a24b81172f41 -->
<!-- sig: 0abac990cde2 -->
<!-- sig: c8471ba12778 -->
<!-- sig: 330339ca8ff2 -->
<!-- sig: edef43e6c76b -->
<!-- sig: da70a6e4955d -->
<!-- sig: c3daf1a531e9 -->
<!-- sig: 0657abedcfc5 -->
<!-- sig: 43eeda465d52 -->
<!-- sig: 18f98d1fcf8b -->
<!-- sig: 04904ec44266 -->
<!-- sig: 5a7f0d7b6674 -->
<!-- sig: 3dce3371bbe3 -->
<!-- sig: 982b10281b4e -->
<!-- sig: 2813323b571a -->
<!-- sig: 5801c4c80e6e -->
<!-- sig: eaf0a72e831b -->
<!-- sig: d81949753694 -->
<!-- sig: 3afae28a8ca6 -->
<!-- sig: 79a3a9d17947 -->
<!-- sig: 93b8635e36d0 -->
<!-- sig: 8722922b2249 -->
<!-- sig: c70cf2fbfc94 -->
<!-- sig: 3b6b254b0c11 -->
<!-- sig: f46022f93962 -->
<!-- sig: 59a7945e300a -->
<!-- sig: 9bcf47a34aea -->
<!-- sig: 91bce8860c64 -->
<!-- sig: ab346a00350d -->
<!-- sig: 40954c550c3d -->
<!-- sig: 81b977b815d6 -->
<!-- sig: 54841e46a02e -->
<!-- sig: 315d8f40fd0e -->
<!-- sig: fa516d6a587a -->
<!-- sig: d58001fcd4de -->
<!-- sig: ae7b49c950cc -->
<!-- sig: b08252b57435 -->
<!-- sig: b0c0c8b3c99b -->
<!-- sig: a4a3efc61cc3 -->
<!-- sig: 6618ffb5e9d3 -->
<!-- sig: 3dd2f7ad9b9e -->
<!-- sig: 50c1b0cdeceb -->
<!-- sig: 376eb777db0f -->
<!-- sig: 6ecf5a52ec5f -->
<!-- sig: 92bb1155795b -->
<!-- sig: d12c5bff8b7c -->
<!-- sig: e4da40dd0275 -->
<!-- sig: 58a6bf3a9d89 -->
<!-- sig: 60ad07725876 -->
<!-- sig: 605b3801757a -->
<!-- sig: ebfd04e24a6a -->
<!-- sig: 49e8adcb2c89 -->
<!-- sig: f6f38900042e -->
<!-- sig: 11267165948c -->
<!-- sig: 73495d6584df -->
<!-- sig: 7ec0cc3cd2f5 -->
<!-- sig: 938e6e5be464 -->
<!-- sig: 2eef29142a87 -->
<!-- sig: 46e7d2817043 -->
<!-- sig: f4ef0b8df3b0 -->
<!-- sig: 71b994560f5a -->
<!-- sig: 39504d7713fb -->
<!-- sig: 758d80b7ff26 -->
<!-- sig: 0501313498f9 -->
<!-- sig: e1e8aee7b676 -->
<!-- sig: 387404746765 -->
<!-- sig: d2530bf6318c -->
<!-- sig: 7f11ce3fc4b2 -->
<!-- sig: 15b3a5a9d44c -->
<!-- sig: 8440ae14fe4f -->
<!-- sig: e4254a19c745 -->
<!-- sig: 279816cd236d -->
<!-- sig: 6209a1cde7cf -->
<!-- sig: 3a5169b76f24 -->
<!-- sig: 974f92c87322 -->
<!-- sig: eec096e751ab -->
<!-- sig: 570163401cdb -->
<!-- sig: 9da6cf3a8273 -->
<!-- sig: 215289dadd23 -->
<!-- sig: 3c92b863bf14 -->
<!-- sig: c1b0ad4f5b86 -->
<!-- sig: 9620d412f2ed -->
<!-- sig: 6487736d3d53 -->
<!-- sig: 324ce9a1d723 -->
<!-- sig: 559e11bdc1dd -->
<!-- sig: edcaf424cb23 -->
<!-- sig: dc27c497c271 -->
<!-- sig: df59e52732a3 -->
<!-- sig: f91147f07efc -->
<!-- sig: 9879791e13c0 -->
<!-- sig: 9c3edbaa4b77 -->
<!-- sig: b0da201746f5 -->
<!-- sig: 6bce8317217e -->
<!-- sig: 7da4f34efba6 -->
<!-- sig: 25e051588750 -->
<!-- sig: 577a177ee18f -->
<!-- sig: 7f3d04ca7a9d -->
<!-- sig: 446c131a1204 -->
<!-- sig: c6840e70709b -->
<!-- sig: 713c26a1043d -->
<!-- sig: b35b7326ecc8 -->
<!-- sig: be2e47fbb179 -->
<!-- sig: 0ca42fdde9f1 -->
<!-- sig: 19ab021a7229 -->
<!-- sig: 668ab809496c -->
<!-- sig: 2f098e06b9bc -->
<!-- sig: 144bdf4aa823 -->
<!-- sig: 2e3281040db9 -->
<!-- sig: 887718c2a2cc -->
<!-- sig: ee97a6576a13 -->
<!-- sig: 0727006f23c8 -->
<!-- sig: b91f0c306778 -->
<!-- sig: bd7b974dd02c -->
<!-- sig: f0cd63fac711 -->
<!-- sig: 4ae4114f4e87 -->
<!-- sig: 898f3747894f -->
<!-- sig: ff26bfdee315 -->
<!-- sig: c121325041dd -->
<!-- sig: 54f9e6d096ca -->
<!-- sig: 1f0433fc0e5c -->
<!-- sig: c76ee966f655 -->
<!-- sig: 189a138c0474 -->
<!-- sig: 164ce4ba4982 -->
<!-- sig: e26707912320 -->
<!-- sig: b90b456c3f12 -->
<!-- sig: 4bc89cfa6d52 -->
<!-- sig: 3e17b685c9f8 -->
<!-- sig: 5142e067e0ed -->
<!-- sig: f265890ccda5 -->
<!-- sig: 6df486b90a9b -->
<!-- sig: 4f66a4735910 -->
<!-- sig: 5edafce4f3e5 -->
<!-- sig: e7640f4af849 -->
<!-- sig: 7718928f452f -->
<!-- sig: 9e7961b7e457 -->
<!-- sig: 74d48fb69fff -->
<!-- sig: 274433342423 -->
<!-- sig: 5fa82f2fa523 -->
<!-- sig: bf798fe59e11 -->
<!-- sig: 9dcb8726f1df -->
<!-- sig: 1c80cd2a00e5 -->
<!-- sig: 415e48dacb39 -->
<!-- sig: 4490e4d47d72 -->
<!-- sig: 61e1865080b8 -->
<!-- sig: 62f5b3088b37 -->
<!-- sig: aa71e93f0c32 -->
<!-- sig: ccf5b2285e07 -->
<!-- sig: d61424a06445 -->
<!-- sig: 548fbf45104e -->
<!-- sig: 40a9bb62e0ee -->
<!-- sig: 63eb5ea7781b -->
<!-- sig: 3905942c3e06 -->
<!-- sig: 53edb59d487f -->
<!-- sig: ae6264d1df45 -->
<!-- sig: 8292702407cb -->
<!-- sig: 90f9c1a797a5 -->
<!-- sig: 6aab28232387 -->
<!-- sig: 65f9998e6897 -->
<!-- sig: c4bb01a88933 -->
<!-- sig: 4f37bf8b1acb -->
<!-- sig: c5928f9637d5 -->
<!-- sig: 82cc9d0f1240 -->
<!-- sig: 6b338feb5931 -->
<!-- sig: 4b4cc4d15965 -->
<!-- sig: b093f7225638 -->
<!-- sig: 49fb7a3a9e3f -->
<!-- sig: 4fbde9c27d2a -->
<!-- sig: 7643a6ad818f -->
<!-- sig: 8ec2e3166f04 -->
<!-- sig: 2b2591cb3e57 -->
<!-- sig: ad01a3dbdf09 -->
<!-- sig: 537b179d45a0 -->
<!-- sig: 5ddba0eb6df6 -->
<!-- sig: df471734b85d -->
<!-- sig: cedfb3d32516 -->
<!-- sig: 34e307b7a072 -->
<!-- sig: d8b30a21fd53 -->
<!-- sig: 23cbe357440e -->
<!-- sig: 684b67d36426 -->
<!-- sig: 6b1098b90923 -->
<!-- sig: 0099485b0127 -->
<!-- sig: a3d1256c560b -->
<!-- sig: 206171dc7afc -->
<!-- sig: d083f5aa1a5b -->
<!-- sig: 981132733a5f -->
<!-- sig: 6aaf76bae206 -->
<!-- sig: 34d8d952f3e0 -->
<!-- sig: abb51d4a6233 -->
<!-- sig: d6fb6cff78d1 -->
<!-- sig: 1d1a2b683210 -->
<!-- sig: c8de7b981429 -->
<!-- sig: 92f343d0daae -->
<!-- sig: c49f19a7b2c2 -->
<!-- sig: 65143d59ddf4 -->
<!-- sig: 5e476bd026fa -->
<!-- sig: 4b5c8557ce3e -->
<!-- sig: 453987994687 -->
<!-- sig: c7ce7b8056bd -->
<!-- sig: 62d599df546e -->
<!-- sig: 6fb4857082e1 -->
<!-- sig: 0b97b183d7ac -->
<!-- sig: ce6cb1d88da8 -->
<!-- sig: 74c586bd062b -->
<!-- sig: b5479df4f861 -->
<!-- sig: 9b17b40b1905 -->
<!-- sig: 95c1f7f0bb5c -->
<!-- sig: edf89473caa8 -->
<!-- sig: c5f11b21aa46 -->
<!-- sig: 487210944009 -->
<!-- sig: 36bd3d5a34c4 -->
<!-- sig: 8b7f0b161dfc -->
<!-- sig: 05c73610f66b -->
<!-- sig: b95c5cd23f1b -->
<!-- sig: d16232c169a8 -->
<!-- sig: 5aecc68e82cf -->
<!-- sig: c76a3275a737 -->
<!-- sig: 53b016d782c7 -->
<!-- sig: 0632cb9eff2b -->
<!-- sig: 07e861cf3e9f -->
<!-- sig: 0f1126f1a3fd -->
<!-- sig: 241aaf3c9f04 -->
<!-- sig: 24f7f9e677a6 -->
<!-- sig: 1d9b545629d1 -->
<!-- sig: 718295602c21 -->
<!-- sig: 5888b9f10afc -->
<!-- sig: 670cfe4237c0 -->
<!-- sig: 3edb210f3eb2 -->
<!-- sig: 1847fe57611f -->
<!-- sig: 31a1eb3c05ac -->
<!-- sig: d5b44289ef0c -->
<!-- sig: 44e80f9183c0 -->
<!-- sig: 28d22fcb9989 -->
<!-- sig: 893a868e40d7 -->
<!-- sig: 5755b2e155d7 -->
<!-- sig: e1de416908af -->
<!-- sig: 893e2cc35a03 -->
<!-- sig: c8ebf722e200 -->
<!-- sig: 5584c2af37ad -->
<!-- sig: 58e71c81fb29 -->
<!-- sig: cd3499724ca7 -->
<!-- sig: 2c6209fc8c68 -->
<!-- sig: 7ada0c133549 -->
<!-- sig: 56bc42a7948a -->
<!-- sig: 30f4f2af8803 -->
<!-- sig: 13c8c4c89e32 -->
<!-- sig: 36d9b317d99b -->
<!-- sig: 77a078e60978 -->
<!-- sig: fab33784a6d5 -->
<!-- sig: 24e471213000 -->
<!-- sig: c385e857dd51 -->
<!-- sig: b57aac434959 -->
<!-- sig: a2d0db727a85 -->
<!-- sig: 70fb83237666 -->
<!-- sig: aa0e0cc56b8b -->
<!-- sig: 83b0c2846e8d -->
<!-- sig: e26e401b581d -->
<!-- sig: a26b18631bd2 -->
<!-- sig: 783d9bdcba8a -->
<!-- sig: 0ff0c41f6d42 -->
<!-- sig: 78b29dfdcd27 -->
<!-- sig: 41411c102fe6 -->
<!-- sig: f048c06e0e01 -->
<!-- sig: 27f4e6125477 -->
<!-- sig: 584bb1ed491b -->
<!-- sig: 5b7ee6f73588 -->
<!-- sig: b8329ca228ee -->
<!-- sig: 830f554d9634 -->
<!-- sig: 3674fa873b85 -->
<!-- sig: c8d8687ac94e -->
<!-- sig: 2a1cdf3cdd6f -->
<!-- sig: c925ed089c6a -->
<!-- sig: b6b6e8063db3 -->
<!-- sig: 4ae2690365af -->
<!-- sig: 70efc1657d6e -->
<!-- sig: a2d0534901b8 -->
<!-- sig: 87a2e55a4591 -->
<!-- sig: f7a1b8397059 -->
<!-- sig: 14278d607b18 -->

```bash
head -n 30 package.json
```

- **What it does:** Prints the first 30 lines and stops.
- **Why:** Caps output when piping something long (`... | head -30`), which keeps command output readable and cheap.
- **Variants:** `head -1` (or `head -n 1`) keeps a single line, handy for extracting a branch name or one value from a pipe such as `git status -sb | head -1`; `head` with no arguments is equivalent to `head -n 10` and is the shortest way to cap a pipeline.

### Read the last N lines of a file or pipe
<!-- sig: d85d1c71612e -->
<!-- sig: 26c5fd808225 -->
<!-- sig: ef6fda14f8fe -->
<!-- sig: b41746160aa3 -->
<!-- sig: cbdc7f775b86 -->
<!-- sig: 8428bada3465 -->
<!-- sig: f13a30e6312c -->
<!-- sig: e9c77a3402b3 -->
<!-- sig: a6983d0c7692 -->
<!-- sig: e088ac41e175 -->
<!-- sig: 1b90f9e27a19 -->
<!-- sig: 028257f1f5ee -->
<!-- sig: a0fd7e60bd9b -->
<!-- sig: 89f020049314 -->
<!-- sig: 36bf7ee75ee3 -->
<!-- sig: 0a298316cc55 -->
<!-- sig: d41804041dae -->
<!-- sig: 3f56d08b9c02 -->
<!-- sig: 9031b6065603 -->
<!-- sig: ec9188b915eb -->
<!-- sig: ebdd1681acf2 -->
<!-- sig: a677f713a781 -->
<!-- sig: 70ab73b85a41 -->
<!-- sig: 2eb6b9265cb8 -->
<!-- sig: a8652439c263 -->
<!-- sig: 592c67ee6b3b -->
<!-- sig: c32822dd232c -->
<!-- sig: de449ac13a73 -->
<!-- sig: 00ae4ad96e81 -->
<!-- sig: 8c83f0c11b57 -->
<!-- sig: 0f1f049fe444 -->
<!-- sig: 34be77a8f3c4 -->
<!-- sig: 4e4b3dbff4a1 -->
<!-- sig: 893abb498edc -->
<!-- sig: 360349ad65c2 -->
<!-- sig: 362e5323b781 -->
<!-- sig: 523de19cee7a -->
<!-- sig: 65ec10a73423 -->
<!-- sig: fb87d6036edf -->
<!-- sig: 96db4a689054 -->
<!-- sig: 22ef7ba2eaea -->
<!-- sig: 9f0ada973360 -->
<!-- sig: 1a7599d7b59c -->
<!-- sig: aa522d72d295 -->
<!-- sig: d0fb3c98a713 -->
<!-- sig: abac4ca4f7f3 -->
<!-- sig: 92afa0a4c478 -->
<!-- sig: c070255199be -->
<!-- sig: 42c4e28755be -->
<!-- sig: 74662f3264c7 -->
<!-- sig: e5a03e001fcc -->
<!-- sig: 784d70c9448e -->
<!-- sig: 6da4f22cd12d -->
<!-- sig: c8707c100aa2 -->
<!-- sig: 85264d121ef7 -->
<!-- sig: 93a22ce19f1e -->
<!-- sig: 715107cc0f25 -->
<!-- sig: c59f8c92bc3f -->
<!-- sig: d3c6e509efe1 -->
<!-- sig: be4c552737b1 -->
<!-- sig: 9d8be44d9833 -->
<!-- sig: ccc3bc35343f -->
<!-- sig: 0ac221913896 -->
<!-- sig: ce8def3fa037 -->
<!-- sig: 888bf6d45f6a -->
<!-- sig: 87e2431ea1c6 -->
<!-- sig: f93d2ebf9401 -->
<!-- sig: cf9118db0c79 -->
<!-- sig: 57d9de651dc3 -->
<!-- sig: 2f73914797ee -->
<!-- sig: f19e5c2aefc4 -->
<!-- sig: 462ee01a92e5 -->
<!-- sig: 9fe8e4113646 -->
<!-- sig: 9e477bc5e952 -->
<!-- sig: 0b8ab547f92f -->
<!-- sig: 9e7e48044230 -->
<!-- sig: bdde289ead9a -->
<!-- sig: 7c035c1242e8 -->
<!-- sig: 30db54fe099c -->
<!-- sig: 395f32e8b8fc -->
<!-- sig: 5ce0c323b45a -->
<!-- sig: 203c3c428f18 -->
<!-- sig: c3eb59db8127 -->
<!-- sig: fc5988964e28 -->
<!-- sig: 764e9414b831 -->
<!-- sig: 2036e3cfeb45 -->
<!-- sig: dd306525a74c -->
<!-- sig: df90367d7ec8 -->
<!-- sig: 3315d9236905 -->
<!-- sig: 3ae38ff4f959 -->
<!-- sig: 9117420e2f70 -->
<!-- sig: f60a2af91862 -->
<!-- sig: 5a260ca2215b -->
<!-- sig: 5204c0810feb -->
<!-- sig: f4290a3eb604 -->
<!-- sig: bf4b90e6c4cf -->
<!-- sig: 9960183e0586 -->
<!-- sig: 558b86ec408d -->
<!-- sig: ad3b39b409e3 -->
<!-- sig: c48490760d8b -->
<!-- sig: 6979a377eea7 -->
<!-- sig: 336ed58e772c -->
<!-- sig: c3334d7e5644 -->
<!-- sig: aa8105a39e42 -->
<!-- sig: 564ce91afae6 -->
<!-- sig: e27f0c762d15 -->
<!-- sig: 85cd372af682 -->
<!-- sig: 065124de0c9b -->
<!-- sig: 314bb95d68ac -->
<!-- sig: 2c92aa14958a -->
<!-- sig: b41301ac1038 -->
<!-- sig: b9996ec6cdb3 -->
<!-- sig: 40343e4c9527 -->
<!-- sig: 70a7508814e1 -->
<!-- sig: cd73549c8237 -->
<!-- sig: 281482f4212a -->
<!-- sig: b2b5b628f169 -->
<!-- sig: a38f611fc4c4 -->
<!-- sig: 0c30ffebde67 -->
<!-- sig: fea9816ada3e -->
<!-- sig: c25450b83a49 -->
<!-- sig: 6d35cedbf9e1 -->
<!-- sig: e6eb5b280223 -->
<!-- sig: 348bc4bc888c -->
<!-- sig: c32cc7b78248 -->
<!-- sig: a9af3d97b744 -->
<!-- sig: 28478d7bce4f -->
<!-- sig: 753b77e2ffc6 -->
<!-- sig: 57517df1b09b -->
<!-- sig: 0885e50b12f4 -->
<!-- sig: c2dbe8087621 -->
<!-- sig: de86bbf1a1ac -->
<!-- sig: baaf29088c8f -->
<!-- sig: a8eba6cf56dc -->
<!-- sig: 1175bd940cb9 -->
<!-- sig: ba4112ae7935 -->
<!-- sig: 8a8aa676d326 -->
<!-- sig: f281d2d7cc7a -->
<!-- sig: 8b3bbcc0c76f -->
<!-- sig: b06796ed897d -->
<!-- sig: 6c8565f4f63f -->
<!-- sig: e5dc610f76bc -->
<!-- sig: 19152fb01d78 -->
<!-- sig: 3b695a92206e -->
<!-- sig: 69088e9942a7 -->
<!-- sig: 3cb90126e82e -->
<!-- sig: 2f673de149a6 -->
<!-- sig: e66bfe9e8c62 -->
<!-- sig: ab9951c129d2 -->
<!-- sig: b6e31b7c10fb -->
<!-- sig: 89083b4fabb5 -->
<!-- sig: 08023fa2ac58 -->
<!-- sig: 00ae1c35c501 -->
<!-- sig: 213593146bf5 -->
<!-- sig: ee6deffc06fb -->
<!-- sig: 720786dbc6d5 -->
<!-- sig: 4a73c388a261 -->
<!-- sig: e9642115163b -->
<!-- sig: 965359e38f55 -->
<!-- sig: 7359aae24ac8 -->
<!-- sig: a829f63173ab -->
<!-- sig: 99cf0e29ae7f -->
<!-- sig: 91c7ea8f3275 -->
<!-- sig: 4ee67a25e978 -->
<!-- sig: a8d5f312e6b7 -->
<!-- sig: c2c8004cabf7 -->
<!-- sig: fc17d8493bcb -->
<!-- sig: 82e5aee218e5 -->
<!-- sig: a3ef61318925 -->
<!-- sig: 8919b355657f -->
<!-- sig: b28f3f91736a -->
<!-- sig: 4f45b6f235b1 -->
<!-- sig: 638a511cfb79 -->
<!-- sig: 0fa83f5c1b63 -->
<!-- sig: 49cf076b47fb -->
<!-- sig: 75496fca59b0 -->
<!-- sig: 5b09e0837dc4 -->
<!-- sig: faa7ecf94dcf -->
<!-- sig: 6c95c197c1a3 -->
<!-- sig: 4e59374fe429 -->
<!-- sig: 6b0b22441c6d -->
<!-- sig: 7843ba880776 -->
<!-- sig: b653b7675c21 -->
<!-- sig: 2dc3644424d6 -->
<!-- sig: 0078e7b3bb4a -->
<!-- sig: cfe3e56ffe4a -->
<!-- sig: f203775ffb90 -->
<!-- sig: 5d8f48a338ea -->
<!-- sig: ff78feec16fc -->
<!-- sig: 8ae03b322b5f -->
<!-- sig: 557fc1b01388 -->
<!-- sig: 92ae4156a0aa -->
<!-- sig: e70281db2b29 -->
<!-- sig: 44a2d10cbccc -->
<!-- sig: 7a7bf13b621d -->
<!-- sig: 0db5f488144d -->
<!-- sig: 3e11380b197f -->
<!-- sig: ab58f2e8c627 -->
<!-- sig: 80bc77825c12 -->
<!-- sig: ed56ebf1e795 -->
<!-- sig: 022ca9406595 -->
<!-- sig: 82cd69038bab -->
<!-- sig: 21829998bcf0 -->
<!-- sig: c77cf62f563e -->
<!-- sig: 78d15cbf2ab6 -->
<!-- sig: 4f1e9d2b17fc -->
<!-- sig: d7e32f920c15 -->
<!-- sig: 00fd7693e3a5 -->
<!-- sig: f83c9962df4d -->
<!-- sig: 71d44011c0a3 -->
<!-- sig: b4727a104dfc -->
<!-- sig: 5a50880c8cc4 -->
<!-- sig: 40187c58b2a8 -->
<!-- sig: 723442b05f77 -->
<!-- sig: 363a9e3dfe68 -->
<!-- sig: 7d9858f4f5ee -->
<!-- sig: aa34a81270f8 -->
<!-- sig: d90a8e0d737d -->
<!-- sig: 9e2d433d0ec8 -->
<!-- sig: 7cf6ba23b34d -->
<!-- sig: 8227181fc720 -->
<!-- sig: 1ec3033fb18a -->
<!-- sig: d8fcaf7066eb -->
<!-- sig: 40aa68401f55 -->

```bash
tail -n 25 .runtime/watcher.log
```

- **What it does:** Prints the final 25 lines of a file (or the last N lines from a pipeline).
- **Why:** The non-blocking way to inspect recent output from a log or a long command result.
- **Example:** `tail -n 25 .runtime/watcher.log`.
- **Notes:** `tail -25` is equivalent to `tail -n 25`. `tail -f` follows a log live.
- **Variants:** `tail -30` at the end of a pipeline limits output to the last 30 lines.

### Follow a log as it is written
<!-- sig: e379155eba32 -->

```bash
tail -f .runtime/watcher.log
```

- **What it does:** Prints the end of the file and then streams new lines as they are appended.
- **Why:** The way to watch a background process while it runs.
- **Notes:** Blocks until interrupted — never use it in a non-interactive/automated command, use `tail -n 50` instead.

### Count lines
<!-- sig: 948726cdc2e6 -->
<!-- sig: 9687221f2555 -->
<!-- sig: f237ae783fca -->
<!-- sig: 214674c0e2e0 -->
<!-- sig: 4efd0b3e7c49 -->
<!-- sig: 564df1e9e04f -->
<!-- sig: 50ce75fb1bf3 -->
<!-- sig: 3723302ab3c9 -->
<!-- sig: 5b33e4dac53c -->
<!-- sig: 1ed9f53123f3 -->
<!-- sig: 622450609e07 -->
<!-- sig: 9c41562bc204 -->
<!-- sig: f4d2316d4275 -->
<!-- sig: c7c8ab3380b4 -->
<!-- sig: 82d9704d7ff1 -->
<!-- sig: f08ec521b141 -->
<!-- sig: af65c8459d0d -->
<!-- sig: faa1ce7ade70 -->
<!-- sig: d11d09d4e99e -->
<!-- sig: 5a7e063ae9a8 -->
<!-- sig: b95982791b3a -->
<!-- sig: 917ef89a9012 -->
<!-- sig: 1e792866b9fc -->
<!-- sig: bfcad84d5f5c -->
<!-- sig: 6c212c68a584 -->
<!-- sig: 964bf9d96d90 -->
<!-- sig: 77f9b91a79f8 -->
<!-- sig: a9c3f4674984 -->
<!-- sig: ba73f1498365 -->
<!-- sig: ffe1fa0aae18 -->
<!-- sig: d80db77d0fd9 -->
<!-- sig: 3116b434de37 -->
<!-- sig: 4acbe47e7b23 -->
<!-- sig: 8e1072ff3469 -->
<!-- sig: 6e2dcfdd2691 -->
<!-- sig: 0081e67b7c3a -->

```bash
wc -l pending.jsonl
```

- **What it does:** Prints the number of newline-terminated lines.
- **Why:** Cheapest way to size a queue/log file or count matches from a pipe (`rg -l foo | wc -l`).
- **Notes:** `wc -l < file` omits the filename from the output, which is easier to use in a variable.

### List all regular files in a tree, skipping .git
<!-- sig: 4e45776fce36 -->
<!-- sig: 62a0228d6916 -->
<!-- sig: 0af255b97c0d -->
<!-- sig: 7fb7101537ed -->
<!-- sig: 9ef0dc11287f -->
<!-- sig: 80cb0b1c9f66 -->
<!-- sig: 5cafc73d8413 -->
<!-- sig: 95409ef7b30c -->
<!-- sig: 01b24af3f2b5 -->
<!-- sig: 6df3f7db666c -->
<!-- sig: 4be323bceb96 -->
<!-- sig: b20eb5d5076d -->
<!-- sig: 20ac0921bbfb -->
<!-- sig: 2bad9f7ffd1d -->
<!-- sig: 57a93cb68a5e -->
<!-- sig: 828985b04510 -->
<!-- sig: 6690f879c883 -->
<!-- sig: 3d046fc454f8 -->
<!-- sig: 259b8a698183 -->
<!-- sig: 6efa3b682c9e -->
<!-- sig: 3aa4b88799e8 -->
<!-- sig: f0e2c838bbda -->
<!-- sig: 7ba1c8519dcd -->
<!-- sig: b80dd874dd06 -->
<!-- sig: 3322a3580312 -->
<!-- sig: 6e1ea4622d7b -->
<!-- sig: b79badc7d03d -->
<!-- sig: 6491ea702ab6 -->
<!-- sig: fa25f8211fa4 -->
<!-- sig: d9e94d1007f7 -->
<!-- sig: f6f400eb7f40 -->
<!-- sig: 10b29adae6e6 -->
<!-- sig: 527972b0bb92 -->
<!-- sig: 63b5f123bbf4 -->
<!-- sig: 60ac4bf18584 -->
<!-- sig: 3b738baadb79 -->
<!-- sig: 5af7527aa3a9 -->

```bash
find . -path ./.git -prune -o -type f -print
```

- **What it does:** Walks the current directory and prints every regular file, while pruning the `.git` directory so it is not entered or printed.
- **Why:** A quick inventory of the real files in a checkout before piping to `sort`, `wc`, or an archive command.
- **Example:** `cd <repo> && find . -path ./.git -prune -o -type f -print | sort`
- **Notes:** Keep the explicit `-o -type f -print` to avoid printing the `.git` directory itself on some `find` implementations.

### List all files and directories in the current location
<!-- sig: 5cea075f59fa -->

```bash
dir /b /a
```

- **What it does:** Lists the names of all files and directories in the current directory, showing only the bare name (/b) and including all types of files (/a).
- **Why:** This provides a clean, simple list of every item present, ignoring extra metadata like size or date stamps.
- **Example:** dir /b /a on the root of the project directory.
- **Notes:** This is the Windows equivalent of 'ls -a' but outputs only the bare names.

### List and display contents of configuration files
<!-- sig: efb719f4ce5b -->
<!-- sig: 489012bb1520 -->

```bash
ls;
cat pytest.ini setup.cfg pyproject.toml '2>/dev/null'
```

- **What it does:** Lists files in the current directory, then concatenates the contents of pytest.ini, setup.cfg, and pyproject.toml, suppressing any permission errors.
- **Why:** This sequence quickly gathers key configuration files used by modern Python projects into a single stream for review.
- **Example:** ls; cat pytest.ini setup.cfg pyproject.toml '2>/dev/null' to check project setup files.
- **Notes:** The initial 'ls;' command is separated by a semicolon, executing it first before the cat command runs.

### Check current directory and staged changes
<!-- sig: 2eae801c9963 -->

```bash
pwd;
git status --short
```

- **What it does:** The command first prints the current working directory, then displays a concise summary of modified files in the working tree and staging area.
- **Why:** This provides a quick, two-part status check: where you are, and what has changed since the last commit, without the verbose output of a standard status check.
- **Example:** pwd; git status --short to confirm you are in the correct directory and see only the files you intended to modify.
- **Notes:** The semicolon separates two distinct commands that are executed sequentially in the shell.

### List contents of a virtual environment directory
<!-- sig: 32879531d91e -->

```bash
ls .venv venv 2>/dev/null
```

- **What it does:** Lists the contents of the venv directory within the .venv directory, suppressing any errors that occur.
- **Why:** This isolates the listing to only the expected virtual environment directory, preventing noise from other potential directories.
- **Example:** cd packages/collectors && (ls .venv venv 2>/dev/null | head -2; which python3; python3 -m pytest -q -x tests/test_mirrored_database_manager.py 2>&1 | tail -5)
- **Notes:** The outer parentheses group the commands, and the redirection handles potential non-existence of the directory.

### Display object properties in a vertical list format
<!-- sig: 446c3a372179 -->

```bash
Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion | Format-List
```

- **What it does:** Takes the selected properties of the Win32_VideoController objects and prints them in a list format where each property name and value appears on a new line.
- **Why:** Easier to read than the default table view when dealing with long strings or many properties that would otherwise be truncated or wrapped.
- **Example:** Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM,DriverVersion | Format-List
- **Notes:** Format-List is a formatting cmdlet and its output is typically not passed to another command; it is intended for the final step of a pipeline.

### Display process properties in a perfectly sized table
<!-- sig: ea7fb2cf5291 -->

```bash
Get-Process ollama* -ErrorAction SilentlyContinue | Select-Object ProcessName,CPU,WorkingSet,StartTime | Format-Table -AutoSize
```

- **What it does:** Filters for processes starting with 'ollama', selects specific performance metrics, and outputs them in a table where column widths automatically adjust to fit the content.
- **Why:** Prevents the output from being truncated or wrapped awkwardly when viewing long property names or large memory values.
- **Example:** Get-Process ollama* -ErrorAction SilentlyContinue | Select-Object ProcessName,CPU,WorkingSet,StartTime | Format-Table -AutoSize
- **Notes:** -ErrorAction SilentlyContinue prevents the command from failing if no processes matching the glob are found.

### Extract specific line ranges from a file
<!-- sig: 071e7276ed0d -->

```bash
$c=Get-Content tool/README.md;
$c[0..110];
$c[420..595];
$c[655..725]
```

- **What it does:** Loads the contents of tool/README.md into an array and prints three specific index ranges of lines.
- **Why:** Allows for quick inspection of specific sections of a long file without scrolling or using a full text editor.
- **Example:** $c=Get-Content tool/README.md; $c[0..110]; $c[420..595]; $c[655..725]
- **Notes:** PowerShell's Get-Content returns an array of strings when the file has multiple lines, allowing for direct index slicing.

## Path and command availability

### Check whether a command is installed on PATH
<!-- sig: fda5841bd437 -->
<!-- sig: 062c1ff28547 -->
<!-- sig: aa5b74ffda42 -->
<!-- sig: 057f12795407 -->
<!-- sig: 86860f600a31 -->
<!-- sig: 0b6cac26a921 -->
<!-- sig: cf47c9dbd815 -->
<!-- sig: 347314c76b87 -->

```bash
which <command> 2>/dev/null
```

- **What it does:** Searches the directories in `$PATH` for the named executable and prints its absolute path, discarding the error message if the command is not found.
- **Why:** A quick way to confirm that a CLI tool is installed before relying on it in a script or pipeline.
- **Example:** `which ollama 2>/dev/null`.
- **Notes:** Combine with `|| echo "not found"` to make the result explicit in non-interactive output.

### Display the type of a file path
<!-- sig: 1d92893431c9 -->

```bash
type C:Userssraj.codexskillssession-skillsSKILL.md
```

- **What it does:** The type command checks the specified path and outputs information about it, treating the path as a literal string.
- **Why:** This is used to quickly verify if a path points to a file, directory, or other recognized system object without needing to read its contents.
- **Example:** type C:Userssraj.codexskillssession-skillsSKILL.md
- **Notes:** This command is specific to Windows environments and is not portable to Unix-like shells.

### Locate executable files in the system path
<!-- sig: 081e1885d8e1 -->

```bash
where powershell.exe
```

- **What it does:** The where command searches the directories listed in the system's PATH environment variable for files matching the specified executable name.
- **Why:** It provides a quick way to confirm which specific executable file is being found when a command name might be ambiguous or when you need to verify its exact location.
- **Example:** where powershell.exe to find all instances of the PowerShell executable.
- **Notes:** This command is specific to Windows environments and uses the system PATH variable for its search scope.

### Check if the virtual environment directory exists
<!-- sig: 53cf11960c20 -->

```bash
(test -d ../../.venv
```

- **What it does:** The 'test' command checks the file system status of the specified path, and the '-d' flag ensures it only passes if the path is a directory.
- **Why:** This pattern allows checking for the existence of a required dependency directory before attempting to use tools within it, preventing subsequent commands from failing.
- **Example:** (test -d ../../.venv && echo rootvenv) ; ls ../../.venv/bin/python 2>/dev/null
- **Notes:** The parentheses group the test command, ensuring its exit status is used by the subsequent '&&' operator. The path '../../.venv' is relative to the current working directory.

### Check the availability of specific python executables
<!-- sig: fe8a22bad23b -->
<!-- sig: 9b7c68c0c9de -->

```bash
done; ls packages/python-api/.venv/bin/python packages/collectors/.venv/bin/python 2>&1
```

- **What it does:** This command first executes the 'done;' statement from a loop structure, and then uses 'ls' to list the specified python executables, redirecting standard error to standard output.
- **Why:** It confirms that the python interpreters located in the virtual environments for the python-api and collectors directories are accessible in the current shell's PATH context.
- **Example:** done; ls packages/python-api/.venv/bin/python packages/collectors/.venv/bin/python 2>&1
- **Notes:** The 'done;' is likely leftover syntax from a preceding 'for' loop structure. The '2>&1' ensures that any errors (like 'file not found') are printed to the standard output stream along with successful listings.
### Locate all instances of an executable
<!-- sig: 3aa39e96e820 -->

```bash
where.exe godot
```

- **What it does:** This command searches the system's PATH environment variable to find all executable files named 'godot'.
- **Why:** It is useful for confirming which specific version or installation path of an executable is being found by the shell, especially when multiple versions might exist.
- **Example:** where.exe godot to see all installed Godot engine executables.
- **Notes:** This command is specific to Windows environments and uses the 'where.exe' utility.

### Check for existence of multiple executable paths
<!-- sig: 343ced09be69 -->

```bash
'$candidates' = '@(' 'C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe,' 'C:\Program Files (x86)\Steam\steamapps\common\Godot Engine\Godot_v4.7-stable_win64.exe,' 'C:\Program Files\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe' ')' '$found' = '$candidates'
```

- **What it does:** This script block assigns an array containing several potential paths to the variable `$candidates`, and then filters this array to find only the paths that actually exist on the filesystem, storing the results in `$found`.
- **Why:** It systematically checks multiple known locations for a required executable, which is necessary when the exact installation path of a tool like Godot Engine is uncertain.
- **Example:** Running the script block to populate `$found` with valid Godot executables.
- **Notes:** This is a PowerShell snippet. The logic relies on the `Test-Path` cmdlet to validate the existence of each specified path.

### Check existence and retrieve details of a file
<!-- sig: 30709d8c5756 -->
<!-- sig: b809381003cd -->

```bash
$path = 'C:\Users\sraj\.codex\visualizations\2026\09\10\01a08c95-8193-7763-aaa7-3156f1c8763b\circuit-clash-concept.html'; Write-Output 'exists=$(Test-Path -LiteralPath $path)'; if '(Test-Path' -LiteralPath '$path)' '{' Get-Item -LiteralPath '$path'`],
what`
This script first assigns the full path to the variable $path, then outputs a boolean indicating if the path exists, and finally, if it exists, it retrieves item details and the first three lines of content.
```

- **What it does:** This script first assigns the full path to the variable $path, then outputs a boolean indicating if the path exists, and finally, if it exists, it retrieves item details and the first three lines of content.
- **Why:** It combines path checking, metadata retrieval, and content preview into a single, conditional block.
- **Example:** Running the command with the specified path will output the existence status and file details for circuit-clash-concept.html.
- **Notes:** The script uses PowerShell syntax and relies on the variable $path being correctly set to the target file's absolute path.

### Retrieve metadata for multiple files
<!-- sig: 3ec4563bf4f7 -->
<!-- sig: e3b61c377491 -->
<!-- sig: 3005d960c354 -->

```bash
Get-Item -LiteralPath '$doc,$image'
```

- **What it does:** Retrieves system information for the specified files, which are passed as a comma-separated list to the -LiteralPath parameter.
- **Why:** This is a direct way to check the existence and basic properties of multiple, potentially disparate files in one call.
- **Example:** Get-Item -LiteralPath 'D:\git_apps\games\NeonBlocks\design\CIRCUIT_CLASH_VISION.md','D:\git_apps\games\NeonBlocks\design\references\circuit-clash-3d-concept.png'
- **Notes:** The -LiteralPath parameter is used here to correctly handle the comma separation of multiple paths without PowerShell interpreting the comma as a separator for multiple arguments.

## Searching

### Find which files contain a string
<!-- sig: 3766104d2079 -->
<!-- sig: 973cd4561d55 -->
<!-- sig: 82bde54e21ec -->
<!-- sig: 1e8bbf573275 -->
<!-- sig: 01fcc7770651 -->
<!-- sig: 1b517f08b389 -->
<!-- sig: 792202ff3716 -->
<!-- sig: 1f5a23e612a7 -->
<!-- sig: 59f992bb3ca0 -->
<!-- sig: aad1601858a3 -->
<!-- sig: e4ade2248554 -->
<!-- sig: c8fc248ba9ea -->
<!-- sig: 8993a959a674 -->
<!-- sig: ebce53ec9db2 -->
<!-- sig: c25075dcc7ec -->
<!-- sig: ec43ba54700b -->
<!-- sig: 06b772db48c9 -->
<!-- sig: 729e4466505e -->
<!-- sig: 9a7734ab0654 -->
<!-- sig: c5d796803371 -->
<!-- sig: b478343f7129 -->
<!-- sig: 997456708376 -->
<!-- sig: 6cd2c2b3cf1e -->
<!-- sig: c751884d4dd9 -->
<!-- sig: 2d4c4b3e0bd9 -->
<!-- sig: 260d1d4a1a57 -->
<!-- sig: 6ef2d7f08a9e -->
<!-- sig: fdee19b6f362 -->
<!-- sig: 9ed5228cf855 -->
<!-- sig: 04ae032eac24 -->
<!-- sig: 65c82a294c52 -->
<!-- sig: d3cce9026ecc -->
<!-- sig: cab4ab23425f -->
<!-- sig: d67212649ec7 -->
<!-- sig: 56989b69bc8e -->
<!-- sig: fa0bd7643353 -->
<!-- sig: 7f60f43382d1 -->
<!-- sig: 34be2d8cc1c2 -->
<!-- sig: 8c5f377b58e2 -->
<!-- sig: 5a257249afa4 -->
<!-- sig: cac3368f033c -->
<!-- sig: bf6f8cbd7396 -->
<!-- sig: bcafc4986bd9 -->
<!-- sig: 64c1418f1f1a -->
<!-- sig: 6f1da292f03a -->
<!-- sig: 0da9991593b7 -->
<!-- sig: 4d7427d9770b -->
<!-- sig: 6e048a02e77f -->
<!-- sig: 87c611a212ee -->
<!-- sig: 8e19470a8e61 -->
<!-- sig: 9cc070eab2ae -->
<!-- sig: 01add8a7b723 -->
<!-- sig: e3ed4e9ca0b1 -->
<!-- sig: 5bfce61cb2c9 -->
<!-- sig: fab9de1cb4e8 -->
<!-- sig: 38d1ec76e865 -->
<!-- sig: d4d8026a90e6 -->
<!-- sig: b722817cc759 -->
<!-- sig: 7e43f6c6999d -->
<!-- sig: ed2a3b41d429 -->
<!-- sig: d69bf035523b -->
<!-- sig: d9300e7fe3da -->
<!-- sig: 530944428266 -->
<!-- sig: 011e2250eab3 -->
<!-- sig: ae5218129dcb -->
<!-- sig: 3d037bebd9eb -->
<!-- sig: aa3dfe14559c -->
<!-- sig: 798dc93aa4a4 -->
<!-- sig: 2bd0700383fc -->
<!-- sig: b055ea19f0de -->
<!-- sig: 790f8d56e3e7 -->
<!-- sig: 3c093ddb7b0d -->
<!-- sig: 431396ba3a9a -->
<!-- sig: 7194f39999b6 -->
<!-- sig: ca89eacc1d94 -->
<!-- sig: adebb45f7edf -->
<!-- sig: 36771490d03c -->
<!-- sig: 3385b4abc769 -->
<!-- sig: c0f62a3a89d6 -->
<!-- sig: 143098826697 -->
<!-- sig: 6a6f5f4942dc -->
<!-- sig: 9bc60d4385f4 -->
<!-- sig: e15d40acd641 -->
<!-- sig: c8d38076c8fe -->
<!-- sig: ac09314864ba -->
<!-- sig: 70421277a822 -->
<!-- sig: 2944029bcd2d -->
<!-- sig: 7aff3d4a5d28 -->
<!-- sig: e911121b8b42 -->
<!-- sig: 3ee304ec8f47 -->
<!-- sig: 9860d6820ca9 -->
<!-- sig: 68bed290e21e -->
<!-- sig: 96b8df239a81 -->
<!-- sig: a4bb484bfed6 -->
<!-- sig: f1fa987aecaf -->
<!-- sig: 21e2a3eb3346 -->
<!-- sig: 48ab78df0e1c -->
<!-- sig: c3c212ae0a5e -->
<!-- sig: e4c6eed3d087 -->
<!-- sig: 25d302df5a12 -->
<!-- sig: 8dbf276d0a3f -->
<!-- sig: 106fcf125be8 -->
<!-- sig: fab555e0f954 -->
<!-- sig: 5128e3af2b07 -->
<!-- sig: 83b37b05758d -->
<!-- sig: e9cf0e25f903 -->
<!-- sig: 2cd90eafc3e8 -->
<!-- sig: 8c8d2a3d784f -->
<!-- sig: 5e2d8ce22cb1 -->
<!-- sig: 13dd3e495db9 -->
<!-- sig: 3718ec9b8e67 -->
<!-- sig: 9fa095dd9999 -->
<!-- sig: 912768b55887 -->
<!-- sig: 31993381e526 -->
<!-- sig: bc5bb0e6f1ce -->
<!-- sig: d27d8f3b3559 -->
<!-- sig: 4af5980c3e06 -->
<!-- sig: 592938ed113a -->
<!-- sig: 5d4f76a3704e -->
<!-- sig: cb034de033fa -->
<!-- sig: 14a8e7c1e630 -->
<!-- sig: fb20e54b8e4f -->
<!-- sig: cbed29cc49d0 -->
<!-- sig: 986049beb42c -->
<!-- sig: f42b4c581299 -->
<!-- sig: 002dac60b41b -->
<!-- sig: 23425bf17522 -->
<!-- sig: 0fdef95226ae -->
<!-- sig: 5b0905abe76e -->
<!-- sig: 49d1e38c7e23 -->
<!-- sig: 70efa2765ff6 -->
<!-- sig: 294fd6aefcc8 -->
<!-- sig: c8ba13b98597 -->
<!-- sig: 57c927c6573e -->
<!-- sig: d00529881016 -->
<!-- sig: 2ed61707bdcb -->
<!-- sig: 3cc8b69c645e -->
<!-- sig: fd60ed3607cb -->
<!-- sig: e94bc8a45063 -->
<!-- sig: cb034de033fa -->
<!-- sig: ec43ba54700b -->
<!-- sig: 06b772db48c9 -->
<!-- sig: 718533df33c1 -->
<!-- sig: d27d8f3b3559 -->
<!-- sig: c751884d4dd9 -->
<!-- sig: 881e01afe6c8 -->
<!-- sig: ad126d107e54 -->
<!-- sig: 2d99f065df7f -->
<!-- sig: 2d4c4b3e0bd9 -->
<!-- sig: fdee19b6f362 -->
<!-- sig: bc09f56f77cf -->
<!-- sig: 3c2d76ee8b0e -->
<!-- sig: fb1fef807332 -->
<!-- sig: 79402b8b748e -->
<!-- sig: 01add8a7b723 -->
<!-- sig: 68bed290e21e -->
<!-- sig: ae5218129dcb -->
<!-- sig: 4eb77e4bf771 -->
<!-- sig: f73438a80050 -->
<!-- sig: 5c03f0a3d424 -->
<!-- sig: 85ffbe223e18 -->
<!-- sig: 529576d0c3ad -->
<!-- sig: 0f790ff6b333 -->
<!-- sig: 6ff19f276b91 -->

```bash
rg -l -e 'ENTRA_REFRESH_TOKEN'
```

- **What it does:** ripgrep searches recursively from the current directory and lists only matching file paths (`-l`).
- **Why:** The fastest first step in an unfamiliar codebase; respects `.gitignore` so it skips `node_modules` and build output automatically.
- **Notes:** `-e` makes the pattern explicit, so patterns starting with `-` are not read as flags.

### Read matches with surrounding context
<!-- sig: fe6d68ce019c -->
<!-- sig: d43fbdff6730 -->
<!-- sig: c7fe5d5b1975 -->
<!-- sig: 5767f3160945 -->

```bash
rg -n -C 3 -e 'AppError'
```

- **What it does:** Prints matching lines with line numbers (`-n`) and 3 lines of context either side (`-C`).
- **Why:** Usually enough to understand a usage without opening the file.
- **Variants:** `-B`/`-A` for context before/after only; `-w` for whole-word matches; `-F` for a literal (non-regex) pattern; `-i` for case-insensitive matches. Combine with `-g` to scope the search: `rg -C 2 -g '*.ts' -e AppError`.
- **Notes:** Devin's `grep` tool is this command — same flags, size-capped output, no shell permission needed.

### Count occurrences per file
<!-- sig: f67b2c5729f9 -->

```bash
rg -c -e 'TODO'
```

- **What it does:** Prints `path:count` for each file with at least one match.
- **Why:** Quantifies how widespread a pattern is before a refactor, without printing thousands of lines.

### Restrict a search to one file type
<!-- sig: 6cfdf3177aac -->

```bash
rg -g '*.ts' -e 'useEffect'
```

- **What it does:** Applies a glob filter to the file set (`-g '!dist/**'` excludes instead).
- **Why:** Cuts noise from tests, fixtures, lockfiles and generated code.
- **Notes:** Quote the glob so the shell does not expand it. ripgrep uses Rust regex syntax — no look-around or backreferences.

### List files by name pattern
<!-- sig: eea743fc2d09 -->

```bash
rg --files -g '**/*.md'
```

- **What it does:** Lists files ripgrep would search, filtered by glob — a fast, gitignore-aware `find`.
- **Why:** Much faster than `find` in a repo and it skips ignored directories by default.

### Find files by name with plain find
<!-- sig: 3f7002092115 -->

```bash
find . -name '*.sql'
```

- **What it does:** Walks the tree and prints paths matching the name pattern.
- **Why:** Available everywhere, and it *does* traverse gitignored directories, which is exactly what you need when hunting build artefacts.
- **Notes:** Prefer `rg --files` in repos. Add `-maxdepth 2` to keep it shallow, `-type f` to skip directories.

### Filter a stream of text case-insensitively
<!-- sig: 5025ff9f1a46 -->

```bash
... 2>&1 | grep -i commitscope
```

- **What it does:** Searches each line of a piped input for a pattern, ignoring case (`-i`), and prints only the matching lines.
- **Why:** Quick filter when the exact casing in logs or test output is unknown or varies, without the power-user flags of `rg`.
- **Example:** `python3 tool/tests/test_portable.py 2>&1 | grep -i commitscope`.
- **Notes:** Plain `grep` is not gitignore-aware and does not support `rg`'s rust-regex restrictions; use `grep -i` for one-off pipelines and `rg -i` for code searches.

### Count matching lines in a queue and pretty-print the most recent record
<!-- sig: ed504be81133 -->
<!-- sig: ae5ce0e27d7a -->
<!-- sig: be439772421c -->
<!-- sig: c653bf5c9b23 -->
<!-- sig: c9c6bf7b6c87 -->
<!-- sig: dd15c115c28c -->
<!-- sig: fa83a0d19dda -->
<!-- sig: 80e6a817b621 -->
<!-- sig: 43979ae77291 -->
<!-- sig: 48da5d02a343 -->
<!-- sig: 516e536c28ad -->
<!-- sig: 61a04308b48f -->
<!-- sig: de50b9f33685 -->
<!-- sig: ca175e357e0a -->
<!-- sig: 643d24ee4f22 -->
<!-- sig: 7d0e7e4d0be9 -->
<!-- sig: c84d74f33425 -->
<!-- sig: 6e34b147fc80 -->
<!-- sig: 2369fc754fad -->
<!-- sig: 19540cf16dd0 -->
<!-- sig: 4eccb6f8888b -->
<!-- sig: 4213dcb504e1 -->
<!-- sig: f9e4734653de -->
<!-- sig: 17db12d642f9 -->
<!-- sig: 4ff16646be64 -->
<!-- sig: 3bef909ad73d -->
<!-- sig: 287e0238deee -->
<!-- sig: 9fdb7457aaad -->
<!-- sig: 26036815c08f -->
<!-- sig: 3c5275bedc88 -->
<!-- sig: ab91a20bc1a2 -->
<!-- sig: a839eaca8317 -->
<!-- sig: 90f932f7c9de -->
<!-- sig: c27076b06b40 -->
<!-- sig: 2bb8a13dc0e7 -->
<!-- sig: 23b1093e5409 -->
<!-- sig: eabfe177f55c -->
<!-- sig: 6d62bcfd5e0e -->
<!-- sig: 45bcebcbb447 -->
<!-- sig: 51a3b5d3c967 -->
<!-- sig: 254c82115196 -->
<!-- sig: b507dc31f4ce -->
<!-- sig: e6e101f79b05 -->
<!-- sig: eec5199fda39 -->
<!-- sig: ba1d4baac0ed -->
<!-- sig: 14e0f7cde831 -->
<!-- sig: 3fdcb3e62744 -->
<!-- sig: 6b4d853c96c6 -->
<!-- sig: 32d33f12e97b -->
<!-- sig: d1c106adf931 -->
<!-- sig: c0a3b247f6a9 -->
<!-- sig: f8245c579fb5 -->
<!-- sig: a8e9f78a6f5d -->
<!-- sig: d3a9131c11dc -->
<!-- sig: a9584d431495 -->
<!-- sig: 4bd5732fa6c6 -->
<!-- sig: bc3f4fec9889 -->
<!-- sig: 8f41498823a0 -->
<!-- sig: 0cd18c72d37d -->
<!-- sig: d93cf77896f1 -->
<!-- sig: 108a6d1371e4 -->
<!-- sig: d65c10a4fc80 -->
<!-- sig: cb1e7164abe4 -->
<!-- sig: 53861bd26d7e -->
<!-- sig: d95b93d878ba -->
<!-- sig: 67dd1e541b18 -->
<!-- sig: fb56986a10f4 -->
<!-- sig: 101ca83a005e -->
<!-- sig: 395e085f9531 -->
<!-- sig: 5037c99d331d -->
<!-- sig: b4702b25cde7 -->
<!-- sig: 4b25564d3c9f -->
<!-- sig: ffad51c00b94 -->
<!-- sig: 1336fe281252 -->
<!-- sig: 52055f2a2637 -->
<!-- sig: e0599284bf19 -->
<!-- sig: b9c604d48bb9 -->
<!-- sig: 9aeda824e14c -->
<!-- sig: 3dabab5d9bb7 -->
<!-- sig: 907b7f07b34e -->
<!-- sig: e1567373f697 -->
<!-- sig: c51efc6b29d1 -->
<!-- sig: abf78f2abf04 -->
<!-- sig: a8549dd1aef6 -->
<!-- sig: 1fa297eaf651 -->
<!-- sig: 72b3ca764815 -->
<!-- sig: b2dbe2262d45 -->
<!-- sig: 1777ad5edda9 -->
<!-- sig: 3dfd3f820260 -->
<!-- sig: 3f9de281dba0 -->
<!-- sig: 3042437ee73d -->
<!-- sig: 12f211f8eb16 -->
<!-- sig: 4a5de1378e97 -->
<!-- sig: d00aaab27726 -->
<!-- sig: 2ac94ea36937 -->
<!-- sig: e40e4cedd069 -->
<!-- sig: c2e1576039c3 -->
<!-- sig: c0ce5cf7d0a4 -->
<!-- sig: 69da3cae462b -->
<!-- sig: 2c86870c5861 -->
<!-- sig: c2fa32f8a291 -->
<!-- sig: 5c0162ed1204 -->
<!-- sig: 18b44501e32b -->
<!-- sig: aadd2ab1223f -->
<!-- sig: d342f837b456 -->
<!-- sig: 4f783a701f4a -->
<!-- sig: 0ab50eae987a -->
<!-- sig: cb35e31d78d3 -->
<!-- sig: 2e8c8e26dfc3 -->
<!-- sig: 05a8bf7039b6 -->
<!-- sig: bf7dc411d562 -->
<!-- sig: b834a5e03f76 -->
<!-- sig: 43fd1f66baa6 -->
<!-- sig: 9b996d182c21 -->
<!-- sig: 44a44bf2f636 -->
<!-- sig: 7cb99961cf40 -->
<!-- sig: 0c995b36543e -->
<!-- sig: 36671c158019 -->
<!-- sig: 9e996b507e70 -->
<!-- sig: 7b1e89d8cb9a -->
<!-- sig: d69ed289f311 -->
<!-- sig: ad6e09ff5188 -->
<!-- sig: 74cd77fe5eae -->
<!-- sig: 491ef03f5a3d -->
<!-- sig: 6fb5bd780a10 -->
<!-- sig: 0e2ada6fe87f -->
<!-- sig: 030bf3084d2e -->
<!-- sig: 07f657ac8b0c -->
<!-- sig: a62d6aa81555 -->
<!-- sig: 84b05e28f1e7 -->
<!-- sig: e7dfdc4a1d0e -->
<!-- sig: a84d18b39101 -->
<!-- sig: 2f67d509232f -->
<!-- sig: 067834364c72 -->
<!-- sig: e2d244ec26c9 -->
<!-- sig: 4b7e827540be -->
<!-- sig: 7e2e75b26404 -->
<!-- sig: 6de92ccacf99 -->
<!-- sig: 0cd831b1a682 -->
<!-- sig: 69acfa5e2188 -->
<!-- sig: 89a9ce368faa -->
<!-- sig: 67cea2cd97cb -->
<!-- sig: 93a59fe82999 -->
<!-- sig: 19628cdab69a -->
<!-- sig: 50d2750020ab -->
<!-- sig: 3ef330873830 -->
<!-- sig: b83acbe643c0 -->
<!-- sig: 2519fcd9c312 -->
<!-- sig: 4fef36fdcba1 -->
<!-- sig: d0f8e94786ef -->
<!-- sig: f4a2afc8aa25 -->
<!-- sig: c052b214258b -->
<!-- sig: b62bc26494b1 -->
<!-- sig: 7bbfa049982c -->
<!-- sig: b6c15a69146d -->
<!-- sig: 5cb048396132 -->
<!-- sig: 5849effd2430 -->
<!-- sig: bf9a81d671a1 -->
<!-- sig: 0fd2c82af086 -->
<!-- sig: 8b6542c442ca -->
<!-- sig: b20e873bc987 -->
<!-- sig: 4f7e4e6db60f -->
<!-- sig: f9a5cd905839 -->
<!-- sig: e58319f9da3e -->
<!-- sig: 045ecc5e799e -->
<!-- sig: 9649733cdd4e -->
<!-- sig: feec3f3aec78 -->
<!-- sig: 48f07c4bac8e -->
<!-- sig: d9f3c66e973d -->
<!-- sig: 9e447d471f66 -->
<!-- sig: 192fc6c62327 -->
<!-- sig: 66142ba507d4 -->
<!-- sig: 676dbe604803 -->
<!-- sig: ecc5a1dc805c -->
<!-- sig: e5f58e11b58b -->
<!-- sig: 8d8384ac01e3 -->
<!-- sig: ee387202cd1e -->
<!-- sig: d5a22e477874 -->
<!-- sig: 5637e4672dd8 -->
<!-- sig: 18bffd43bdcd -->
<!-- sig: 7099bb4471d9 -->
<!-- sig: 61ee28139b0e -->
<!-- sig: 74cf7b6cfde3 -->
<!-- sig: 16d153859b39 -->
<!-- sig: 3f5997eb55cd -->
<!-- sig: 54e23f40f318 -->
<!-- sig: 207c0b17ed17 -->
<!-- sig: 36ae1efb9c93 -->
<!-- sig: 38c772e88fef -->
<!-- sig: 2b3707fbbd9a -->
<!-- sig: a126c9cac810 -->
<!-- sig: 9b88d2b990c1 -->
<!-- sig: 06d996c3be91 -->
<!-- sig: b5188d72185b -->
<!-- sig: ae132de33bbf -->
<!-- sig: 68a026340171 -->
<!-- sig: d3bc60e1cb79 -->
<!-- sig: 6b82bc7fa277 -->
<!-- sig: dda262d8d3b4 -->
<!-- sig: e6fc73bb2dd3 -->
<!-- sig: 2d45f2dc1f9b -->

```bash
grep -c <pattern> <queue-file> 2>/dev/null
tail -n 1 <queue-file> | python3 -m json.tool
```

- **What it does:** `grep -c` returns the number of lines matching `<pattern>` in the queue file; `tail -n 1` extracts the last queued record and `python3 -m json.tool` formats it as readable JSON.
- **Why:** A quick sanity check when verifying a captured event landed in the queue and inspecting the latest entry.
- **Example:** `grep -c cargo .runtime/pending.jsonl 2>/dev/null; tail -n 1 .runtime/pending.jsonl | python3 -m json.tool`.
- **Variants:** `grep -c 'sig:' git.md` counts the dedupe-signature lines in a knowledge-base file.
- **Notes:** `2>/dev/null` on the first command keeps a missing queue file from producing an error; `python3 -m json.tool` fails if the last line is not valid JSON.

### Show matching lines with context using grep
<!-- sig: 14443ee0d76a -->

```bash
grep -B 2 -A 2 'pattern' <file>
```

- **What it does:** Prints each matching line of `<file>` plus 2 lines before (`-B`) and 2 lines after (`-A`).
- **Why:** Quick context view in a single known file, without ripgrep's `.gitignore` handling or opening an editor.
- **Example:** `grep -B 2 -A 2 'class User' src/models.py`
- **Notes:** `grep` uses basic/extended regex; use `-F` for a literal pattern. Combine `-B`/`-A` or use `-C 2` for symmetric context.

### Find all occurrences of specific text patterns
<!-- sig: cf1902996385 -->

```bash
findstr /n "/c:case \"sage\"" /c:handleSage devtrack_clientcli.go
```

- **What it does:** Searches the file devtrack_clientcli.go for lines containing both the case-insensitive string "sage" and the string "handleSage".
- **Why:** This is used to quickly locate all instances of specific code patterns across a single source file without using a full-text search tool.
- **Example:** findstr /n "/c:case \"sage\"" /c:handleSage devtrack_clientcli.go
- **Notes:** The /n flag prefixes each line with its line number, and the /c: flag specifies a literal string to search for.

### Find common names between two directories
<!-- sig: 0e9920bbcf39 -->
<!-- sig: 24c901772bc0 -->

```bash
comm -12 <(ls .kiro/specs | sort) <(ls .github/specs | sort)
```

- **What it does:** Compares two sorted lists of filenames, printing only lines unique to both inputs. The input lists are generated by listing and sorting the contents of the respective directories.
- **Why:** This is a concise way to find the intersection of two sets of filenames without needing an intermediate file or multiple pipes.
- **Example:** comm -12 <(ls .kiro/specs | sort) <(ls .github/specs | sort) to see specs present in both directories.
- **Notes:** The use of process substitution (<(...)) is crucial here to feed the sorted output of `ls` directly into `comm`.

### List router definitions in a specific file
<!-- sig: 38407afcae3f -->
<!-- sig: 44e788e44f95 -->
<!-- sig: b165e93675a2 -->
<!-- sig: 3271f067145c -->
<!-- sig: d65ff591906e -->
<!-- sig: b2cb3bb4da8a -->
<!-- sig: d648e28847c7 -->
<!-- sig: b790725ca43c -->
<!-- sig: ea74e22f8209 -->
<!-- sig: 5f50432b9714 -->
<!-- sig: 8668e0e235ba -->
<!-- sig: 89bd6fb51ef5 -->
<!-- sig: 8056e1445ecb -->
<!-- sig: 191e3ffbccd6 -->
<!-- sig: 9cf011cfa81a -->
<!-- sig: e4bca11f4ec9 -->
<!-- sig: 6568b385d28a -->
<!-- sig: de78708f2349 -->
<!-- sig: 36e0741739d5 -->
<!-- sig: f3d9dc0f2ff3 -->
<!-- sig: 3d7e56d5bdc5 -->
<!-- sig: 22879f246b23 -->
<!-- sig: c49a89d51173 -->
<!-- sig: c368bad92a36 -->
<!-- sig: 65e0ea6fe7e7 -->
<!-- sig: 3f34d7e64cf8 -->
<!-- sig: a19009a4302c -->
<!-- sig: 07235a45cff2 -->
<!-- sig: a322dfa0d98d -->
<!-- sig: 5bf5279f390b -->
<!-- sig: 001d7174ae84 -->
<!-- sig: 0f7121f675d7 -->
<!-- sig: d7595936a1d7 -->
<!-- sig: 8a4c4ddc9a3d -->
<!-- sig: 1f0a55c6d0e7 -->
<!-- sig: 1f63dfd28e4f -->
<!-- sig: 0aa9b0fc6282 -->
<!-- sig: 1578f61914b3 -->
<!-- sig: 11939a60b06a -->
<!-- sig: bcac168a424e -->
<!-- sig: 71fb5eb0851c -->
<!-- sig: 70a3388a413e -->
<!-- sig: 68fa9a303c76 -->
<!-- sig: 8a1fbc69472f -->
<!-- sig: f87d2e9d03e5 -->
<!-- sig: 82e8705a417f -->
<!-- sig: ac391c0fbe18 -->
<!-- sig: 1ad2798ac085 -->
<!-- sig: 4a551f0b5cff -->
<!-- sig: 2d087c7f3bd7 -->
<!-- sig: fd8d55021b1b -->
<!-- sig: 33d39d669e97 -->
<!-- sig: 011bfe6789e8 -->
<!-- sig: 97c77bbfe5e4 -->
<!-- sig: a04db5381d6e -->
<!-- sig: 13b036f1c508 -->
<!-- sig: 97f5c730b5c4 -->
<!-- sig: 4ed1b3e55376 -->
<!-- sig: fc17abff9387 -->
<!-- sig: 6660d5e09648 -->
<!-- sig: c55f32b835fe -->
<!-- sig: c0be120eecf2 -->
<!-- sig: b7d9786509d0 -->

```bash
head;
echo '=== routers registered in python-api main.py ===';
rg -n 'include_router|prefix=' packages/python-api/main.py
```

- **What it does:** The command first outputs nothing via head, then prints a header string, and finally uses ripgrep to find lines containing 'include_router' or 'prefix=' in packages/python-api/main.py, showing line numbers (-n).
- **Why:** This sequence is used to systematically check for specific patterns related to API routing definitions within a core file, providing context via line numbers.
- **Example:** head; echo '=== routers registered in python-api main.py ==='; rg -n 'include_router|prefix=' packages/python-api/main.py
- **Notes:** The initial 'head;' command is likely a placeholder or artifact from a larger script execution and does not perform a useful action on its own.

### View the contents of a specific file revision
<!-- sig: bef51a327269 -->

```bash
git show 39a6884 -- packages/python-api/services/dashboard_service.py
```

- **What it does:** This command uses git show to display the content of the file packages/python-api/services/dashboard_service.py as it existed at the specific commit hash 39a6884.
- **Why:** It allows inspection of a file's state at a precise point in history without needing to check out the entire commit.
- **Example:** git show 39a6884 -- packages/python-api/services/dashboard_service.py to review the API service structure from last week's build.
- **Notes:** The preceding 'cat;' suggests this command was chained after another command's output, likely for piping or sequential execution.

### Find the path to a specific file
<!-- sig: a2f0229f6273 -->

```bash
f=$(git ls-files 'packages/frontend/src/**/EIRnDTopLevelKPISection.tsx')
```

- **What it does:** Executes git ls-files to list the path of a file matching the glob pattern 'packages/frontend/src/**/EIRnDTopLevelKPISection.tsx' and stores the output in the variable f.
- **Why:** This isolates the exact path of a file within the repository that needs to be passed to subsequent commands for analysis.
- **Example:** f=$(git ls-files 'packages/frontend/src/**/EIRnDTopLevelKPISection.tsx')
- **Notes:** The variable f will contain the relative path to the file if it exists in the index, or it will be empty if git finds no matches.

### Find lines containing specific async database operations
<!-- sig: 99bec622b75a -->
<!-- sig: fd9a6493c9f0 -->
<!-- sig: ab1954254bdc -->
<!-- sig: 780e9d9b84f5 -->
<!-- sig: 57676cd22e53 -->
<!-- sig: c2bf72dbee50 -->
<!-- sig: 6c79833a935f -->
<!-- sig: 859859c306fe -->
<!-- sig: 6b8f5c7eb661 -->

```bash
cat; grep -n 'async \(upsert\|insert\|record\|save\|replace\[A-Za-z]*(' packages/backend/src/services/collector.service.ts
```

- **What it does:** This command pipes the output of `cat;` (which seems to be a placeholder or artifact) into `grep`, which then searches for lines containing specific patterns related to async database operations within the specified service file.
- **Why:** It allows for a targeted search across a potentially large file for specific function call patterns related to data persistence.
- **Example:** cat; grep -n 'async \(upsert\|insert\|record\|save\|replace\[A-Za-z]*(' packages/backend/src/services/collector.service.ts
- **Notes:** The initial `cat;` segment is unusual; ensure it correctly pipes the intended content or remove it if the search should only run on the file content.
### Filter directory items by name pattern
<!-- sig: 1efdf5d03996 -->
<!-- sig: b77c48f66493 -->
<!-- sig: f10d31c96434 -->
<!-- sig: 425b190db584 -->
<!-- sig: ac4e54c52278 -->
<!-- sig: 88ab555c0a86 -->
<!-- sig: 5c50440ede16 -->
<!-- sig: 5b2708537b01 -->
<!-- sig: d5dacf99b6cf -->
<!-- sig: 4eb4aa032466 -->

```bash
Where-Object Name -Match Godot
```

- **What it does:** Filters the incoming pipeline objects, keeping only those where the Name property matches the regular expression 'Godot'.
- **Why:** It allows for precise filtering of directory listings based on a pattern, which is more flexible than simple equality checks.
- **Example:** Get-ChildItem -LiteralPath 'D:\Program Files (x86)\Steam\steamapps\common' -Directory | Where-Object Name -Match 'Godot'
- **Notes:** This command is typically piped from another cmdlet like Get-ChildItem. The pattern 'Godot' is treated as a regex.

## Editing and transforming text

### Print a specific line range of a file
<!-- sig: 1a0e82d71c4c -->
<!-- sig: ad370f088bbe -->
<!-- sig: b71a518b6252 -->
<!-- sig: 43fc5c67155a -->
<!-- sig: 310a312f5620 -->
<!-- sig: 7d68cfe2eb43 -->
<!-- sig: 715999b4e6d1 -->
<!-- sig: 6bcdbcf49f78 -->
<!-- sig: 705fa62c22fe -->
<!-- sig: bde7ed565407 -->
<!-- sig: 753dd2030933 -->
<!-- sig: 8332c5c2ca30 -->
<!-- sig: 2e450146132e -->
<!-- sig: 9f51f73c741d -->
<!-- sig: 49684849f9d8 -->
<!-- sig: 438fb1624da6 -->
<!-- sig: 3d68ce9b57c3 -->
<!-- sig: ad2ebd8965cb -->
<!-- sig: eea304383336 -->
<!-- sig: e6c8c849b03a -->
<!-- sig: e0e6a1cbca13 -->
<!-- sig: 13498a2f2d74 -->
<!-- sig: e0437a1979e2 -->
<!-- sig: ce1a55378ae9 -->
<!-- sig: 096d25e7fe5d -->
<!-- sig: 3ae9977da606 -->
<!-- sig: 0806b0245059 -->
<!-- sig: 8faed42c4cf0 -->
<!-- sig: 583c5f5f3c54 -->
<!-- sig: 3f45e7b40ddf -->
<!-- sig: fce148e23f49 -->
<!-- sig: a248d9f43de2 -->
<!-- sig: d42e7e3dc790 -->
<!-- sig: 323a5ce3b761 -->
<!-- sig: 8c0ffc3077ca -->
<!-- sig: a889d6979373 -->
<!-- sig: 57f95128fc14 -->
<!-- sig: 2d51474f2774 -->
<!-- sig: f3a199a6515a -->
<!-- sig: 3de980cac5ba -->
<!-- sig: 2acb30944de1 -->
<!-- sig: 0f35fc589449 -->
<!-- sig: 18429e96bc9c -->
<!-- sig: 4dd2002baf8a -->
<!-- sig: 7807995db79d -->
<!-- sig: aa9a83d91383 -->
<!-- sig: cf17b414ba1a -->
<!-- sig: 4f741e555ff0 -->
<!-- sig: 291840b740e6 -->

```bash
sed -n '10,40p' packages/backend/src/app.ts
```

- **What it does:** `-n` suppresses default output; `10,40p` prints only lines 10–40.
- **Why:** Reads one region of a large file without loading the whole thing.
- **Example:** `sed -n '95,106p;234,241p' file.txt` prints two ranges in one call.

### Replace text in place across a file
<!-- sig: d1d7b143cab3 -->

```bash
sed -i '' 's/oldName/newName/g' src/config.ts
```

- **What it does:** Substitutes every occurrence and writes the file back.
- **Why:** Mechanical rename across a file without opening an editor.
- **Notes:** **macOS/BSD `sed` requires an argument to `-i`** — `-i ''` means "no backup". GNU/Linux `sed` uses bare `-i`, so the same command is not portable. Always check the diff afterwards; regex substitution has no undo.

### Extract a field from JSON
<!-- sig: aac5bb852b5b -->

```bash
jq -r '.agent.model' ~/.config/devin/config.json
```

- **What it does:** Parses JSON and prints the selected value; `-r` emits raw strings without quotes.
- **Why:** Safe way to read config values in scripts instead of grepping JSON.
- **Notes:** Not installed everywhere. `python3 -m json.tool` or a short `python3 -c` is a dependency-free fallback.

### Sort lines from standard input
<!-- sig: d50c3e910bfb -->

```bash
... | sort
```

- **What it does:** Reads text from stdin and prints it in ascending alphabetical order, one line at a time.
- **Why:** The easiest way to turn an unsorted list of files or lines into a stable, readable list.
- **Example:** `find . -path ./.git -prune -o -type f -print | sort`

### Convert newlines to spaces for listing files
<!-- sig: cc7e7ace2e72 -->
<!-- sig: 1b2c7e5802c2 -->
<!-- sig: b73137923d8d -->
<!-- sig: 3e70690c1713 -->
<!-- sig: f1119d2cb0fc -->
<!-- sig: ec1ab66550ec -->
<!-- sig: cb1aa3f1a328 -->
<!-- sig: d21c989ebd43 -->
<!-- sig: 452fe0e65bd8 -->

```bash
tr '\n' ' '
```

- **What it does:** The 'tr' command translates or deletes characters; here, it replaces every newline character ('\n') with a space (' ').
- **Why:** When piping the output of 'ls *.md' (which lists files on separate lines), using 'tr' joins all filenames onto a single line separated by spaces, making them easier to process by subsequent commands.
- **Example:** ls *.md | tr '\n' ' '
- **Notes:** The backslashes around 'n' are necessary to ensure the shell passes the literal newline character to 'tr'.

### Extract the second column from input
<!-- sig: a79870422aec -->
<!-- sig: 3d05d9b6c084 -->
<!-- sig: 98ce6af0edf3 -->
<!-- sig: 202ead9aac48 -->
<!-- sig: 469bb57fe02b -->
<!-- sig: 9031bedb1685 -->
<!-- sig: 2cc55bb7045c -->
<!-- sig: 7f6463fae889 -->
<!-- sig: 0f507ef95258 -->
<!-- sig: f54b1172a6d4 -->
<!-- sig: 5e84d732ec6e -->
<!-- sig: fa9fc58114e2 -->
<!-- sig: 758a41994c4f -->

```bash
awk '{print $2}'
```

- **What it does:** This command processes input line by line and prints only the second field, assuming fields are separated by whitespace.
- **Why:** It is used here to isolate specific data points (like binary names) from the output of another command before further processing like sorting or counting.
- **Example:** python3 tool/bin/kb.py routes | awk '{print $2}'
- **Notes:** The input to awk must be piped from another command, and it relies on the default field separator (whitespace).

### Count unique occurrences of items
<!-- sig: c316e5c014c9 -->
<!-- sig: c1b44b2196b6 -->
<!-- sig: 35874b084eac -->
<!-- sig: b5fbccbcfbaf -->
<!-- sig: ee94a4a7fe3a -->
<!-- sig: 1419a3abe863 -->

```bash
uniq -c
```

- **What it does:** Reads lines from standard input and prepends the count of consecutive identical lines to each unique line.
- **Why:** It is used here after piping the output of `awk` to count how many times each unique binary route appears in the list.
- **Example:** python3 tool/bin/kb.py routes | awk '{print $2}' | sort | uniq -c
- **Notes:** This command must be preceded by `sort` to group identical lines together, which is required for `uniq` to function correctly.

### Count and sort unique items numerically
<!-- sig: 7c95b0c9c705 -->
<!-- sig: d15534cee302 -->
<!-- sig: aaed86e91831 -->
<!-- sig: 438800df0f7c -->
<!-- sig: 112407908526 -->
<!-- sig: 41ecb73b0ccf -->
<!-- sig: ccbb38249cb1 -->
<!-- sig: 9c48e18ae5ec -->
<!-- sig: be1ea9c075a6 -->
<!-- sig: 05ba1328897e -->
<!-- sig: cefe0209cf22 -->
<!-- sig: 0cddd3528528 -->
<!-- sig: d30d540d5b55 -->
<!-- sig: 53f36cd23aa9 -->
<!-- sig: 022c35b8aaf7 -->

```bash
sort -rn
```

- **What it does:** Sorts the input lines numerically (-n) and in reverse order (-r), placing the highest counts at the top.
- **Why:** This is used after counting unique items with 'uniq -c' to easily see which items appeared most frequently.
- **Example:** python3 tool/bin/kb.py routes | awk '{print $2}' | sort | uniq -c | sort -rn
- **Notes:** The '-n' flag ensures proper numeric sorting, and '-r' reverses the order so the largest numbers appear first.

### Sort the output of a previous command
<!-- sig: ac5752fc7662 -->
<!-- sig: d579cb775220 -->
<!-- sig: 3a49e3015a2b -->
<!-- sig: b263de417dc4 -->

```bash
sort-object
```

- **What it does:** This cmdlet sorts the incoming objects from the pipeline based on the specified property or object structure.
- **Why:** It provides structured, predictable ordering to data streams coming from other commands, which is often necessary for reliable processing.
- **Example:** rg --files tool .runtime | Sort-Object
- **Notes:** When used in a pipeline, it processes objects sequentially as they arrive from the preceding command.

### Extract the first sixteen characters from output
<!-- sig: 79b742bba9d8 -->
<!-- sig: fa1447609ab6 -->
<!-- sig: b0237c310488 -->
<!-- sig: 7cac9567a1cd -->
<!-- sig: 67b4c84e27a9 -->
<!-- sig: 30253411926c -->
<!-- sig: 98dd5eb24487 -->
<!-- sig: 010bf0b0fa23 -->
<!-- sig: 7a4554576895 -->
<!-- sig: 4296d79fb550 -->
<!-- sig: 51f19afd752c -->
<!-- sig: 3ca34624db8e -->
<!-- sig: 46d5ba5f696a -->
<!-- sig: dbc349fc46c8 -->
<!-- sig: ecdcde78f82a -->
<!-- sig: 32b011efdc67 -->
<!-- sig: 92a59f6b3826 -->
<!-- sig: 079ad9573ed7 -->
<!-- sig: 90455f525a63 -->
<!-- sig: a2d192c3da94 -->
<!-- sig: ab56f07cc824 -->
<!-- sig: a766cfeab108 -->
<!-- sig: 9ea0d660f3ae -->
<!-- sig: 3404051da24d -->
<!-- sig: 896a058e7ed7 -->
<!-- sig: cc4397e7c4af -->
<!-- sig: 64ab76e0f57b -->
<!-- sig: 86d50951754f -->
<!-- sig: 5db7c83fa08c -->
<!-- sig: 90aebdf662e3 -->
<!-- sig: c443357258ea -->
<!-- sig: 949d4f802bd5 -->
<!-- sig: 6454fb1df69b -->
<!-- sig: 1dd1c748eea9 -->
<!-- sig: a346901475c0 -->
<!-- sig: 3e01afba2c3d -->
<!-- sig: 1e96f11dda59 -->
<!-- sig: 199a5cec30ae -->
<!-- sig: 1075d450fee2 -->
<!-- sig: 3064ff67cf86 -->
<!-- sig: 4d1c33565600 -->
<!-- sig: 529001bc80e8 -->
<!-- sig: 27bef73dde5f -->
<!-- sig: 6eea9b4d816b -->
<!-- sig: 0343ea6d32b5 -->
<!-- sig: 827156436555 -->
<!-- sig: c684fbf2ab3d -->
<!-- sig: 334a859f137d -->
<!-- sig: 2343b7d5cdab -->
<!-- sig: c2d36845343d -->
<!-- sig: 7efe43bc155b -->
<!-- sig: 2662b446ca35 -->
<!-- sig: e96f6bc64c65 -->
<!-- sig: 74e9285543e4 -->
<!-- sig: d0a8a2391dbb -->
### Show differences in a specific file
<!-- sig: 51d74c2f296b -->
<!-- sig: d1b4a6c42309 -->
<!-- sig: 10b6f3d6d4db -->

```bash
cmd /c git diff -- README.md
```

- **What it does:** Executes git diff via the Windows command prompt to show unstaged changes between the working directory and the index for README.md.
- **Why:** This explicitly targets a single file's differences, which is useful for reviewing changes in a README before committing, without needing to stage the entire repository.
- **Example:** cmd /c git diff -- README.md to check documentation updates.
- **Notes:** The use of 'cmd /c' is necessary to correctly pass the git command through the Windows shell.

## Files, permissions, network

```bash
cut -c1-16
```

- **What it does:** The cut command extracts specific character ranges from input data. The option -c1-16 specifies characters 1 through 16.
- **Why:** This is used here to truncate long hexadecimal hashes into a fixed, short representation for comparison in the output.
- **Example:** git show cb6dbc0:packages/collectors/config/config.yaml | shasum -a 256 | cut -c1-16
- **Notes:** This command relies on the preceding command (like shasum) piping its output to it.

### Add markdown table content to a file
<!-- sig: c9c620f48dbc -->

```bash
cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF'

### Filter the last few lines of output
<!-- sig: f8b2fc900531 -->

```bash
head)
```

- **What it does:** This command is likely a typo or incomplete snippet, as 'head' typically takes arguments like a file or a number of lines.
- **Why:** It was used in a pipeline to process the output of a preceding command, filtering for specific status indicators.
- **Example:** pytest ... | grep -E "passed|failed|FAILED|Error" | head
- **Notes:** The full context shows this was used to pipe output into 'head', which usually requires arguments like 'head -n 10' to show the first 10 lines, not just 'head)'.

### Write standard input content to a file
<!-- sig: 78b522ad6893 -->
<!-- sig: c1e78e3bb59d -->
<!-- sig: 29131e201163 -->
<!-- sig: 19c9d79c139f -->
<!-- sig: 8da6206d541b -->

```bash
tee /tmp/orphans.txt
```

- **What it does:** Reads data from standard input and writes it both to the specified file, /tmp/orphans.txt, and to standard output.
- **Why:** It allows you to see the output of a command while simultaneously saving that output to a file, which is useful for debugging or logging.
- **Example:** echo 'some content' | tee /tmp/orphans.txt
- **Notes:** If the file /tmp/orphans.txt already exists, tee will overwrite it by default.

### Perform complex find-and-replace operations in a file
<!-- sig: 208a5afa576e -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- `origin` = `sraj-epam/ei-rd-eff-deliverymetrics` — **the fork. Push here.**
- `upstream` = `philips-internal/ei-rd-eff-deliverymetrics` — **the canonical
  repo. NEVER push here, under any circumstances.**
""", """> **Corrected 2026-09-25 for this repository.** This section was copied from
> the dashboard checkout and named the dashboard's remotes. Verified with
> `git remote -v`: this checkout has **only** `origin` =
> `sraj-epam/ei-rd-eff`

"""")
```

- **What it does:** This script reads the content of AGENTS.local.md into a variable, defines a replacement function, and then executes the replacement function to substitute a specific multi-line string with a corrected version.
- **Why:** It allows for complex, context-aware text manipulation within a file that is difficult or impossible to achieve with simple command-line tools like sed.
- **Example:** python3 - <<'EOF' ... (script content) EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the entire Python code block to python3. The replacement function asserts that the old string appears exactly once in the file content before replacing it.

### Convert markdown to a styled HTML file
<!-- sig: e2aa94ae57d0 -->
<!-- sig: bf7ac9b0796a -->
<!-- sig: 87c29ce2a2dd -->
<!-- sig: 10c9c12bcee7 -->

```bash
pandoc '$f.md' -f gfm -t html5 -s --metadata 'pagetitle=$(head -1 $f.md | sed 's/^# //')' -c /tmp/cto-print.css --embed-resources -o '/tmp/$f.html'
```

- **What it does:** Converts a file from GitHub Flavored Markdown (GFM) to a standalone HTML5 document, embedding resources and setting a page title from the first line of the source.
- **Why:** This provides a self-contained, styled HTML output suitable for direct viewing or further processing, unlike simple markdown rendering.
- **Example:** pandoc 'delivery-progress-2026-09-21.md' -f gfm -t html5 -s --metadata 'pagetitle=$(head -1 delivery-progress-2026-09-21.md | sed 's/^# //')' -c /tmp/cto-print.css --embed-resources -o '/tmp/delivery-progress-2026-09-21.html'
- **Notes:** The metadata extraction relies on the first line starting with a single hash (`# `) to set the page title. The output file is placed in /tmp/.

### Convert a document to plain text output
<!-- sig: be0a1424276c -->

```bash
textutil -convert txt -stdout 'Client Observation/delivery-metrics-code-analysis-report.docx'
```

- **What it does:** Converts the specified DOCX file into plain text format and prints the resulting content to standard output.
- **Why:** This allows piping the content of a proprietary document directly into another command or script without saving an intermediate file.
- **Example:** textutil -convert txt -stdout 'Client Observation/delivery-metrics-code-analysis-report.docx' | less
- **Notes:** The -stdout flag ensures the converted text is sent to stdout instead of being saved to a file.

### Number lines in a specific YAML workflow file
<!-- sig: 7646966affff -->

```bash
nl -ba .github/workflows/ci-cd.yml
```

- **What it does:** The nl command numbers all lines (-a) in the file .github/workflows/ci-cd.yml, including blank lines (-b).
- **Why:** This provides a line-numbered view of the workflow file, which is useful for referencing specific lines when debugging or reviewing CI/CD configurations.
- **Example:** nl -ba .github/workflows/ci-cd.yml to see line numbers for the CI/CD workflow.
- **Notes:** The output is often piped to other tools like sed to extract specific ranges of lines.

### Update a specific date range in a markdown file
<!-- sig: aa2a450afba7 -->
### Read the entire content of a markdown file
<!-- sig: f6230d6cef29 -->
<!-- sig: d58da3ef8576 -->
<!-- sig: d80496ea78f0 -->
<!-- sig: 61296789507e -->
<!-- sig: 7404e77209e8 -->
<!-- sig: b3cb264707d3 -->
<!-- sig: 3a2a082c5b15 -->
<!-- sig: c51cb700dbfd -->
<!-- sig: d75e64617e68 -->
<!-- sig: e2a0c2eb09b6 -->
<!-- sig: acff56557f5e -->
<!-- sig: a085508f460a -->
<!-- sig: e5eea2e17a04 -->
<!-- sig: f544816ed122 -->

```bash
sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md
cat >> architecture/00-overview.md <<'EOF'
```

- **What it does:** The first command uses sed to perform an in-place substitution on architecture/00-overview.md, replacing an old date range with a new one. The second command appends content to the same file.
- **Why:** This sequence allows for both targeted text replacement and appending new, structured content (like a new commit log entry) to the same document in one workflow.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes && sed -i '' 's/(change log: 2026-09-28 to 2026-10-16)/(change log: 2026-09-28 to 2026-10-21)/' architecture/00-overview.md && cat >> architecture/00-overview.md <<'EOF'
- **Notes:** The '-i ''' option in sed is necessary for in-place editing on macOS/BSD systems.

### Scan repository and draft standards file
<!-- sig: 77872f8b66da -->
### Create a directory structure forcefully
<!-- sig: 1686ced82075 -->

```bash
New-Item -ItemType Directory -Force -Path 'D:\git\_apps\games\NeonBlocks'
```

- **What it does:** This cmdlet creates a new item, specifically a directory, at the specified path. The -Force parameter ensures that parent directories are created if they do not already exist.
- **Why:** It guarantees the target directory exists without failing if intermediate directories are missing, which is safer than multiple explicit creation steps.
- **Example:** New-Item -ItemType Directory -Force -Path 'D:\git\_apps\games\NeonBlocks' to prepare the destination for new game assets.
- **Notes:** The -Force parameter is crucial here as it allows the command to succeed even if the parent directories in the path do not exist.

### Copy multiple project files to a new location
<!-- sig: e1f5dccd98c8 -->

```bash
Copy-Item -LiteralPath 'D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\project.godot,D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\main.tscn,D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\game.gd,D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\README.md' -Destination 'D:\git_\apps\games\NeonBlocks' -Force
```

- **What it does:** Copies multiple specified files from the source directory to the destination directory, overwriting existing files if necessary.
- **Why:** This is a direct way to synchronize a set of related project assets from a staging area to a final games directory.
- **Example:** Copy-Item -LiteralPath 'D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\project.godot,D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\main.tscn,D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\game.gd,D:\git_apps\Devtrack_\.codex_stage\NeonBlocks\README.md' -Destination 'D:\git_\apps\games\NeonBlocks' -Force
- **Notes:** The initial Out-Null; is used to suppress output from the preceding command (New-Item) if it were run in sequence.

### Delete a specific application directory
<!-- sig: b1cd33d79854 -->
<!-- sig: 29be379e4ded -->

```bash
Remove-Item -LiteralPath 'D:\git_apps\games\tetris'
```

- **What it does:** Removes the directory located at 'D:\git_apps\games\tetris' using the specified literal path.
- **Why:** This is the explicit PowerShell way to delete a directory structure, ensuring that paths containing special characters or spaces are handled correctly via -LiteralPath.
- **Example:** Remove-Item -LiteralPath 'D:\git_apps\games\tetris' to clean up an old game directory.
- **Notes:** If the directory is not empty, you may need to add the -Recurse parameter to force deletion of contents.

### Copy a file only if the destination does not exist
<!-- sig: d15bd7e83b36 -->
<!-- sig: 6217209852a0 -->

```bash
Out-Null if '(Test-Path -LiteralPath '$destinationImage') {' throw 'Destination already exists; refusing to overwrite it.' '} Copy-Item -LiteralPath '$sourceImage' -Destination '$destinationImage' Get-Item -LiteralPath '$destinationImage'
```

- **What it does:** This script checks if the destination file exists; if it does, it throws an error and stops execution. If it doesn't exist, it copies the source file to the destination.
- **Why:** This pattern ensures that an overwrite operation is explicitly prevented, which is safer than relying on default copy behavior.
- **Example:** Out-Null if '(Test-Path -LiteralPath 'D:\git_apps\games\NeonBlocks\design\references\circuit-clash-3d-concept.png') {' throw 'Destination already exists; refusing to overwrite it.' '} Copy-Item -LiteralPath 'C:\Users\sraj\.codex\generated_images\01a08c95-8193-7763-aaa7-3156f1c8763b\exec-d6bef533-66c7-46eb-bca2-1b403ce9b77e.png' -Destination 'D:\git_apps\games\NeonBlocks\design\references\circuit-clash-3d-concept.png' Get-Item -LiteralPath 'D:\git_apps\games\NeonBlocks\design\references\circuit-clash-3d-concept.png'
- **Notes:** The structure uses an 'if' block to conditionally execute the throw statement, which is then followed by the copy operation. The final Get-Item is likely for confirmation or subsequent logic.

### Forcefully delete a specific configuration file
<!-- sig: e3635f09ec86 -->

```bash
del /f /q D:git_appsDevtrack_.codexhooks.json
```

- **What it does:** Deletes the file D:git_appsDevtrack_.codexhooks.json, forcing deletion of read-only attributes (/f) and suppressing confirmation prompts (/q).
- **Why:** This is used to clean up a specific, potentially problematic hook file in a development repository without interactive confirmation.
- **Example:** del /f /q D:git_appsDevtrack_.codexhooks.json before re-running setup scripts.
- **Notes:** The /f flag forces deletion even if the file is read-only, and /q suppresses prompts for confirmation.

### Verify that source and target paths are inside the workspace
<!-- sig: 8604478d4025 -->

```bash
$workspace = (Resolve-Path -LiteralPath .).Path;
$source = (Resolve-Path -LiteralPath "['vscode', 'cli']").Path;
$target = (Resolve-Path -LiteralPath '.runtime\wal').Path;
if (-not $source.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase) -or -not $target.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Path outside workspace' }
```

- **What it does:** Resolves the absolute paths for the current directory, a specific source folder, and a target folder, then checks if both source and target reside within the workspace root.
- **Why:** Prevents scripts from accidentally modifying or accessing files outside of the intended project directory, acting as a safety guardrail.
- **Example:** Use this logic at the start of a build or deployment script to ensure the environment is correctly scoped.
- **Notes:** Uses -LiteralPath to ensure paths containing brackets or special characters are handled correctly by Resolve-Path.

### Move a file and delete source if machine IDs match
<!-- sig: ca29ec52a449 -->

```bash
Move-Item -LiteralPath '$files[0].FullName' -Destination '$destination'
if ((Get-Content -Raw -LiteralPath '$idSource').Trim() -eq (Get-Content -Raw -LiteralPath '$idTarget').Trim()) { Remove-Item -LiteralPath '$idSource' }
```

- **What it does:** Moves a specific file from a source path to a destination and checks if the content of a machine-id file matches between source and target. If they match, it deletes the source machine-id file.
- **Why:** Ensures that files are only moved when the underlying machine identity is consistent, preventing data corruption or identity mismatches during migration.
- **Example:** Move a JSON event file and remove the source machine-id if the IDs are identical.
- **Notes:** Uses -LiteralPath to ensure that special characters in the file paths are not interpreted as wildcards.

### Delete specific failed batch files within a workspace
<!-- sig: ac16d5535fa3 -->

```bash
$failedDir = (Resolve-Path -LiteralPath '.runtime/failed').Path;
$workspace = (Resolve-Path -LiteralPath '.').Path;
if (-not $failedDir.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Failed directory is outside workspace' };
$files = @(Get-ChildItem -LiteralPath $failedDir -File -Filter 'batch-*.jsonl');
if ($files.Count -ne 6) { throw "Expected 6 failed batches, found $($files.Count)" };
foreach ($file in $files) { Remove-Item -LiteralPath $file.FullName -Force };
```

- **What it does:** Resolves the paths for the workspace and a failed directory, validates that the failed directory is inside the workspace, and deletes exactly 6 files matching 'batch-*.jsonl' from the failed directory.
- **Why:** Ensures safety by verifying the directory path before performing a bulk deletion of specific batch files.
- **Example:** $failedDir = (Resolve-Path -LiteralPath '.runtime/failed').Path; $workspace = (Resolve-Path -LiteralPath '.').Path; if (-not $failedDir.StartsWith($workspace + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Failed directory is outside workspace' }; $files = @(Get-ChildItem -LiteralPath $failedDir -File -Filter 'batch-*.jsonl'); if ($files.Count -ne 6) { throw "Expected 6 failed batches, found $($files.Count)" }; foreach ($file in $files) { Remove-Item -LiteralPath $file.FullName -Force };
- **Notes:** Uses -LiteralPath to ensure paths with special characters are handled correctly. The script will throw an error if the count of files found is not exactly 6.

## Processes

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads and modifies the content of `blueprint/tui/widgets.py` and `README.md` using string replacement.
- **Why:** It applies specific code and documentation changes to enforce standards without overwriting existing files.
- **Example:** python3 - <<'EOF' ... (full script content)
- **Notes:** The script uses heredoc syntax (`<<'EOF'`) to pass a multi-line Python script to `python3` for execution.

### Modify specific text patterns within Python scripts
<!-- sig: 884104110a05 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script uses Python's pathlib to read the contents of two files, blueprint/tui/widgets.py and README.md, and then performs string replacements on their content.
- **Why:** It automates the process of updating specific, complex string literals within source code and documentation files to reflect desired logic changes.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to the python3 interpreter. The replacement in widgets.py uses a count of 1 to ensure only the first occurrence is replaced.

### Replace specific text patterns within Python files
<!-- sig: 0f6e0a9ae2e6 -->
### Launch the game engine with specific project arguments
<!-- sig: 1471c10a43af -->

```bash
Start-Process -FilePath 'D:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe' -ArgumentList '--editor,--path,D:\git\_apps\games\NeonBlocks'
```

- **What it does:** Starts a new process using the specified executable path and passes arguments to launch the Godot editor pointing to the NeonBlocks project directory.
- **Why:** This is the explicit way to launch an external application with arguments in PowerShell, ensuring the process starts correctly regardless of the current shell context.
- **Example:** Start-Process -FilePath 'D:\Program Files (x86)\Steam\steamapps\common\Godot Engine\godot.windows.opt.tools.64.exe' -ArgumentList '--editor,--path,D:\git\_apps\games\NeonBlocks'
- **Notes:** The path arguments must be correctly escaped for PowerShell execution.

### List processes matching a specific executable name
<!-- sig: e1737ca014a7 -->

```bash
tasklist /V /FO CSV /FI "IMAGENAME eq Code.exe"
```

- **What it does:** Displays a detailed list of running processes, filtering the output to only include entries where the Image Name equals Code.exe, and formatting the result as CSV.
- **Why:** This provides a structured, machine-readable list of processes matching a specific executable name, which is better for scripting than the default output.
- **Example:** tasklist /V /FO CSV /FI "IMAGENAME eq Code.exe" to check for running instances of the IDE.
- **Notes:** The /V flag provides verbose output, and /FO CSV ensures the output is comma-separated values, making it easy to parse in a script.

## Archives and compression

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads and modifies content from two files, 'blueprint/tui/widgets.py' and 'README.md'.
- **Why:** This allows for complex, multi-step text manipulation and file rewriting using Python's `pathlib` module without needing to write a separate executable script.
- **Example:** python3 - <<'EOF' from pathlib import Path p = Path("blueprint/tui/widgets.py"); s = p.read_text() s = s.replace(''' for line in item.evidence: text.append(f"\n {line}", style=theme.INK3)''', ''' for line in item.evidence: if line not in item.summary: text.append(f"\n {line}", style=theme.INK3)''', 1) p.write_text(s) p = Path("README.md"); s = p.read_text() s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''', '', 'EOF' after running the command.
- **Notes:** The use of '<<'EOF'' ensures that the content between the delimiters is treated as a literal string, preventing shell expansion of variables within the Python code block.

### Replace specific text patterns within Python files
<!-- sig: 6b4cec9c4b06 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads, modifies, and overwrites content in two files: blueprint/tui/widgets.py and README.md.
- **Why:** This allows for complex, multi-step text transformations across multiple files without needing to manually edit them or use external text processing tools.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal text, preventing shell expansion of variables within the Python script.

### Replace specific text patterns within Python files
<!-- sig: 6ab25d121789 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, 'blueprint/tui/widgets.py' and 'README.md', and performs string replacements on their contents before writing the modified text back to the original files.
- **Why:** It automates the process of updating specific, complex string literals across multiple source files to align code or documentation with a new feature or logic.
- **Example:** python3 - <<'EOF' ... (as shown in the command line)
- **Notes:** The script uses Python's `pathlib` module for file I/O and relies on the shell's here-document (`<<'EOF'`) to pass the multi-line script content to `python3`.

### Replace specific text patterns within a Python script
<!-- sig: 2180d44ff627 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of two files, `blueprint/tui/widgets.py` and `README.md`, and performs string replacements on their contents before writing the modified text back to the original files.
- **Why:** It automates the modification of source code and documentation to update specific logic or phrasing across the project.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The use of `<<'EOF'` ensures that the shell does not perform variable expansion on the content piped into the Python script.

### Apply specific text replacements across files
<!-- sig: 44cfa14ea79a -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, modifies specific string patterns within them using string replacement, and then writes the modified content back to the original files.
- **Why:** It automates a targeted refactoring or documentation update across multiple files by programmatically applying complex text substitutions.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses Python's pathlib for file I/O and relies on the exact string literals provided for replacement to function correctly.

### Replace specific text patterns within Python files
<!-- sig: 8247fa4837d9 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
```

- **What it does:** Executes a Python script passed via standard input, which reads, modifies, and overwrites content in `blueprint/tui/widgets.py` and `README.md` using string replacement.
- **Why:** This allows for complex, multi-step text transformations on source files without needing to manually edit them or use external text processing tools.
- **Example:** python3 - <<'EOF' ... (content as shown above) ... EOF
- **Notes:** The use of `<<'EOF'` ensures that the shell does not perform variable expansion on the content piped into the Python script.

### Replace specific text patterns within Python files
<!-- sig: 60108988abc4 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of two files, modifies specific string literals within them using string replacement, and then writes the modified content back to the original files.
- **Why:** It automates the process of updating hardcoded strings or logic within source files to reflect new conventions or features.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses heredoc syntax (`<<'EOF'`) to pass the multi-line Python code directly to the python3 interpreter for execution.

### Modify widget file to filter evidence lines
<!-- sig: 0cc7f1e7b6d9 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of blueprint/tui/widgets.py and README.md, performs string replacements on both files, and then writes the modified content back to the original files.
- **Why:** It automates a targeted code refactoring and documentation update by using Python's string replacement capabilities across multiple files.
- **Example:** python3 - <<'EOF' ... (full script content) ... EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to python3. The replacement in widgets.py changes the evidence logging logic to only show lines not present in item.summary.

### Replace specific text patterns within Python files
<!-- sig: 538777aef9bb -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads and modifies content from two files, 'blueprint/tui/widgets.py' and 'README.md'.
- **Why:** This allows for complex, multi-step text manipulation and file rewriting using Python's `pathlib` module without needing to write a separate executable script.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal input, preventing shell expansion of variables within the script block.

### Replace specific text patterns within Python files
<!-- sig: 636faf764251 -->
### Check for local admin artifacts existence
<!-- sig: 402a31973b52 -->
<!-- sig: dc544962b055 -->

```bash
if exist .codex-cache '(dir' /s /b '.codex-cache)' else '(echo' 'NO_LOCAL_ADMIN_E2E_ARTIFACTS)'
```

- **What it does:** This command checks if the directory .codex-cache exists using 'if exist'. If it does, it executes 'dir /s /b .codex-cache' to list its contents recursively; otherwise, it prints the string 'NO_LOCAL_ADMIN_E2E_ARTIFACTS'.
- **Why:** It provides a conditional check to determine if necessary local artifacts are present before proceeding with a build or operation.
- **Example:** if exist .codex-cache '(dir' /s /b '.codex-cache)' else '(echo' 'NO_LOCAL_ADMIN_E2E_ARTIFACTS)'
- **Notes:** This syntax is specific to Windows batch scripting and relies on the 'if' conditional structure.

### Process and display contents of multiple files
<!-- sig: f6dee5b3e54f -->

```bash
for %f in (.claude\memory\project_mcp_distribution.md .claude\memory\project_launch_strategy.md .claude\memory\project_platform_modes.md .claude\memory\project_documentation.md .claude\memory\project_server_ui_refresh.md .claude\memory\feedback_rules.md .claude\memory\reference_subsystems.md .claude\memory\project_autoload_env.md .claude\memory\project_local_agents.md .claude\memory\project_saas_license.md) do @echo ====%f==== & @type %f
```

- **What it does:** This batch loop iterates over a list of specified markdown files, printing a separator header for each file, and then executing the @type command on the file path.
- **Why:** It automates the process of sequentially processing and displaying the contents of several related documentation files within a single batch script execution.
- **Example:** for %f in (file1.md file2.md) do @echo ====%f==== & @type %f
- **Notes:** The command uses batch scripting syntax (`for`, `do`, `&`) and relies on the availability of the `@type` utility.

### Generate a comprehensive project overview report
<!-- sig: 022c27a29a32 -->

```bash
Write-Output '--- README ---;'
Get-Content -LiteralPath 'README.md';
Write-Output '--- main.tscn ---;'
Get-Content -LiteralPath 'main.tscn';
Write-Output '--- game.gd outline ---;'
rg -n '^(extends|class_name|signal|const|var |@onready|func )' 'game.gd';
Write-Output '--- git status ---;'
git status --short --branch
```

- **What it does:** This sequence outputs headers, reads the content of README.md and main.tscn, uses ripgrep to find declarations in game.gd, and finally shows the current git status.
- **Why:** It aggregates multiple disparate pieces of project metadata—documentation, scene structure, code declarations, and git state—into a single, readable output stream for review.
- **Example:** Running this entire pipeline before submitting a pull request to summarize the current state of the project.
- **Notes:** The use of Write-Output ensures clear section breaks between the different content blocks being concatenated.

### Collect all potential Steam installation paths from registry
<!-- sig: eef054086751 -->

```bash
$steamPaths = @()
$regPaths = @('HKCU:\Software\Valve\Steam','HKLM:\SOFTWARE\WOW6432Node\Valve\Steam','HKLM:\SOFTWARE\Valve\Steam')
foreach ($key in $regPaths) { if (Test-Path '$key') { $props = Get-ItemProperty '$key' if ($props.SteamPath) { $steamPaths += $props.SteamPath } if ($props.InstallPath) { $steamPaths += $props.InstallPath } } }
$steamPaths = $steamPaths | Sort-Object -Unique
Write-Output 'Steam roots:'
$steamPaths
```

- **What it does:** This script initializes an array to hold Steam paths, then iterates through three specified registry keys. For each existing key, it retrieves properties like SteamPath and InstallPath, appending any found values to the $steamPaths array.
- **Why:** It systematically checks multiple common registry locations where Steam might store its installation or configuration paths, ensuring comprehensive coverage.
- **Example:** $steamPaths = @() $regPaths = @('HKCU:\Software\Valve\Steam','HKLM:\SOFTWARE\WOW6432Node\Valve\Steam','HKLM:\SOFTWARE\Valve\Steam') foreach ($key in $regPaths) { if (Test-Path '$key') { $props = Get-ItemProperty '$key' if ($props.SteamPath) { $steamPaths += $props.SteamPath } if ($props.InstallPath) { $steamPaths += $props.InstallPath } } }
- **Notes:** The script relies on the existence of specific registry keys and properties. The final output is a sorted, unique list of collected paths.

### List executable files within a specific game directory
<!-- sig: 74a83a9cbbe5 -->

```bash
'$manifest' = 'D:\Program Files (x86)\Steam\steamapps\appmanifest_404790.acf' if '(Test-Path' -LiteralPath '$manifest)' '{' Get-Content -LiteralPath '$manifest' '}' '$common' = 'D:\Program Files (x86)\Steam\steamapps\common' Get-ChildItem -LiteralPath '$common' -Directory | Where-Object { $_.Name -match 'Godot' } | ForEach-Object { Write-Output "Directory: $($_.FullName)" ; Get-ChildItem -LiteralPath $_.FullName -Recurse -File -Filter '*.exe' | Select-Object FullName,Length }}
```

- **What it does:** This script first checks for and reads a specific Steam manifest file, then finds all subdirectories named 'Godot' within the common Steam directory. Finally, it recursively lists all `.exe` files inside those Godot directories, outputting their full path and length.
- **Why:** This complex sequence is necessary to reliably locate and inventory all executable assets within a specific game's installation folder structure, which is more robust than simple globbing.
- **Example:** Running the full command block to inventory executables in the Godot subdirectory of the Steam common folder.
- **Notes:** The script relies on PowerShell's conditional execution and pipeline processing. The initial manifest check is executed first, regardless of the subsequent directory listing.

### Validate required input directories and files
<!-- sig: be498f4d1e94 -->

```bash
if (-not (Test-Path -LiteralPath $sourceImage)) { throw "Generated source image was not found." }
New-Item -ItemType Directory -Path $referenceDir -Force | Out-Null
if (Test-Path -LiteralPath $destinationImage) { throw "Destination already exists; "
```

- **What it does:** This block checks if the source image exists, ensures the reference directory exists, and then checks if the destination image already exists.
- **Why:** It provides necessary pre-flight checks to prevent subsequent image processing commands from failing due to missing inputs or overwriting existing outputs unexpectedly.
- **Example:** Running this block before an image comparison script to ensure all paths are valid.
- **Notes:** The script uses PowerShell cmdlets like Test-Path and New-Item. The variables $sourceImage, $referenceDir, and $destinationImage must be correctly set beforehand.

### Execute a Python script with a specific harness
<!-- sig: 4a5a839db7fa -->

```bash
'C:\WINDOWS\system32\cmd.exe' /c 'C:\Users\sraj\AppData\Roaming\uv\python\cpython-3.13-windows-x86_64-none\pythonw.exe D:\git_apps\ai_sessions_skills\tool\bin\capture.py --harness codex < D:\git_apps\ai_sessions_skills\.runtime\windowless-hook-probe.json'
```

- **What it does:** This command executes the Python script capture.py using the pythonw interpreter, passing the --harness codex argument, and redirecting the content of windowless-hook-probe.json as standard input.
- **Why:** This pattern is used to run a specific Python utility (capture.py) in a controlled environment, feeding it configuration data from a local JSON file.
- **Example:** 'C:\WINDOWS\system32\cmd.exe' /c 'C:\Users\sraj\AppData\Roaming\uv\python\cpython-3.13-windows-x86_64-none\pythonw.exe D:\git_apps\ai_sessions_skills\tool\bin\capture.py --harness codex < D:\git_apps\ai_sessions_skills\.runtime\windowless-hook-probe.json'
- **Notes:** The use of 'pythonw.exe' suggests running the script without opening a console window. The input redirection (<) feeds the contents of the specified JSON file into the script's standard input.

## Linting and validation

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads and modifies content from two files, 'blueprint/tui/widgets.py' and 'README.md'.
- **Why:** This allows for complex, multi-step text manipulation and file rewriting using Python's `pathlib` module without needing to write a separate executable script.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal input, preventing shell expansion of variables within the script block.

### Replace specific text patterns within Python files
<!-- sig: 7e336c7ba104 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, `blueprint/tui/widgets.py` and `README.md`, and performs string replacements on their contents before writing the modified text back to the original files.
- **Why:** It modifies the source code and documentation to change the logic for displaying evidence lines in the TUI widget and updates the README to reflect a change in the command description.
- **Example:** python3 - <<'EOF' ... (as shown in the command line)
- **Notes:** The script uses `pathlib.Path` for file operations and relies on the shell's here-document (`<<'EOF'`) to pass the multi-line Python code to `python3`.

### Replace specific text patterns within Python files
<!-- sig: 2cd5b3a01f24 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads and modifies content from two files, 'blueprint/tui/widgets.py' and 'README.md'.
- **Why:** This allows for complex, multi-step text manipulation and file rewriting using Python's `pathlib` module without needing to write a separate executable script.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal input, preventing shell expansion of variables within the script block.

### Replace specific text patterns within Python files
<!-- sig: 1c1b7cac6ff2 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads and modifies content from 'blueprint/tui/widgets.py' and 'README.md' using string replacement.
- **Why:** This allows for automated, programmatic modification of source code or documentation files without manually opening and editing them.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal input, preventing shell expansion of variables within the script block.

### Replace specific text patterns within Python files
<!-- sig: 8315de47fcfb -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads and modifies content from two files, 'blueprint/tui/widgets.py' and 'README.md'.
- **Why:** This allows for complex, multi-step text manipulation and file rewriting using Python's `pathlib` module without needing to write a separate executable script.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal input, preventing shell expansion of variables within the script block.

### Replace specific text patterns within files
<!-- sig: f68af30fb14e -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
p.write_text(s)
```

- **What it does:** This script reads the content of two files, replaces specific multi-line string patterns using Python's string replace method, and then writes the modified content back to the original files.
- **Why:** It allows for complex, context-aware text transformations across multiple files that simple search-and-replace tools might struggle with.
- **Example:** Running the script to update the logic in `blueprint/tui/widgets.py` and `README.md`.
- **Notes:** The use of `<<'EOF'` ensures that the shell does not perform variable expansion on the content piped into the Python script.

### Replace specific text patterns within Python files
<!-- sig: d7e0b6338d48 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** Executes a Python script passed via standard input, which reads and modifies content from two files, 'blueprint/tui/widgets.py' and 'README.md'.
- **Why:** This script performs targeted find-and-replace operations across source code and documentation to update logic or phrasing.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal input, preventing shell expansion of variables within the script block.

### Replace specific text patterns within a file
<!-- sig: 47463f30365f -->
<!-- sig: 5625f59bbb05 -->

```bash
log level '|'',' '''|' 'BLUEPRINT_DISCOVERY_STANDARDS_FILENAME'
```

- **What it does:** This command appears to be invoking a custom 'log' binary to perform a find-and-replace operation on the file specified by the BLUEPRINT_DISCOVERY_STANDARDS_FILENAME variable.
- **Why:** It is used to programmatically modify the content of a specific configuration or standard file, likely to update internal logic or documentation placeholders.
- **Example:** log level '|'',' '''|' 'blueprint/tui/widgets.py'
- **Notes:** The command structure suggests a custom utility where the first argument is the log level, followed by the search pattern, replacement pattern, and target file.

### Replace specific text patterns in a file
<!-- sig: 0eea5fd24126 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, 'blueprint/tui/widgets.py' and 'README.md', and performs string replacements on their contents before writing the modified text back to the original files.
- **Why:** It automates the process of updating specific, complex string literals within source code and documentation files to align with current project standards.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The use of a here-document (`<<'EOF'`) ensures that the content inside the quotes is passed directly to the python3 interpreter without shell expansion.

### Modify specific text patterns within files
<!-- sig: 37570c6bff59 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, 'blueprint/tui/widgets.py' and 'README.md', performs string replacements on their contents, and then writes the modified content back to the original files.
- **Why:** It allows for precise, programmatic modification of source code or documentation strings without relying on external text manipulation tools.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses Python's pathlib for file I/O and string.replace() for substitution. The use of '<<'EOF'' ensures the heredoc content is treated as literal text.

### Replace specific text patterns within files
<!-- sig: 211eb09cc727 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, modifies specific string patterns using the replace method, and then writes the modified content back to the original files.
- **Why:** It allows for complex, multi-line, or conditional text substitutions across multiple files without relying on external text processing tools like sed or awk.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The use of a here-document (`<<'EOF'`) ensures that shell variable expansion is disabled within the script block, preserving the literal content for Python execution.

### Replace specific text patterns within Python files
<!-- sig: f033c18ec26a -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of two files, modifies specific string literals within them using string replacement, and then writes the modified content back to the original files.
- **Why:** It automates a targeted refactoring or modification of source code and documentation files without manual editing.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The use of '<<'EOF'' ensures that the shell does not perform variable expansion on the content piped into the python script.

### Update widget file to use summary checks
<!-- sig: 9fe5447f8b83 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term
EOF
```

- **What it does:** This script reads and modifies two files, `blueprint/tui/widgets.py` and `README.md`, using string replacement operations.
- **Why:** It updates the widget logic to conditionally append evidence lines only if they are not present in the item's summary, and updates the README documentation accordingly.
- **Example:** python3 - <<'EOF' ... EOF
- **Notes:** The script uses a here-document (`<<'EOF'`) to pass the multi-line Python code block to the python3 interpreter.

### Replace specific text patterns within a Python script
<!-- sig: 373e2b0ad214 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
```

- **What it does:** Executes a Python script that reads the content of two files, performs string replacements on the content, and then writes the modified content back to the original files.
- **Why:** This allows for automated, targeted modifications to source code or documentation files without manually opening and editing them.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content piped into the script is treated as a literal string, preventing shell expansion of variables within the script block.

### Modify specific text patterns within Python files
<!-- sig: 0f5bc6af6e8b -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of two files, modifies specific string patterns using the replace method, and then writes the altered content back to the original files.
- **Why:** It allows for automated, targeted refactoring of code or documentation without manually opening and editing the files.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to the python3 interpreter. The replacement count of 1 in the first replacement limits the change to the first occurrence.

### Apply specific text replacements across files
<!-- sig: 9cca66d09ecc -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, modifies specific string patterns within them using string replacement, and then writes the modified content back to the original files.
- **Why:** It automates the tedious process of manually editing configuration or documentation files to enforce a specific coding or documentation convention.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses Python's pathlib to handle file I/O and string replacement. The use of '<<'EOF'' ensures the heredoc content is treated as a literal string.

### Replace specific text patterns within a file
<!-- sig: f5bf9e3d9250 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of two files, modifies specific string occurrences using the replace method, and then writes the modified content back to the original files.
- **Why:** It automates a targeted find-and-replace operation across multiple files, which is more complex than a simple shell substitution.
- **Example:** Running the script to update the logic in `blueprint/tui/widgets.py` and the documentation in `README.md`.
- **Notes:** The script uses Python's `pathlib` module for file I/O and relies on the specific string literals provided for replacement.

### Modify specific text patterns within Python files
<!-- sig: 16c7b18772ed -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of two files, 'blueprint/tui/widgets.py' and 'README.md', and performs string replacements on their contents before writing the modified text back to the original files.
- **Why:** It allows for automated, targeted refactoring of code and documentation by replacing specific, complex string literals within the files.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to the python3 interpreter. The replacement in widgets.py uses a count of 1 to ensure only the first occurrence is replaced.

### Replace specific text patterns within Python files
<!-- sig: 66558b3f9215 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term''
EOF
```

- **What it does:** This script reads the content of two files, modifies specific multi-line string patterns using string replacement, and then writes the modified content back to the original files.
- **Why:** It automates a targeted refactoring or modification of source code and documentation files without manual editing.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal text, preventing shell expansion of variables within the script block.

### Replace specific text patterns in Python files
<!-- sig: 7e02eb13f55d -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
EOF
```

- **What it does:** This script reads the content of two files, `blueprint/tui/widgets.py` and `README.md`, and performs string replacements on their contents before writing the modified text back to the original files.
- **Why:** It modifies the source code and documentation to change how evidence lines are appended in `widgets.py` and updates the description of the `blueprint tui` command in `README.md`.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses a here-document (`<<'EOF'`) to pass the multi-line Python code to `python3` for execution. The single quotes around `EOF` prevent shell variable expansion within the script block.

### Replace specific text patterns within Python files
<!-- sig: bc109170fb20 -->

```bash
python3 - <<'EOF'
from pathlib import Path
p = Path("blueprint/tui/widgets.py"); s = p.read_text()
s = s.replace('''        for line in item.evidence:
text.append(f"\n  {line}", style=theme.INK3)''', '''        for line in item.evidence:
if line not in item.summary:
text.append(f"\n  {line}", style=theme.INK3)''', 1)
p.write_text(s)
p = Path("README.md"); s = p.read_text()
s = s.replace('''| `blueprint tui [plan.md]` | Open the terminal UI (needs `textual`). With a plan it runs the same check as `check-plan` and shows it on screens 1 and 2. See [Term`
```

- **What it does:** This script reads the content of two files, modifies specific string literals within them using string replacement, and then writes the modified content back to the original files.
- **Why:** It automates a targeted refactoring or update across multiple source files without manual editing, ensuring consistency across the codebase.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The use of a here-document (`<<'EOF'`) ensures that shell variable expansion is disabled within the script block, preserving the literal strings for Python processing.

### Replace specific code patterns within a Python file
<!-- sig: dcd4bc421b46 -->

```bash
cat > blueprint/validation.py <<'EOF'
"""Check that each standard can be enforced in the repository it governs.
A rule such as "dependencies must be declared in package.json" makes no sense
in a Python project. A local model reads a plain-text profile of the repo and
each rule, and says whether the rule can apply here. Rules it rejects are
marked `status: invalid` in the standards file, never deleted without being asked.
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Literal, Protocol
from .config import Settings
from .llm import LLMError,
```

- **What it does:** This command uses a here-document (<<'EOF') to overwrite the contents of blueprint/validation.py with a specific block of Python code.
- **Why:** It allows for the atomic replacement of an entire file's content, which is necessary when updating complex configuration or validation logic.
- **Example:** cat > blueprint/validation.py <<'EOF' ... (content) ... EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the here-document, ensuring the content is written literally.

### Replace specific text within a file
<!-- sig: 7b0ab18a8645 -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here

Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine,'''
```

- **What it does:** This sequence uses a here-document to write a Python script to /tmp/fix_readme.py. The script reads README.md, replaces a specific string, and overwrites the content.
- **Why:** This allows for a programmatic, targeted replacement of text within a file using Python's string manipulation capabilities, which is more complex than a simple sed substitution.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' ... (script content) ... EOF
- **Notes:** The use of single quotes around 'EOF' prevents shell variable expansion within the here-document, ensuring the Python code is written literally.

### Write multi-line content into a file
<!-- sig: f250133b0d29 -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
```

- **What it does:** The cat command redirects standard input into the file /tmp/fix_readme.py until it encounters the delimiter 'EOF'.
- **Why:** This allows for the direct injection of a large, multi-line block of text or code into a file without needing to use an editor.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' p='README.md' s=open(p).read() s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine,''' EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the heredoc, ensuring the content is written literally.

### Write multi-line content into a file
<!-- sig: 5f039afdebe5 -->

```bash
cat > /tmp/fix_readme.py <<'EOF'
```

- **What it does:** The cat command redirects standard input into the file /tmp/fix_readme.py until it encounters the delimiter 'EOF'.
- **Why:** This allows for the direct injection of a large, multi-line block of text into a file without needing to use an editor interactively.
- **Example:** cat > /tmp/fix_readme.py <<'EOF' p='README.md' s=open(p).read() s=s.replace('''Limits, so nothing is oversold: discovery is deterministic''','''### Checking that a standard can be enforced here Editing the standards in the terminal UI (`e`) and saving asks a **local model** (Ollama, `BLUEPRINT_OLLAMA_MODEL`, default `gemma4:latest`) to read a plain-text profile of the repository and say, one rule at a time, whether the rule can apply to this codebase. A rule about `package.json` in a Python project cannot; a rule that asks for ruff can, because ruff can be added. Nothing leaves your machine, '' EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the heredoc, ensuring the content is written literally.

### Replace specific code snippets within Python files
<!-- sig: d7c26f217465 -->

```bash
cat > /tmp/fix_data3.py <<'EOF'
p='blueprint/store.py'
s=open(p).read()
s=s.replace('''    def get_json(''','''    def stamp(self, namespace: str, key: str) -> float | None:
"""When an entry was stored, without reading its value."""
rows = self._run("SELECT created_at FROM cache WHERE namespace = ? AND key = ?", (namespace, key), fetch=True)
return float(rows[0][0]) if rows else None
def get_json(''',1)
open(p,'w').write(s)
p='blueprint/tui/data.py'
s=open(p).read()
s=s.replace('''    validation_cache: dict[str, StandardCheck] = field(default_factory=dict)''','''
what_description_of_the_command_as_a_whole_process_of_writing_a_script_and_executing_it_to_modify_files_in_place_using_sed_like_replacement_logic_via_python_scripting_and_here_document_redirection_to_a_temporary_file_which_is_then_executed_or_its_contents_are_used_for_subsequent_operations_in_this_case_it_is_used_to_perform_two_separate_string_replacements_on_two_different_files_blueprint/store.py_and_blueprint/tui/data.py_using_the_logic_defined_in_the_here_document_script_which_is_not_fully_shown_but_implied_by_the_structure_of_the_commands_provided_in_the_input_context_which_is_a_cat_command_with_a_here_document_EOF_)
why_this_approach_is_used_over_obvious_alternatives_like_sed_or_direct_edits_is_to_execute_complex_multi_line_or_context_aware_string_replacements_that_are_easier_to_manage_and_debug_within_a_scripted_environment_before_applying_the_changes_to_the_target_files_blueprint/store.py_and_blueprint/tui/data.py
example_invocation_of_the_command_as_provided_in_the_input_context_is_the_entire_block_starting_with_cat_and_ending_with_the_second_replace_call_on_blueprint/tui/data.py
notes_the_commands_are_part_of_a_larger_script_execution_where_the_here_document_EOF_is_the_delimiter_for_the_script_content_and_the_replacement_logic_is_executed_by_the_shell_after_the_cat_command_is_finished_writing_to_the_temporary_file_or_the_script_is_executed_from_that_file_the_actual_execution_of_the_script_is_not_shown_only_the_content_being_written_to_the_temporary_file_is_shown
```

- **What it does:** This sequence writes a script to /tmp/fix_data3.py, which then reads and modifies two files, blueprint/store.py and blueprint/tui/data.py, by replacing specific string patterns within them.
- **Why:** This method allows for complex, multi-step text transformations across multiple files using Python's string manipulation capabilities, which is more robust for intricate code changes than simple shell tools.
- **Example:** cat > /tmp/fix_data3.py <<'EOF' ... (full script content) ... EOF
- **Notes:** The script is written to /tmp/fix_data3.py; subsequent execution of this file is required to apply the changes to blueprint/store.py and blueprint/tui/data.py.

### Redirect multi-line content into a file
<!-- sig: 5ed0b901e955 -->

```bash
cat > /tmp/edit_readme.py <<'EOF'
```

- **What it does:** Uses 'cat' to read input from standard input and redirects it into the file /tmp/edit_readme.py. The '<<' syntax allows the content between the delimiters to be treated as input.
- **Why:** This is a standard shell idiom for creating or overwriting a file with multi-line content directly from the command line without needing an external editor.
- **Example:** cat > /tmp/edit_readme.py <<'EOF' p = "README.md" s = open(p).read() EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the heredoc, ensuring the content is written literally.

### Replace specific text blocks within a Python file
<!-- sig: 741f5fec6836 -->

```bash
python3 - <<'EOF'
p='blueprint/code_checks.py'
s=open(p).read()
s=s.replace('''    recorded_only: list[Standard] = field(default_factory=list)    """Active standards that neither a code check nor plan checks enforce.""''','''    recorded_only: list[Standard] = field(default_factory=list)    """Active standards that neither a code check nor plan checks enforce.""'

    judged: list[Standard] = field(default_factory=list)    """Active standards a model judges. `blueprint gate` runs them; the exact checks here do not."'''
s=s.replace('''    report.recorded_only = [s for s in standards `
```

- **What it does:** This script reads the content of blueprint/code_checks.py, performs two string replacements to modify the code structure, and then presumably writes the changes back (though the write operation is not fully shown).
- **Why:** It allows for targeted, programmatic modification of source code files without manually editing them, which is useful for automated refactoring or patching.
- **Example:** python3 - <<'EOF' ... (as shown in the input)
- **Notes:** The script uses heredoc syntax (`<<'EOF'`) to pass the multi-line Python code block to the python3 interpreter. The replacement strings must exactly match the content being targeted.

### Write content into a file using heredoc
<!-- sig: 729cf9e6e460 -->

```bash
cat > standards.yaml <<'EOF'
standards: - id: no-swallow title: Do not swallow exceptions severity: error description: An except block must not silently ignore the error. It must re-raise, log it, or handle it in a way the caller can see. A bare '`pass`' in an except block is a violation. judge: true b
```

- **What it does:** The cat command redirects input from a here document (delimited by EOF) into the specified file, standards.yaml.
- **Why:** This allows for multi-line input to be piped directly into a file without needing to manually type or paste each line.
- **Example:** cat > standards.yaml <<'EOF' standards: - id: no-swallow title: Do not swallow exceptions severity: error description: An except block must not silently ignore the error. It must re-raise, log it, or handle it in a way the caller can see. A bare '`pass`' in an except block is a violation. judge: true b EOF
- **Notes:** Using single quotes around the delimiter (e.g., <<'EOF') prevents shell variable expansion within the heredoc content.

### Modify markdown file content using python
<!-- sig: ccc08d2038ac -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en`
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs a string replacement to update the fields table, and then uses the resulting string in a subsequent command structure.
- **Why:** It allows for programmatic, targeted modification of structured text within a markdown file, which is more precise than simple text search-and-replace tools.
- **Example:** python3 - <<'EOF' ... (as shown in the command)
- **Notes:** The use of heredoc (`<<'EOF'`) ensures that shell variable expansion is disabled within the script block, preserving the literal content of the Python code.

### Modify markdown content using python script
<!-- sig: d61d59fa363f -->

```bash
python3 - <<'EOF' 
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')

start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** Executes a Python script piped into stdin to read the content of docs/editing-standards.md, perform a string replacement on the fields table, and then find the starting index of a specific markdown heading.
- **Why:** This allows for automated, targeted modification of documentation files based on predefined structural rules, which is more precise than manual text editing.
- **Example:** python3 - <<'EOF' p='docs/editing-standards.md' s=open(p).read() # fields table s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''') start=s.index("## Add a rule that is not deterministic") en
- **Notes:** The script uses a here-document (<<'EOF') to pass the Python code to python3. The replacement string must correctly escape newlines and quotes within the Python string literal.

### Perform an exact string replacement within a file
<!-- sig: ce11573ba844 -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** This Python script reads the content of docs/editing-standards.md, performs a specific string replacement on the content, and then finds the index of a specific heading.
- **Why:** It allows for precise, programmatic modification of documentation content before further processing or validation.
- **Example:** python3 - <<'EOF' ... (as shown above) ... EOF
- **Notes:** The script uses a here-document to pass the multi-line Python code to the interpreter. The replacement targets a specific table structure within the markdown file.

### Replace specific markdown table content within a file
<!-- sig: 6bc5b1aa093d -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs a string replacement on a specific markdown table row, and then attempts to find the index of a specific heading.
- **Why:** It automates the tedious task of updating boilerplate text within a documentation file to reflect new feature descriptions.
- **Example:** python3 - <<'EOF' ... (as shown above) ... EOF
- **Notes:** The script uses a here-document to pass the Python code to python3. The replacement string must exactly match the target string, including surrounding newlines if present in the original file.

### Modify markdown table content using python
<!-- sig: 88345228e88b -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs a string replacement on a specific markdown table row, and then attempts to find the index of a specific heading.
- **Why:** It allows for programmatic, precise modification of structured text files like markdown documentation without manual editing.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the entire Python code block to python3 for execution. The replacement string must exactly match the target content.

### Modify content within a markdown file
<!-- sig: e57862b13583 -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs a string replacement on the fields table section, and then finds the starting index of a specific markdown heading.
- **Why:** It allows for programmatic, targeted modification of documentation content without manually editing the file, which is useful for automated documentation updates.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to the python3 interpreter. The replacement string must exactly match the target string, including newlines.

### Replace specific markdown table content
<!-- sig: 804d1d3d9bdd -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs a string replacement on a specific markdown table section, and then attempts to find the index of a specific heading.
- **Why:** It automates the tedious task of updating boilerplate text within a documentation file to reflect new rules or features.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to python3. The replacement string must exactly match the target text, including newlines.

### Modify documentation standards file content
<!-- sig: a5fdee4cd671 -->

```bash
python3 - <<'EOF'
p='docs/editing-standards.md'
s=open(p).read()
# fields table
s=s.replace('''| `options` | no | Settings for that check, see below. |''','''| `options` | no | Settings for that check, see below. For a judged rule: `include` and `exclude` path patterns. |\n| `judge` | no | `true`: a local model reads each file against the description. See [Add a rule a model judges](#add-a-rule-a-model-judges). |\n| `block` | no | Only with `judge: true`. The model's findings stop `blueprint gate`. Without it they only advise. |''')
start=s.index("## Add a rule that is not deterministic")
en
```

- **What it does:** This script reads the docs/editing-standards.md file, replaces a specific markdown table snippet, and then finds the starting index of a specific section header.
- **Why:** This is used to programmatically update the structure of the documentation file to include new configuration options for rule judging.
- **Example:** python3 - <<'EOF' ... (as shown in the command line)
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to the python3 interpreter.

### Replace specific text within a README file
<!-- sig: 6b74d10e97d8 -->

```bash
python3 - <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace(" Judging markdown plans with a model is not built, and the terminal UI does not run judged rules yet: use `blueprint gate`."," A model can also judge a markdown plan (`applies_to: [plan]`), but only for what the plan says, not for what it leaves out. The terminal UI does not run judged code rules yet: use `blueprint gate`.")
s=s.replace("How to write one: [docs/editing-standards.md](docs/editing-standards.md#add-a-rule-a-model-judges).","The same rule can judge a plan before any code exists: add `applies_to: [plan]` (or `[code, plan`
```

- **What it does:** This Python script reads the content of README.md, performs two string replacements on the content, and implicitly overwrites the file with the modified string.
- **Why:** It allows for a controlled, programmatic update of documentation text across multiple instances in a single execution.
- **Example:** python3 - <<'EOF' p='README.md' s=open(p).read() s=s.replace(" Judging markdown plans with a model is not built, and the terminal UI does not run judged rules yet: use `blueprint gate`."," A model can also judge a markdown plan (`applies_to: [plan]`), but only for what the plan says, not for what it leaves out. The terminal UI does not run judged code rules yet: use `blueprint gate`.") s=s.replace("How to write one: [docs/editing-standards.md](docs/editing-standards.md#add-a-rule-a-model-judges).","The same rule can judge a plan before any code exists: add `applies_to: [plan]` (or `[code, plan` EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to python3. The file modification is implied by the script's logic but not explicitly shown in the provided snippet.

### Replace specific text within a README file
<!-- sig: 6c96cecdec07 -->

```bash
python3 - <<'EOF'
p='README.md'
s=open(p).read()
s=s.replace("Judging markdown plans with a model is not built, and the terminal UI does not run judged rules yet: use `blueprint gate`."," A model can also judge a markdown plan (`applies_to: [plan]`), but only for what the plan says, not for what it leaves out. The terminal UI does not run judged code rules yet: use `blueprint gate`.")
s=s.replace("How to write one: [docs/editing-standards.md](docs/editing-standards.md#add-a-rule-a-model-judges).","The same rule can judge a plan before any code exists: add `applies_to: [plan]` (or `[code, plan`
```

- **What it does:** This Python script reads the content of README.md, performs two string replacements on the content, and implicitly writes the modified content back (though the final write step is omitted in the provided snippet).
- **Why:** It allows for targeted, programmatic updates to documentation strings within a file without manual text editing.
- **Example:** python3 - <<'EOF' ... (script content) ... EOF
- **Notes:** The provided snippet only reads and modifies the string 's'; it does not include the code to write 's' back to README.md.

### Modify Python source files in place
<!-- sig: a65647d7dbf2 -->

```bash
python3 - <<'EOF'
p="blueprint/discovery.py"; s=open(p).read()
s=s.replace("from .models import DependencyCandidate, Plan, Verdict\n","from .models import DependencyCandidate, Plan, Verdict\nfrom .plan_location import PlanLocation, locate_plan\n",1)
open(p,"w").write(s)
p="blueprint/cli.py"; s=open(p).read()
s=s.replace("from .hooks import","from .plan_gate import run_plan_gate, target_from_hook\nfrom .plan_location import PlanLocation\nfrom .hooks import",1)
# render_discovery
s=s.replace('''    lines += ["", f"Drafted {len(found.standards)} standards."]''','''    lines += ["", "Plan"]
i
```

- **What it does:** This script reads the content of two Python files, blueprint/discovery.py and blueprint/cli.py, performs string replacements on the content, and then overwrites the original files with the modified content.
- **Why:** It automates the necessary refactoring of existing source code to integrate new planning logic, which is faster and less error-prone than manual editing.
- **Example:** python3 - <<'EOF' ... (as shown above) ... EOF
- **Notes:** The use of '<<'EOF'' ensures that the shell does not interpret the content of the script block, allowing Python to handle the string replacements correctly.

### Modify a configuration file content in place
<!-- sig: 9c090972a3ec -->

```bash
python3 - <<'EOF'
p="blueprint/plan_gate.py"; s=open(p).read()
s=s.replace("'Edit the plan, not the code: {location.path}. Do not edit {root.name}'s standards file to get past a rule. "',''Edit the plan, not the code: {location.path}. Do not edit the standards file to get past a rule. "')
s=s.replace("def render_blocked(verdict: Verdict, location: PlanLocation, root: Path, limit: int)","def render_blocked(verdict: Verdict, location: PlanLocation, limit: int)")
s=s.replace("render_blocked(verdict, location, root, settings.gate_max_findings)","render_blocked(verdict, location, settings.gat"
```

- **What it does:** This script reads the content of blueprint/plan_gate.py, performs multiple string replacements on the content, and then overwrites the original file with the modified string.
- **Why:** It allows for automated, targeted modifications to a specific configuration file without manually opening and editing it.
- **Example:** python3 - <<'EOF' ... (full script execution)
- **Notes:** The use of '<<'EOF'' ensures that the content passed to python3 is treated as a literal string, preventing shell expansion of variables within the script block.

### Replace specific text within a markdown file
<!-- sig: 10d81f26ebbf -->

```bash
python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1) s=s.replace("The only check today is `type-hints`:","") EOF
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using Python's replace method, and then presumably writes the modified content back (though the write operation is omitted in the provided snippet).
- **Why:** It allows for complex, multi-step text substitution within a file that is difficult or cumbersome to achieve with standard shell tools like sed.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) s=s.replace("another old", "another new") EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the Python code to python3. The '1' in the first replace limits the substitution to the first occurrence.

### Update documentation to include docstrings
<!-- sig: 3de3cf292401 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements to update the text, and then presumably writes the modified content back (though the write operation is omitted in the provided snippet).
- **Why:** It automates the tedious process of finding and replacing specific outdated text blocks within a documentation file to reflect current coding standards.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text",1) s=s.replace("another old phrase", "new phrase") EOF
- **Notes:** The provided snippet reads the file but does not write the modified string `s` back to `docs/editing-standards.md`. A write operation (e.g., `with open(p, 'w') as f: f.write(s)`) is required to persist changes.

### Replace specific text within a document
<!-- sig: 59a2450cd9c5 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements on the content, and then implicitly exits without writing the changes back to the file.
- **Why:** It allows for complex, multi-step text transformations using Python's string manipulation capabilities, which is more powerful than simple shell substitution.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The script reads the file but does not write the modified content back to docs/editing-standards.md. The use of '<<'EOF'' ensures that shell variable expansion is suppressed within the heredoc.

### Update documentation to include type hints
<!-- sig: 39ec5258e336 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the docs/editing-standards.md file, performs two string replacements to update specific text blocks, and then presumably writes the modified content back (though the write operation is omitted in the provided snippet).
- **Why:** It automates the tedious process of updating documentation across multiple instances of specific text to reflect the inclusion of type hints alongside docstrings.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text",1) s=s.replace("another old", "another new") EOF
- **Notes:** The provided snippet does not include the final step to write the modified string `s` back to the file `p`.

### Replace specific text within a document
<!-- sig: d422bb5e9d7e -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using the replace method, and then presumably writes the modified content back to the file (though the write operation is omitted in the provided snippet).
- **Why:** It allows for complex, multi-step text substitution within a file using Python's string manipulation capabilities, which is more powerful than simple shell substitution.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The provided snippet is incomplete as it does not show the final step of writing the modified string 's' back to the file 'docs/editing-standards.md'.

### Replace specific text within a markdown file
<!-- sig: f5054ec8847c -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using the .replace() method, and then implicitly discards the modified content as it is not written back to the file.
- **Why:** It allows for complex, multi-step text substitution within a file using Python's string manipulation capabilities, which is more powerful than simple shell substitution.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The script reads the file but does not write the modified string 's' back to the file, so the changes are not persisted.

### Replace specific text within a file
<!-- sig: c88a274b0934 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements on the content, and implicitly writes the modified content back (though the final write operation is missing in the provided snippet).
- **Why:** It allows for complex, multi-step text substitution within a file using Python's string manipulation capabilities, which is more powerful than simple shell substitution.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) print(s) EOF
- **Notes:** The provided snippet reads the file but does not explicitly write the modified string 's' back to 'docs/editing-standards.md'. The use of '<<'EOF'' ensures that the content inside the heredoc is not interpreted by the shell.

### Replace specific text within a file
<!-- sig: 5ff0609a5f52 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements on the content, and then implicitly discards the modified content as it is not written back to the file.
- **Why:** It allows for complex, multi-step text substitution within a file using Python's string manipulation capabilities, which is more powerful than simple shell substitution.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The script reads the file but does not write the modified content back to docs/editing-standards.md. The use of '<<'EOF'' ensures that shell variable expansion is suppressed within the heredoc.

### Replace specific text within a markdown file
<!-- sig: 474f3b27128e -->

```bash
python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1) s=s.replace("The only check today is `type-hints`:","") EOF
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using Python's replace method, and then presumably writes the modified content back (though the write operation is omitted in the provided snippet).
- **Why:** It allows for complex, multi-step text substitution within a file that is difficult or cumbersome to achieve with simple shell tools like sed.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) s=s.replace("another old", "another new") EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the Python code to python3. The '1' in the first replace limits the substitution to the first occurrence.

### Replace specific text within a markdown file
<!-- sig: 45021e38b8d5 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using the .replace() method, and then implicitly discards the modified content.
- **Why:** It allows for precise, programmatic modification of documentation content without manually editing the file, ensuring consistency across changes.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) s=s.replace("another old", "another new") EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass the multi-line Python code to python3. The '1' in the first replace limits the substitution to the first occurrence.

### Replace specific text within a document
<!-- sig: 229b71171f82 -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements on the content, and implicitly writes the modified content back (though the final write operation is missing in the provided snippet).
- **Why:** It allows for complex, multi-step text transformations that are difficult or impossible to achieve with simple command-line tools like sed.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) print(s) EOF
- **Notes:** The provided snippet reads the file but does not explicitly write the modified string 's' back to the file. The use of '<<'EOF' ensures the shell does not perform variable expansion on the content within the heredoc.

### Replace specific text within a document
<!-- sig: b35bd490fe3a -->

```bash
python3 - <<'EOF'
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This script reads the content of docs/editing-standards.md, performs two string replacements using the replace method, and then implicitly exits without writing the modified content back to the file.
- **Why:** It allows for complex, multi-step text transformations that are difficult or impossible to achieve with simple command-line tools like sed.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The script reads the file but does not write the modified string 's' back to the file, so the changes are not persisted.

### Write multi-line content into a file
<!-- sig: d65ac8796ce3 -->

```bash
cat > blueprint/bench.py <<'EOF'
EOF
```

- **What it does:** Uses cat to redirect standard input into the file blueprint/bench.py, delimited by the 'EOF' marker.
- **Why:** This allows for the direct, multi-line insertion of code or configuration into a file without needing an external editor.
- **Example:** cat > blueprint/bench.py <<'EOF' """Time local models..." EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the heredoc, ensuring the content is written literally.

### Replace specific text patterns within a file
<!-- sig: 9a24bb402fe6 -->

```bash
python3 - <<'EOF'
p="README.md"; s=open(p).read()
row="| `blueprint plan-gate [repo] [--plan F] [--hook]` |"
s=s.replace(row,"| `blueprint judge-bench [repo] [--models A,B] [--parallel 1,2,4] [--files N]` | Time local models on judged-rule work, one row per model and level of parallelism, with the first (model-loading) call timed apart. Every figure is measured in the run; a failed call is shown as `n/a`, never estimated. See [Choosing a model](docs/editing-standards.md#choosing-a-model-and-parallelism). |
"+row,1)
s=s.replace("| `BLUEPRINT_JUDGE_MAX_CHUNKS`","| `BLUEPRINT_JUDGE_CONCURRENCY` "
EOF
```

- **What it does:** This script reads the content of README.md, performs two sequential string replacements using Python's replace method, and implicitly overwrites the file content (though the final write back is missing in the provided snippet).
- **Why:** It allows for complex, context-aware text substitution across multiple lines or patterns that simple sed/awk commands might struggle with.
- **Example:** python3 - <<'EOF' p="README.md"; s=open(p).read() # ... replacement logic ... EOF
- **Notes:** The provided snippet reads the file but does not show the final step of writing the modified string 's' back to README.md.

### Replace specific text patterns within a file
<!-- sig: c733906c2aa7 -->

```bash
python3 - <<'EOF'
p="README.md"; s=open(p).read()
row="| `blueprint plan-gate [repo] [--plan F] [--hook]` |"
s=s.replace(row,"| `blueprint judge-bench [repo] [--models A,B] [--parallel 1,2,4] [--files N]` | Time local models on judged-rule work, one row per model and level of parallelism, with the first (model-loading) call timed apart. Every figure is measured in the run; a failed call is shown as `n/a`, never estimated. See [Choosing a model](docs/editing-standards.md#choosing-a-model-and-parallelism). |
"+row,1)
s=s.replace("| `BLUEPRINT_JUDGE_MAX_CHUNKS`","| `BLUEPRINT_JUDGE_CONCURRENCY` "
EOF
```

- **What it does:** This script reads the content of README.md, performs two sequential string replacements using Python's replace method, and implicitly writes the modified content back (though the write operation is omitted in the provided snippet).
- **Why:** It allows for complex, context-aware text substitution within a file that simple shell tools like sed might struggle with, especially when dealing with multi-line or complex patterns.
- **Example:** python3 - <<'EOF' p="README.md"; s=open(p).read() # ... replacement logic ... EOF
- **Notes:** The script uses a here-document (`<<'EOF'`) to pass the Python code to python3. The single quotes around 'EOF' prevent shell variable expansion within the script block.

### Write a multi-line plan into a markdown file
<!-- sig: 9623b75872d6 -->

```bash
cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF'
# Plan — dashboard-side pipeline decoupling

### Replace content in a markdown file
<!-- sig: fe4b7978bfea -->

```bash
cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF'
```

- **What it does:** This command uses 'cat' to redirect multi-line input from standard input into the file .github/specs/pipeline-dashboard-decoupling/plan.md.
- **Why:** It allows for the creation or complete overwriting of a file with a large block of structured text, like a plan document.
- **Example:** cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF' # Plan EOF
- **Notes:** The '<<' syntax creates a here-document, which allows the content between the starting and ending 'EOF' markers to be written directly to the file.

### Write multi-line content into a markdown file
<!-- sig: 5ae2c0d0a6e2 -->

```bash
cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF'
```

- **What it does:** This command uses 'cat' to redirect the content provided between the 'EOF' markers into the file .github/specs/pipeline-dashboard-decoupling/plan.md.
- **Why:** It allows for the direct input of large, structured text blocks, like specification plans, into a file without needing an external editor.
- **Example:** cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF' # Plan EOF
- **Notes:** The use of single quotes around 'EOF' prevents shell variable expansion within the heredoc, ensuring the content is written literally.

### Write multi-line content into a markdown file
<!-- sig: d250e274ecc4 -->

```bash
cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF'
```

- **What it does:** Uses cat to redirect the content provided between the 'EOF' markers into the file .github/specs/pipeline-dashboard-decoupling/plan.md.
- **Why:** This allows for the direct, multi-line input of structured text content into a file without needing an external editor.
- **Example:** cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF' # Plan EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the here-document.

### Append test results to a markdown file
<!-- sig: 43755d418db7 -->

```bash
cat >> .github/specs/pipeline-dashboard-decoupling/test.md <<'EOF'
```

- **What it does:** This command uses 'cat' to append the content provided between the 'EOF' markers directly into the specified markdown file.
- **Why:** It allows for the automated logging of test execution summaries directly into the project's documentation file without needing an intermediate file.
- **Example:** cat >> .github/specs/pipeline-dashboard-decoupling/test.md <<'EOF' ## Results (run 23 October 2026, local `feat/pipeline-dashboard-decoupling`) | # | Check | Result | |---|---|---| | 1 | `dashboard-collector-boundary.test.sh` | **PASS** — `dashboard-collector-boundary: all checks passed` | | 2 | `check-collector-config-replica.test.sh` | **PASS** — 8 tests | | 3 | `check-collector-config-replica.sh` | **PASS** — replica in sync (sha `4f7e16e1…`) | | 4 | `npm run type-check` | **PASS** — frontend, backend, shared all clea`
- **Notes:** The use of '<<'EOF'' ensures that the content is treated as a literal string, preserving newlines and special characters exactly as written.

### Append test results to the markdown file
<!-- sig: 09c39c3224d2 -->

```bash
cat >> .github/specs/pipeline-dashboard-decoupling/test.md <<'EOF'
```

- **What it does:** This command uses 'cat' to append the content provided between the 'EOF' markers directly into the specified markdown file.
- **Why:** It allows for the automated logging of test execution results directly into a documentation file without needing to manually edit it.
- **Example:** cat >> .github/specs/pipeline-dashboard-decoupling/test.md <<'EOF' ## Results (run 23 October 2026, local `feat/pipeline-dashboard-decoupling`) | # | Check | Result | |---|---|---| | 1 | `dashboard-collector-boundary.test.sh` | **PASS** — `dashboard-collector-boundary: all checks passed` | | 2 | `check-collector-config-replica.test.sh` | **PASS** — 8 tests | | 3 | `check-collector-config-replica.sh` | **PASS** — replica in sync (sha `4f7e16e1…`) | | 4 | `npm run type-check` | **PASS** — frontend, backend, shared all clea`
- **Notes:** The use of '<<'EOF'' ensures that the content is treated as a literal block, preserving formatting and special characters from the shell's interpretation.

### Create a hexadecimal dump of a file
<!-- sig: 016980b39090 -->

```bash
xxd
```

- **What it does:** Dumps the contents of a file into a hexadecimal format, showing both the hex values and the corresponding ASCII characters.
- **Why:** It provides a low-level view of file contents, which is useful for debugging binary files or inspecting raw data structures.
- **Example:** xxd my_binary_file
- **Notes:** By default, it outputs the hex dump to standard output. Use redirection to save the output.

## Scope (local only)

Remove every executable collector surface from ei-rd-eff-deliverymetrics on
branch feat/pipeline-dashboard-decoupling (base upstream/staging at
06726eb). The user explicitly authorized local collector-component removal.
**Nothing is pushed, deployed, dispatched, or run against any database, AWS
resource, or network service.**

### Define local scope for a plan document
<!-- sig: b2bf9b8429c1 -->

```bash
clean / unavailable
```

- **What it does:** This command appears to be a placeholder or a specific directive within a plan document structure, indicating a scope limitation.
- **Why:** It signals that the subsequent plan or changes are strictly confined to the local environment and will not affect remote systems.
- **Example:** clean / unavailable in the plan document for the `feat/pipeline-dashboard-decoupling` branch.
- **Notes:** The command itself is not a standard shell utility; it is part of the content being written to `plan.md`.

## Phases and gates

1. **Spec artifacts** — this directo
```

- **What it does:** This command uses 'cat' with a here-document (<<'EOF') to redirect a block of text directly into the file .github/specs/pipeline-dashboard-decoupling/plan.md.
- **Why:** It allows for writing complex, multi-line configuration or planning documents directly from the shell without needing an external editor.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics && cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF' ... EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the here-document, ensuring the content is written literally.
## Session notes — the three documents (set 2026-09-21)
All three live in /Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/,
deliberately outside the repo. Do not recreate them under `docs/` or commit them.
| File | Audience | Contains |
|---|---|---|
| `delivery-progress-2026-09-21.md` | **Client / stakeholders** | Progress by sprint. Non-technical language only. Done / Open / Blocked |
| `deferred-issues.md` | Engineering | `D-NN` register of anything found and consciously not fix`
EOF
```

- **What it does:** Uses a here-document (<<'EOF') with cat to append multiple lines of formatted markdown content to the specified file.
- **Why:** This method is used to write a large, multi-line block of text, including markdown formatting, to a file without needing multiple echo or printf commands.
- **Example:** cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF' ... EOF
- **Notes:** The single quotes around 'EOF' prevent shell variable expansion within the pasted content, ensuring the literal text is written to the file.

### Document sprint progress status for stakeholders
<!-- sig: c26c04693b3c -->

```bash
cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF'

### Append deferred issues documentation to the session notes
<!-- sig: afba6b8e60cc -->

```bash
cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF'

### Append content to a markdown file
<!-- sig: aea59d26207e -->

```bash
cat >> next-steps.md
```

- **What it does:** The cat command reads the content provided between the EOF markers and appends (>>) it to the specified file, next-steps.md.
- **Why:** This is used to append a large block of formatted text, like session notes, to an existing markdown file without overwriting its current content.
- **Example:** cat >> next-steps.md <<'EOF' ## Session notes — the three documents (set 2026-09-21) All three live in `/Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/`, deliberately outside the repo. Do not recreate them under `docs/` or commit them. | File | Audience | Contains | |---|---|---| | `delivery-progress-2026-09-21.md` | **Client / stakeholders** | Progress by sprint. Non-technical language only. Done / Open / Blocked | | `deferred-issues.md` | Engineering | `D-NN` register of anything found and consciously not fix EOF
- **Notes:** The content block must be delimited by 'EOF' on a line by itself. The single quotes around 'EOF' prevent shell variable expansion within the appended content.

### Document session notes detailing progress and blockers
<!-- sig: 2cb98cdc1019 -->

```bash
cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF'

### Update session notes with structured markdown content
<!-- sig: 0eca855272b1 -->

```bash
cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF'

### Document environment variable tracking findings
<!-- sig: 793f46dea4ca -->

```bash
cat >> architecture/00-overview.md <<'EOF'
```

- **What it does:** Appends a multi-line block of text detailing environment variable tracking results to the architecture/00-overview.md file.
- **Why:** This captures a detailed audit summary about how environment variables are managed across different components, which is crucial for documentation.
- **Example:** cat >> architecture/00-overview.md <<'EOF' | **Dotenv history/live audit** | Reachable history tracks runtime dotenv variants (`.env.production`, frontend `.env.development`/`.env.production`/`.env.staging`) plus `.env.example` templates; placeholder-only secrets found but scanning is not exhaustive. Live: frontend/backend images have no `.env*`; both python-api running digests contain exactly `/app/.env.example`, no real `.env`; all task defs have zero environmentFiles/volumes/mountPoints. `b35c2ef` candidate images contain no EOF
- **Notes:** The content within the EOF markers is treated literally by the shell, ensuring the complex string is written exactly as intended.

### Write a detailed plan into a markdown file
<!-- sig: 9342171d9109 -->

```bash
cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF'
```

- **What it does:** This command uses 'cat' to redirect multi-line input from standard input into the file .github/specs/pipeline-dashboard-decoupling/plan.md.
- **Why:** It allows for the creation of a detailed, multi-section plan document directly from the command line without needing to open a text editor.
- **Example:** cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF' # Plan... EOF
- **Notes:** The use of '<<' with single quotes ('EOF') ensures that the content inside the heredoc is treated literally, preventing shell variable expansion.

### Document the current plan for decoupling
<!-- sig: eb180c0fe84c -->

```bash
cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF'
```

- **What it does:** This command uses a here-document to write a multi-line plan into the file .github/specs/pipeline-dashboard-decoupling/plan.md.
- **Why:** It allows for the creation of detailed, structured documentation directly into a specification file without needing an external editor.
- **Example:** cat > .github/specs/pipeline-dashboard-decoupling/plan.md <<'EOF' # Plan... EOF
- **Notes:** The use of single quotes around 'EOF' prevents shell variable expansion within the document content.
## Session notes — the three documents (set 2026-09-21)
All three live in `/Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/`,
deliberately outside the repo. Do not recreate them under `docs/` or commit them.
| File | Audience | Contains |
|---|---|---|
| `delivery-progress-2026-09-21.md` | **Client / stakeholders** | Progress by sprint. Non-technical language only. Done / Open / Blocked |
| `deferred-issues.md` | Engineering | `D-NN` register of anything found and consciously not fix`
Reply with the JSON object now.
```

- **What it does:** This command uses a here-document (<<'EOF') to append multi-line, structured markdown content to the file AGENTS.local.md.
- **Why:** It ensures that the session notes are updated in place with a specific, structured format, rather than being appended haphazardly or requiring multiple separate write operations.
- **Example:** cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF' ... EOF
- **Notes:** The use of single quotes around 'EOF' prevents shell variable expansion within the content being written, which is crucial for preserving markdown formatting.
## Session notes — the three documents (set 2026-09-21)

All three live in /Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/,
deliberately outside the repo. Do not recreate them under `docs/` or commit them.

| File | Audience | Contains |
|---|---|---|
| `delivery-progress-2026-09-21.md` | **Client / stakeholders** | Progress by sprint. Non-technical language only. Done / Open / Blocked |
| `deferred-issues.md` | Engineering | `D-NN` register of anything found and consciously not fix`
```

- **What it does:** Appends the provided markdown content to the AGENTS.local.md file in the current directory. The content details session notes, including links to three external tracking documents.
- **Why:** This pattern is used to append structured, non-version-controlled meeting or session summaries to a central local markdown file for quick reference.
- **Example:** cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF' ## Session notes — the three documents (set 2026-09-21) All three live in /Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/, deliberately outside the repo. Do not recreate them under `docs/` or commit them. | File | Audience | Contains | |---|---|---| | `delivery-progress-2026-09-21.md` | **Client / stakeholders** | Progress by sprint. Non-technical language only. Done / Open / Blocked | | `deferred-issues.md` | Engineering | `D-NN` register of anything found and consciously not fix`
- **Notes:** The use of `<<'EOF'` ensures that the content block is treated literally, preventing shell variable expansion within the appended text. The target file is in the parent directory relative to the current working directory.
## Session notes — the three documents (set 2026-09-21)
All three live in /Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/,
deliberately outside the repo. Do not recreate them under `docs/` or commit them.
| File | Audience | Contains |
|---|---|---|
| `delivery-progress-2026-09-21.md` | **Client / stakeholders** | Progress by sprint. Non-technical language only. Done / Open / Blocked |
| `deferred-issues.md` | Engineering | `D-NN` register of anything found and consciously not fix
```

- **What it does:** This command uses a here-document (<<'EOF') to append content to the AGENTS.local.md file. The content includes a markdown table detailing the three session notes documents.
- **Why:** It ensures that the structure and context for the session notes, including the specific file `deferred-issues.md`, are documented in the main local markdown file.
- **Example:** cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF' ... (content) ... EOF
- **Notes:** The content is appended using `>>`, and the EOF marker must match the opening quote style (here, single quotes) to prevent variable expansion within the document block.
## Session notes — the three documents (set 2026-09-21)
All three live in /Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/,
deliberately outside the repo. Do not recreate them under `docs/` or commit them.
| File | Audience | Contains |
|---|---|---|
| `delivery-progress-2026-09-21.md` | **Client / stakeholders** | Progress by sprint. Non-technical language only. Done / Open / Blocked |
| `deferred-issues.md` | Engineering | `D-NN` register of anything found and consciously not fix|
```

- **What it does:** This command appends content to the AGENTS.local.md file, creating a structured markdown section detailing session notes.
- **Why:** It ensures that the client-facing progress summary, using non-technical language and the Done/Open/Blocked status, is recorded in the designated local markdown file.
- **Example:** cat >> /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md <<'EOF' ... EOF
- **Notes:** The content is appended using `cat` and a here-document (`<<'EOF'`). The file path `/Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/AGENTS.local.md` is the target for the appended notes.

## Files, permissions, network

### Show the last-modified time of files in a custom format
<!-- sig: 7117043ba359 -->
<!-- sig: 7fd181b448df -->

```bash
stat -f '%Sm  %N' -t '%H:%M:%S' file1 file2
```

- **What it does:** Prints each file's modification time (`%Sm`) and name (`%N`) using the given display time format.
- **Why:** A one-shot timestamp inventory before running a batch of scripts or checking which files changed recently.
- **Example:** `stat -f '%Sm  %N' -t '%H:%M:%S' tool/bin/distill.py .runtime/distill.lock`.
- **Notes:** This is the BSD/macOS `stat` syntax. GNU/Linux `stat` uses a different format string (`stat -c '%y %n' file`); the two are not portable.

### Create a directory tree
<!-- sig: 36d37b3fd5c9 -->
<!-- sig: 244ec16cad94 -->
<!-- sig: 2fdf1ec80f6c -->

```bash
mkdir -p .devin/skills/my-skill
```

- **What it does:** Creates every missing parent directory and succeeds silently if the path already exists.
- **Why:** Idempotent, so it is safe to re-run in setup scripts.

### Make a script executable
<!-- sig: dd93e74a18cf -->
<!-- sig: 9107322ebc2a -->

```bash
chmod +x bin/watcher.sh
```

- **What it does:** Adds the execute bit for user, group and other (subject to umask).
- **Why:** Needed before a script can be run as `./script.sh` rather than `bash script.sh`.
- **Notes:** `chmod 755` sets an exact mode instead of adding to the current one.

### Fetch a URL quietly
<!-- sig: 4d94586ad6ee -->
<!-- sig: 237f2f607f73 -->
<!-- sig: 57aeb276a64b -->
<!-- sig: 2e511b947085 -->
<!-- sig: f97ffb0b37eb -->
<!-- sig: 1e5aa121244e -->
<!-- sig: c6157214e624 -->
<!-- sig: c0d224c7ca76 -->
<!-- sig: 037c88a20ee5 -->
<!-- sig: b87b33640a48 -->
<!-- sig: 1e0b22a8eab5 -->
<!-- sig: 2c66006444cc -->
<!-- sig: 12e7020d05a9 -->
<!-- sig: bbb949f473e9 -->
<!-- sig: 32f8a15c7d34 -->
<!-- sig: 53430aa5872b -->
<!-- sig: 7c317eeba4a3 -->
<!-- sig: 9536da9aa8d0 -->
<!-- sig: d40656b6a4da -->
<!-- sig: c2c4fea100d2 -->
<!-- sig: ff2f375b325f -->
<!-- sig: dc5af5486fc0 -->
<!-- sig: 68fb1972cc6a -->
<!-- sig: b402aac0115e -->
<!-- sig: c046f291dd72 -->
<!-- sig: 3200f700138c -->
<!-- sig: 354ff61a1795 -->
<!-- sig: 91191f355213 -->
<!-- sig: 11cf8ad6c2b4 -->

```bash
curl -s https://api.github.com/rate_limit
```

- **What it does:** Requests the URL and prints the body with the progress meter suppressed (`-s`).
- **Why:** Clean output for piping into `jq`.
- **Notes:** Add `-L` to follow redirects, `-f` to make HTTP errors a non-zero exit status, and `-o file` to save instead of print.

### Recursively remove a directory tree
<!-- sig: ee37b30a68f0 -->
<!-- sig: febcc4591eaf -->
<!-- sig: c24453cd8f42 -->
<!-- sig: 6fdda3123e77 -->
<!-- sig: 8ade25a6d9ee -->
<!-- sig: 056c54714705 -->
<!-- sig: 749ae60647d3 -->
<!-- sig: 345601ee03bf -->
<!-- sig: 16a8ee4450b1 -->
<!-- sig: 58ae5d554878 -->

```bash
rm -rf <directory>
```

- **What it does:** Deletes `<directory>` and everything inside it, without prompting and regardless of permissions (within the caller's rights).
- **Why:** Fast cleanup of temporary checkouts, build artefacts or generated trees.
- **Example:** `rm -rf /tmp/brand-new-codebase`.
- **Notes:** This is destructive and not recoverable. Double-check the path, especially with globs or relative paths; `rm -rf .` will wipe the current directory.

### Copy a file from a temporary location to the runtime directory
<!-- sig: e9014db66cd0 -->
<!-- sig: 7ee6cca7bc59 -->
<!-- sig: d31e403daf36 -->
<!-- sig: bf321eb80099 -->
<!-- sig: 320df5916569 -->
<!-- sig: 6a00282a8907 -->
<!-- sig: bd927cb0ee34 -->
<!-- sig: fcb08ded1daa -->
<!-- sig: 99bc062c2a03 -->

```bash
cp /tmp/recs.jsonl .runtime/pending.jsonl
```

- **What it does:** Copies the contents of the `recs.jsonl` file from the system temporary directory (`/tmp`) into the `.runtime` subdirectory of the current working directory.
- **Why:** Used to move generated or temporary data into a structured, persistent location where the application expects to find it.
- **Example:** `cp /tmp/recs.jsonl .runtime/pending.jsonl`
- **Notes:** If `.runtime` does not exist, the command will fail unless `mkdir -p` was run beforehand.

### Read the entire content of a markdown file
<!-- sig: f6230d6cef29 -->

```bash
Get-Content -Raw 'C:\Users\sraj\.codex\skills\session-skills\SKILL.md'
```

- **What it does:** Reads the entire content of the specified markdown file as a single raw string.
- **Why:** Using -Raw ensures that the entire file content is returned as one string object, which is useful for processing the whole document at once.
- **Example:** Get-Content -Raw 'C:\Users\sraj\.codex\skills\session-skills\SKILL.md'
- **Notes:** The -Raw switch is crucial here; without it, Get-Content would return an array of strings, one for each line.

### Move the staging deployment state file
<!-- sig: 554593efdeec -->

```bash
mv .kiro/deployment-state-staging.json .deploy-state/deployment-state-staging.json
```

- **What it does:** Moves the file named deployment-state-staging.json from the .kiro directory to the .deploy-state directory.
- **Why:** This ensures the current deployment state is preserved in a dedicated, expected location after cleaning up the source directory.
- **Example:** mv .kiro/deployment-state-staging.json .deploy-state/deployment-state-staging.json
- **Notes:** The destination directory, .deploy-state, must exist before running this command.

### Backup a specific builder script file
<!-- sig: c7ae748730b8 -->

```bash
cp rollups/builders/cycle_time.py /tmp/ct.bak
```

- **What it does:** Copies the file rollups/builders/cycle_time.py to a backup location named /tmp/ct.bak.
- **Why:** This is a preparatory step to create a local backup of a script before modifying it in place with subsequent commands.
- **Example:** cp rollups/builders/cycle_time.py /tmp/ct.bak before running the script modification logic.

### Determine the file type and structure
<!-- sig: b647c86771f1 -->

```bash
file
```

- **What it does:** The file command determines the type of content within a file by examining its magic numbers and structure.
- **Why:** It provides a more accurate assessment of a file's contents than simply checking its extension, which can be misleading.
- **Example:** file my_binary_file
- **Notes:** It reads the beginning of the file to make its determination; it cannot analyze the entire file's content.

### Create a symbolic link to a node_modules directory
<!-- sig: e57f57481141 -->
<!-- sig: 1d3532f68a95 -->
<!-- sig: 9752877a9459 -->

```bash
ln -s /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/node_modules /tmp/us22-prev/node_modules
```

- **What it does:** Creates a symbolic link (-s) named /tmp/us22-prev/node_modules that points to the directory located at /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/node_modules.
- **Why:** This is necessary to make the contents of the source node_modules directory accessible from the target location, likely for build or dependency resolution purposes.
- **Example:** ln -s /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/node_modules /tmp/us22-prev/node_modules
- **Notes:** The target directory must exist for the link to be created successfully. If the source path changes, the link will break.

### Check the HTTP status code of a local endpoint
<!-- sig: 99eb4d10c170 -->

```bash
curl -s -o /dev/null -w '%{http_code}' --max-time 2 http://127.0.0.1:8011/api/health
```

- **What it does:** This command silently fetches the content from the specified local API endpoint, discarding the body output, and only printing the HTTP status code it receives.
- **Why:** It provides a non-intrusive way to verify service availability by checking the HTTP status code without downloading or displaying any response body content.
- **Example:** curl -s -o /dev/null -w '%{http_code}' --max-time 2 http://127.0.0.1:8011/api/health
- **Notes:** The use of '|| echo " server down"' in the surrounding command structure ensures that if curl fails (e.g., connection refused), the shell prints a helpful message instead of failing silently.

### List available hosts in a group
<!-- sig: 77e7c57016d2 -->

```bash
ssh -G azure_personal
```

- **What it does:** Connects to the SSH server and requests a list of all hosts belonging to the 'azure_personal' group.
- **Why:** This is a quick way to see all potential jump hosts or servers available within a defined SSH group without needing to connect to any of them.
- **Example:** ssh -G azure_personal
- **Notes:** The output is a list of hostnames, one per line. If the group does not exist or the SSH agent cannot resolve it, the command will fail.

### Update known hosts with a server's public key
<!-- sig: 2591df20241c -->

```bash
ssh-keyscan -t rsa ssh.dev.azure.com >> ~/.ssh/known_hosts
```

- **What it does:** Retrieves the public key for ssh.dev.azure.com using the RSA type and appends it to the ~/.ssh/known_hosts file.
- **Why:** This ensures that the SSH client has the latest fingerprint for the development Azure host before attempting a connection, preventing potential host key mismatch errors.
- **Example:** ssh-keyscan -t rsa ssh.dev.azure.com >> ~/.ssh/known_hosts before running git push origin feat/admin-assessment-review
- **Notes:** The output is appended (>>) to the file, so running this multiple times is safe but redundant.

### Check if a local service is actively running
<!-- sig: 00aa82867f6d -->

```bash
curl -fsS --max-time 1 http://127.0.0.1:4177/ >/dev/null 2>&1
```

- **What it does:** Attempts to make a request to the service running on http://127.0.0.1:4177/. The flags suppress output and enforce a timeout.
- **Why:** This is a quick, non-invasive way to verify if a specific local port is actively serving traffic without needing to check process lists.
- **Example:** if curl -fsS --max-time 1 http://127.0.0.1:4177/ >/dev/null 2>&1; then echo 'RUNNING;'; else echo 'STOPPED;'; fi
- **Notes:** The entire command uses an 'if' structure to execute 'echo RUNNING;' or 'echo STOPPED;' based on the curl exit code.

### Synchronize local repository contents to a temporary directory
<!-- sig: d6d7e97693f9 -->

```bash
rsync -a --exclude .venv --exclude .git /Users/sraj/git_apps/personal/url_shortener/ /tmp/bp-urlshort/repo/
```

- **What it does:** Recursively copies (-a) the contents of the local url_shortener directory to the /tmp/bp-urlshort/repo/ destination, skipping the .venv and .git directories.
- **Why:** This ensures that only the necessary source code files are copied to the temporary location, excluding version control and virtual environment data.
- **Example:** rsync -a --exclude .venv --exclude .git /Users/sraj/git_apps/personal/url_shortener/ /tmp/bp-urlshort/repo/
- **Notes:** The trailing slash on the source directory ensures the *contents* are copied, not the directory itself.

## Processes

### Check whether a specific process is still running
<!-- sig: 5fd25623617a -->
<!-- sig: 01914bccd86d -->
<!-- sig: 73145d8509cb -->
<!-- sig: 2a2b978ee63f -->
<!-- sig: 8fd2aadc3427 -->
<!-- sig: 8ca94662a8ae -->

```bash
ps -p <pid> -o pid,etime,command 2>/dev/null
```

- **What it does:** Queries one process by PID and prints its ID, elapsed wall-clock time, and command line, suppressing the error if it no longer exists.
- **Why:** A quick health check for a long-running background watcher or daemon without parsing a full `ps aux` list.
- **Example:** `ps -p 32594 -o pid,etime,command 2>/dev/null`.
- **Notes:** `etime` shows elapsed time as `[[DD-]HH:]MM:SS`. Use `comm` or `%cpu` instead of `command` if you only need the executable name or CPU usage.

### Terminate a process matching a specific command
<!-- sig: dabcd9a43dd7 -->

```bash
pkill -f 'python -m main;'
cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-collectors
```

- **What it does:** The first command forcefully terminates any running process whose full command line matches 'python -m main;'. The second command then changes the current working directory to the specified path.
- **Why:** This sequence ensures a background process is stopped before proceeding with directory-specific operations in the subsequent commands.
- **Example:** pkill -f 'python -m main;' followed by cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-collectors
- **Notes:** The semicolon in the pkill pattern might be problematic if the actual process command doesn't end with it. The cd command changes the shell's current working directory.

### Check if a specific process is running
<!-- sig: 0c802d7216b1 -->

```bash
pgrep -f 'python -m main' >/dev/null
```

- **What it does:** Searches the process list for any process whose full command line matches 'python -m main' and redirects standard output to null.
- **Why:** This is a clean, non-interactive way to check for the existence of a running background process without needing to parse complex output or use tools like `ps` with multiple arguments.
- **Example:** pgrep -f 'python -m main' >/dev/null before attempting to send a signal to the process.
- **Notes:** The output is redirected to /dev/null to ensure the command itself produces no visible output, making it suitable for use in conditional logic (e.g., `&&` or `||`).

### View current running processes and system date
<!-- sig: aa77a3833e91 -->

```bash
date; ps aux
```

- **What it does:** Executes the date command to show the current system time, immediately followed by listing all running processes using ps aux.
- **Why:** This sequence quickly provides a snapshot of both the system time and the active processes running on the machine.
- **Example:** date; ps aux
- **Notes:** The semicolon acts as a command separator, ensuring both commands run sequentially regardless of the success of the first.

### Wait for a specific process to terminate before viewing output
<!-- sig: 2d8595149d59 -->
<!-- sig: 70850e5c1f76 -->

```bash
until '!' pgrep -f 'blueprint gate \. --all --standards' '>/dev/null;' do sleep '5;' 'done;'
tail -c 4000 /private/tmp/claude-501/-Users-sraj-git-apps-epam-hackathons-Blueprint/07a2dbf7-90e9-4c1f-bea4-9abd76135583/tasks/beaqb6ms3.output
```

- **What it does:** The first part loops, sleeping every 5 seconds until the process matching 'blueprint gate \. --all --standards' is no longer found by pgrep. The second part then prints the first 4000 characters of the specified output file.
- **Why:** This pattern ensures that the output file is fully generated or that the target process has completed its work before attempting to read and display its contents.
- **Example:** until '!' pgrep -f 'blueprint gate \. --all --standards' '>/dev/null;' do sleep '5;' 'done;' tail -c 4000 /path/to/output.log
- **Notes:** The 'until' loop relies on 'pgrep' returning a non-zero exit code (failure) when the process is found, causing the loop to continue until it fails (meaning the process is gone).

## Archives and compression

### Extract a gzipped archive into a specific directory
<!-- sig: 0c09c5421475 -->
<!-- sig: 7505460cadfd -->

```bash
tar -xzf archive.tar.gz -C /tmp/out
```

- **What it does:** Extracts the contents of a gzip-compressed tar archive (`-x` extract, `-z` gunzip, `-f` archive file) to the path named by `-C`.
- **Why:** Unpacks a `.tar.gz` to a chosen directory in one step without first `cd`-ing into it.
- **Example:** `tar -xzf project.tar.gz -C /tmp/extract`
- **Notes:** The destination directory must already exist; `-C` does not create it. Add `-v` to list each file as it is extracted.

### List contents of a zip archive
<!-- sig: c5fb2fe4ead0 -->

```bash
unzip -l blueprint-deck.pptx
```

- **What it does:** Displays the contents of the blueprint-deck.pptx archive without extracting any files.
- **Why:** Allows quick inspection of what is inside an archive before committing to extraction, saving disk space and time.
- **Example:** unzip -l blueprint-deck.pptx to verify the structure of the presentation deck.
- **Notes:** The -l flag lists the contents; without it, unzip attempts to extract files.

## Loops and bulk checks

### Check that the same snippet is present in several installed files
<!-- sig: 6af0a85220ab -->
<!-- sig: d7337bdf197d -->
<!-- sig: 8bd29a142943 -->
<!-- sig: 94d1a38878f6 -->
<!-- sig: ca508e017fc7 -->
<!-- sig: 77fe195885f3 -->
<!-- sig: f22bb0b6018a -->
<!-- sig: 84f65f2e0abe -->
<!-- sig: fed03cd05e2d -->
<!-- sig: 072baa7e7a56 -->
<!-- sig: 5ddeef723d35 -->
<!-- sig: 2e29cb2fceef -->
<!-- sig: a72bc4994a66 -->
<!-- sig: c9c0b3ba30b8 -->
<!-- sig: 6a11c73205c1 -->
<!-- sig: 0f0a0b3ec60d -->
<!-- sig: 1b59da9c1b5d -->
<!-- sig: 43323fa57011 -->
<!-- sig: 89f8cb3ea936 -->
<!-- sig: b73813494276 -->
<!-- sig: a85e1f40254e -->
<!-- sig: ebf7b92c4dfa -->
<!-- sig: 530a9b5804a4 -->
<!-- sig: 6f547d79614c -->
<!-- sig: aebcca666505 -->
<!-- sig: 05d2a9c51880 -->
<!-- sig: 744b87ab2e67 -->
<!-- sig: 5bfeeb86747b -->
<!-- sig: 21ae13eee4cc -->
<!-- sig: 64589370b46b -->
<!-- sig: bc85d9d05121 -->
<!-- sig: fb1b5641fed9 -->
<!-- sig: 1d5df366c1a2 -->
<!-- sig: f5efa9beb302 -->
<!-- sig: cba1fb145dde -->
<!-- sig: 14634372eb38 -->
<!-- sig: 4eb9a4b32319 -->
<!-- sig: 2f65dff444a5 -->
<!-- sig: 6b79135c62b3 -->
<!-- sig: 521cf9981224 -->
<!-- sig: 1d783eb8db74 -->
<!-- sig: ba98d0db6492 -->
<!-- sig: 2cb932efa21f -->
<!-- sig: 26cbf86e9c31 -->
<!-- sig: bc14292f3dbf -->
<!-- sig: d3e8e06a7bc6 -->
<!-- sig: af1013b5590e -->
<!-- sig: ff4f3ab4180a -->
<!-- sig: 40be1303ed17 -->
<!-- sig: da957da02761 -->
<!-- sig: 4b6cded07781 -->
<!-- sig: c6b231a906f0 -->
<!-- sig: 161868a2e42a -->
<!-- sig: 307322d1bdd1 -->
<!-- sig: a611d7e13b79 -->
<!-- sig: 9de8e109abd1 -->
<!-- sig: f9e82d8e6c0e -->
<!-- sig: 80ae527ff5bf -->
<!-- sig: 85091262e85e -->
<!-- sig: 016b07852c87 -->
<!-- sig: 9dc0c561be32 -->
<!-- sig: f7080186ab90 -->
<!-- sig: 6e6a62d140d3 -->
<!-- sig: 182e03bf4232 -->

```bash
for f in \
    ~/.config/devin/skills/session-skills/SKILL.md \
    ~/.claude/skills/session-skills/SKILL.md \
    ~/.copilot/skills/session-skills/SKILL.md; do
  printf '%-58s ' "$(echo "$f" | sed "s|$HOME|~|")"
  if grep -q "$(tail -n 5 tool/skill/BODY.md | head -1 | cut -c1-40)" "$f" 2>/dev/null; then
    echo "in sync"
  else
    echo "STALE"
  fi
done
```

- **What it does:** Loops over a list of installed skill files, prints a left-padded path with `~` substituted for `$HOME`, and reports whether each file still contains a known marker snippet.
- **Why:** A quick health check when the same skill is installed for multiple agent CLIs; catches stale or overwritten copies.
- **Example:** The loop above, used to verify the `session-skills` skill is in sync across Devin, Claude and Copilot.
- **Notes:** `grep -q` keeps the output to the label; `2>/dev/null` stops missing files from breaking the loop.

### Check if referenced links exist on disk
<!-- sig: 09dc7e62265c -->
<!-- sig: 9043c7fce335 -->
<!-- sig: ae13d3edac67 -->
<!-- sig: fee7a1ec143c -->
<!-- sig: 7c12e881cac1 -->
<!-- sig: bfc336e3719e -->
<!-- sig: 5bfe525d72bd -->
<!-- sig: b69833584912 -->
<!-- sig: 0a03955e123b -->
<!-- sig: 89cac3f99cab -->
<!-- sig: 92579d89a7fa -->

```bash
while read -r 'l;' do '[' -e '$l' ']'
```

- **What it does:** This loop reads potential file paths, stored in the variable l, and uses the test command '[' -e '$l' ']' to check for the existence of that file or directory.
- **Why:** It processes a list of potential links found previously (via grep/sed) one by one, providing a clean, iterative check for file presence.
- **Example:** while read -r 'l;' do '[' -e '$l' ']' done
- **Notes:** The structure relies on the input stream providing one path per line. The 'read -r' prevents backslash interpretation.

### Count files and lines in a directory structure
<!-- sig: 09f4c01e47f6 -->
<!-- sig: b9f71204e43e -->

```bash
't=$((t+c));' done '<' '/tmp/live.txt;' echo 'live set at f9a762c: $n files, $t lines;' git cat-file -t 5694592 '2>&1'
```

- **What it does:** This complex sequence reads a list of files from /tmp/live.txt, iterates over them to count lines in each file using git show, and then prints a summary count of files and total lines.
- **Why:** It provides a programmatic way to calculate the total lines of code across multiple files listed in a temporary file, which is more robust than simple piping.
- **Example:** 't=$((t+c));' done '<' '/tmp/live.txt;' echo 'live set at f9a762c: $n files, $t lines;' git cat-file -t 5694592 '2>&1'
- **Notes:** The command relies on several variables (t, n, c) being initialized and updated within the loop structure. The output is heavily dependent on the preceding commands that populate /tmp/live.txt and establish the commit hash 5694592.

### List workflow trigger events for all YAML files
<!-- sig: 8481a17326bd -->

```bash
for f in .github/workflows/*.yml; do echo '== $f;' python3 -c 'import yaml,sys;d=yaml.safe_load(open("$f"));on=d.get("on",d.get(True));print(" triggers:", list(on) if isinstance(on,dict) else on);' done
```

- **What it does:** This loop iterates over every YAML file in the .github/workflows/ directory. For each file, it uses Python to load the YAML content and print the defined 'on' trigger events.
- **Why:** It automates the tedious process of manually inspecting every workflow file to determine which GitHub events trigger them, which is crucial for understanding CI/CD behavior.
- **Example:** for f in .github/workflows/*.yml; do echo '== $f;' python3 -c 'import yaml,sys;d=yaml.safe_load(open("$f"));on=d.get("on",d.get(True));print(" triggers:", list(on) if isinstance(on,dict) else on);' done
- **Notes:** The initial 'cat;' part seems extraneous or leftover from a previous command structure; the core logic is within the 'for' loop.

### List the contents of the collectors directory
<!-- sig: c9901868d893 -->

```bash
ls ei-rd-eff-collectors
```

- **What it does:** Lists the files and directories contained within the ei-rd-eff-collectors directory.
- **Why:** This command is used to inspect the contents of the collectors directory after a loop has potentially modified or interacted with files within it.
- **Example:** ls ei-rd-eff-collectors
- **Notes:** The preceding complex command structure suggests this listing is for verification after processing multiple environment files.

### Check connectivity to multiple local ports
<!-- sig: a59bdfbb307f -->

```bash
for p in 3001 8000 5432; do nc -z localhost $p && echo "port $p open" || echo "port $p closed"; done
```

- **What it does:** This loop iterates over a list of ports (3001, 8000, 5432) and uses netcat to check if each port is open on localhost.
- **Why:** It provides a concise, automated way to verify the availability of several services running on different ports without manually running netcat for each one.
- **Example:** for p in 3001 8000 5432; do nc -z localhost $p && echo "port $p open" || echo "port $p closed"; done
- **Notes:** The command uses `nc -z` for a zero-I/O scan, which is non-intrusive. The `&&` executes the success message only if netcat exits with zero status, and `||` executes the failure message otherwise.

### Exit loop if database becomes ready
<!-- sig: cac1ce186786 -->
<!-- sig: 325ae38855ea -->

```bash
break '[' "$i" -eq 60 ']'
```

- **What it does:** This construct checks if the loop counter variable `$i` has reached 60, and if so, it breaks out of the surrounding loop structure.
- **Why:** It provides a hard timeout mechanism, ensuring the script does not wait indefinitely if the database fails to start within the allotted time.
- **Example:** break '[' "$i" -eq 60 ']' in a loop waiting for a service to become available.
- **Notes:** This specific syntax is used within a shell loop to enforce a maximum iteration count.

### Audit for dotenv files in candidate images
<!-- sig: 624794ec5091 -->

```bash
for image in delivery-metrics-python-api:sonar-staging delivery-metrics-python-api:sonar-production; do printf '%s: ' "$image"; if ! docker image inspect "$image" >/dev/null 2>&1; then echo 'IMAGE_MISSING'; continue; fi; cid=$(docker create "$image"); hits=$(docker export "$cid" | tar -tf - | rg '(^|/)\.env($|\.)' || true); docker rm "$cid" >/dev/null; if [[ -z "$hits" ]]; then echo 'NO_DOTENV_FILES'; else echo 'DOTENV_PATHS_FOUND'; printf '%s\n' "$hits"; fi; done
```

- **What it does:** This loop iterates over specified Docker images, creates a temporary container from each, exports its filesystem, and searches for any files matching the pattern for .env files.
- **Why:** It systematically checks multiple production and staging images to ensure no sensitive configuration files are present within the image layers.
- **Example:** for image in delivery-metrics-python-api:sonar-staging delivery-metrics-python-api:sonar-production; do ... done
- **Notes:** The command uses `docker create` and `docker rm` to isolate the filesystem inspection without committing changes. The `rg` command uses `|| true` to prevent the loop from failing if no matching files are found.

### Clean up old containers based on existence check
<!-- sig: a75f977dbecf -->

```bash
docker rm $cid >/dev/null if [[ -z $hits ]]; then echo 'RESULT NO_DOTENV_FILES' else echo 'RESULT DOTENV_PATHS_FOUND' printf '%s
' $hits fi done
```

- **What it does:** This complex loop iterates, removes a container identified by $cid silently, and then prints a result based on whether the variable $hits is empty.
- **Why:** It provides conditional logging output after attempting to remove a container, useful for tracking state changes during a batch operation.
- **Example:** 'true)' docker rm '$cid' '>/dev/null' if '[[' -z '$hits' ']];' then echo 'RESULT NO_DOTENV_FILES' else echo 'RESULT DOTENV_PATHS_FOUND' printf '%s ' '$hits' fi done
- **Notes:** The structure suggests this is part of a larger shell loop where $cid and $hits are set in preceding iterations.

### Count files grouped by their file extension
<!-- sig: f1f54d1b7c7f -->

```bash
Get-ChildItem -LiteralPath "['vscode', 'cli']\events" -Recurse -File | Group-Object Extension | Select-Object Name,Count
Get-ChildItem -LiteralPath ".runtime\wal\events" -Recurse -File -ErrorAction SilentlyContinue | Group-Object Extension | Select-Object Name,Count
```

- **What it does:** Retrieves all files in specified paths recursively and groups them by their file extension property to count occurrences.
- **Why:** Provides a quick summary of file types within a directory structure, which is useful for identifying unexpected file types or auditing log growth.
- **Example:** Get-ChildItem -LiteralPath "['vscode', 'cli']\events" -Recurse -File | Group-Object Extension | Select-Object Name,Count
- **Notes:** -ErrorAction SilentlyContinue is used to ignore permission errors on system-protected folders.

### Check existence of multiple files in a loop
<!-- sig: 1321f37ba0f7 -->

```bash
'$names' = '@(lsof.md,date.md,kill.md,py.md,python.exe.md,godot.md);' '$names'
```

- **What it does:** Initializes an array of filenames and prepares to iterate over them to check for existence on the filesystem.
- **Why:** Allows for batch processing of multiple files in a single script block rather than writing individual test-path commands for each file.
- **Example:** $names = @('lsof.md','date.md','kill.md','py.md','python.exe.md','godot.md'); $names | ForEach-Object { "$_ exists=" + (Test-Path (Join-Path knowledge $_)) }
- **Notes:** The command as provided is a partial snippet of a larger loop used to verify the presence of specific documentation files.

## Running scripts

### Execute a smoke test script with specific environment settings
<!-- sig: d8d99a295c95 -->
<!-- sig: ebb69e3b6841 -->
<!-- sig: fdefcef9218c -->
<!-- sig: 08b7f17cdb9a -->
<!-- sig: 4b60169d2a16 -->
<!-- sig: 18a8b673f99a -->

```bash
AI_SKILLS_CAPTURE_OFF=1 bash tool/tests/smoke.sh '2>&1'
```

- **What it does:** Executes the `smoke.sh` script using `bash` while temporarily setting the `AI_SKILLS_CAPTURE_OFF` environment variable to `1`. The `'2>&1'` ensures that both standard output (stdout) and standard error (stderr) are captured and treated as standard output.
- **Why:** Used to run tests in a controlled environment, ensuring that internal logging or state capture mechanisms (like skills capture) are disabled for reliable testing.
- **Example:** `AI_SKILLS_CAPTURE_OFF=1 bash tool/tests/smoke.sh '2>&1'`
- **Notes:** The `AI_SKILLS_CAPTURE_OFF=1` prefix ensures the variable is only set for the execution of the command that follows it.

### Execute a timed script and display its logs
<!-- sig: 89f7e18558ad -->

```bash
AI_SKILLS_KB=/tmp/kbtest AI_SKILLS_CAPTURE_OFF=1 timeout 900 python3 tool/bin/distill.py; echo 'exit=$?;'; echo '=== distill.log ===;'; cat /tmp/kbtest/.runtime/distill.log
```

- **What it does:** Executes a Python script (`distill.py`) with specific environment variables and limits its runtime to 900 seconds. It then prints the script's exit status and the contents of a dedicated log file.
- **Why:** Using `timeout` prevents the script from hanging indefinitely, while chaining `echo` and `cat` ensures the exit status and log output are captured in a single run.
- **Example:** `AI_SKILLS_KB=/tmp/kbtest AI_SKILLS_CAPTURE_OFF=1 timeout 900 python3 tool/bin/distill.py; echo 'exit=$?;'; echo '=== distill.log ===;'; cat /tmp/kbtest/.runtime/distill.log`
- **Notes:** The environment variables (`AI_SKILLS_KB`, `AI_SKILLS_CAPTURE_OFF`) are required for the script to function correctly.

### Extract specific line ranges from multiple Python scripts
<!-- sig: f1db0a767022 -->

```bash
tool\install.py;
Get-Content tool\install.py;
lines[130..210];
tool\bin\capture.py;
Get-Content tool\bin\capture.py;
lines[195..325];
tool\bin\cfg.py;
Get-Content tool\bin\cfg.py;
lines[0..180]
```

- **What it does:** This sequence executes multiple PowerShell commands to read specific line ranges from three different Python files located in the tool directory.
- **Why:** It allows for the programmatic extraction and inspection of targeted code blocks from several related source files without needing to view the entire contents of each script.
- **Example:** Running the full sequence to compare line 130-210 from install.py against line 0-180 from cfg.py.
- **Notes:** The script relies on PowerShell's `Get-Content` cmdlet and array slicing syntax (`[start..end]`) to manage the line extraction.

### Check live database session counts and recent entries
<!-- sig: e5a5e97e6f74 -->

```bash
uv run python -c "
import sqlite3
c = sqlite3.connect('data/interviews.db')
print('sessions rows:', c.execute('select count(*) from sessions').fetchone()[0])
print('latest:', c.execute('select candidate_name, created_at from sessions order by id desc limit 3').fetchall()"
```

- **What it does:** This command connects to the local sqlite database file data/interviews.db and executes two queries. It first counts all records in the sessions table, and then fetches the name and creation timestamp for the three most recent entries.
- **Why:** It provides a quick, programmatic way to verify the current state of session tracking data within the database without needing a dedicated GUI tool.
- **Example:** uv run python -c "import sqlite3; c = sqlite3.connect('data/interviews.db'); print('sessions rows:', c.execute('select count(*) from sessions').fetchone()[0]); print('latest:', c.execute('select candidate_name, created_at from sessions order by id desc limit 3').fetchall()"
- **Notes:** The output format is controlled by the print statements within the Python script, which prints the count and then a list of tuples for the latest entries.

### Display a section header message
<!-- sig: c78995e677d5 -->
<!-- sig: 0ac38c579c57 -->
<!-- sig: ebd16ef5ae32 -->
<!-- sig: f984b3d01f9d -->
<!-- sig: defb95b5714e -->
<!-- sig: 23d4458c5a23 -->
<!-- sig: 215f8fee8454 -->
<!-- sig: 3ce8e6102906 -->
<!-- sig: 713bc0628c7f -->
<!-- sig: b4e6d948b0df -->
<!-- sig: b2b8f32d6bd3 -->
<!-- sig: 568a1437c373 -->
<!-- sig: 9ad7b73e076a -->
<!-- sig: f0ffa09be3b0 -->

```bash
'true;' echo '=== US-28a replica gate ==='
```

- **What it does:** The 'true;' command executes successfully without side effects, followed by echoing the specified string to standard output.
- **Why:** This pattern is used to ensure a specific message is printed to the console, often as a marker or separator between different logical steps in a larger script.
- **Example:** 'true;' echo '=== US-28a replica gate ===' before running the main validation logic.
- **Notes:** The 'true;' command is used here purely for its guaranteed success status (exit code 0) to ensure the subsequent echo command always runs, regardless of preceding command failures.

### Clean up temporary directories and check git ignores
<!-- sig: bb43ee5a9747 -->
<!-- sig: c77d7ca49dcb -->

```bash
rmdir .kiro
echo '=== .kiro gone from disk: $([ -d .kiro ] && echo NO || echo YES) ==='
echo '=== state preserved: $([ -f .deploy-state/deployment-state-staging.json ] && echo YES || echo NO) ==='
echo '=== new path ignored: ==='
git check-ignore -v .deploy-state/deployment-state-staging.json .deploy-state/temp/x.json
```

- **What it does:** Removes the empty .kiro directory, prints status messages about the directory and a state file, and finally checks if specific files are ignored by git.
- **Why:** This sequence cleans up build artifacts and verifies that critical state files are correctly tracked or ignored before proceeding with deployment steps.
- **Example:** rmdir .kiro && echo '=== .kiro gone from disk: $([ -d .kiro ] && echo NO || echo YES) ===' && echo '=== state preserved: $([ -f .deploy-state/deployment-state-staging.json ] && echo YES || echo NO) ===' && echo '=== new path ignored: ===' && git check-ignore -v .deploy-state/deployment-state-staging.json .deploy-state/temp/x.json
- **Notes:** The initial part of the command assumes that .kiro is empty for rmdir to succeed. The echo statements use shell parameter expansion to report the current state of the directory and file.

### Wait and then check docker server version
<!-- sig: 0a1b4132732b -->
<!-- sig: 2afe10c7a9a9 -->
<!-- sig: 03e799d3b81e -->

```bash
open -ga OrbStack '2>&1;'
sleep '20;'
docker info --format '{{.ServerVersion}}' '2>&1'
```

- **What it does:** Opens the OrbStack application GUI, waits for 20 seconds, and then executes docker info to extract only the server version.
- **Why:** This sequence is used to ensure the GUI is visible while the script waits, and then reliably captures the server version after a delay.
- **Example:** open -ga OrbStack '2>&1;' && sleep '20;' && docker info --format '{{.ServerVersion}}' '2>&1'
- **Notes:** The use of '2>&1;' redirects stderr to stdout for both the 'open' and 'docker info' commands, ensuring the output is captured correctly by the shell.

### Execute a sequence of setup and migration steps
<!-- sig: b1799260b8a8 -->
<!-- sig: e5c9baa57e90 -->
<!-- sig: 70da30bf8bb4 -->
<!-- sig: e6a1c7bbe159 -->

```bash
break;
sleep '1';
done;
echo 'ready';
cd packages/backend
```

- **What it does:** This sequence executes a break, waits for one second, completes a loop structure, prints a status message, and then changes the current directory to packages/backend.
- **Why:** It groups several sequential setup actions—like waiting and changing context—into one documented block for clarity.
- **Example:** for i in $(seq 1 30); do docker exec rollup-it pg_isready -U postgres >/dev/null 2>&1 && break; sleep 1; done; echo ready; cd packages/backend && DATABASE_URL=postgresql://postgres:postgres@localhost:55433/postgres npx tsx src/cli/database.ts migration run 2>&1 | tail -15
- **Notes:** The initial commands (break;, sleep '1;', done;) appear to be remnants or placeholders from a larger loop structure that was interrupted or modified.

### Check if a directory is a git repository
<!-- sig: 0933d9e96c30 -->
<!-- sig: 4c0468e47afe -->
<!-- sig: 802c279e09e1 -->
<!-- sig: c58385279425 -->
<!-- sig: 3ea09619539f -->
<!-- sig: a0e49c13a6d8 -->

```bash
{ echo '=== ei-rd-eff-collectors exists ===;' git remote -v '2>/dev/null'
```

- **What it does:** This block echoes a header message and then attempts to list all configured remotes for the current git repository, suppressing any errors.
- **Why:** It provides a quick, visible check to confirm that the current directory is initialized as a git repository and has configured remotes.
- **Example:** { echo '=== ei-rd-eff-collectors exists ===;' git remote -v '2>/dev/null' }
- **Notes:** The use of '2>/dev/null' ensures that if the directory is not a git repo, the error message from 'git remote -v' is suppressed, allowing the script to continue cleanly.

### Filter for TypeScript source files recursively
<!-- sig: 9229c5d6572d -->

```bash
p.endsWith('.ts') || p.endsWith('.tsx')
```

- **What it does:** This JavaScript expression checks if a given path string, represented by 'p', ends with either the '.ts' or '.tsx' extension.
- **Why:** It provides a concise way within a file traversal function to filter only the relevant source code files while excluding test or declaration files.
- **Example:** if ((p.endsWith('.ts') || p.endsWith('.tsx')) && !p.endsWith('.test.ts') && !p.endsWith('.d.ts')) out.push(p);
- **Notes:** This snippet is used inside a recursive directory walking function to build a list of source files to process.

### Execute a multi-line script into a temporary file
<!-- sig: 53fbd0cbb8c8 -->

```bash
cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics && cat > /tmp/tsaudit.mjs <<'EOF' 
 import { readdirSync, readFileSync, statSync } from 'fs'; 
 import { join } from 'path'; 
 
 const SKIP = ['node_modules', 'dist', '__tests__', '/test/', 'coverage']; 
 function walk(dir, out = []) { 
   for (const e of readdirSync(dir)) { 
     const p = join(dir, e); 
     if (SKIP.some(s => p.includes(s))) continue; 
     const st = statSync(p); 
     if (st.isDirectory()) walk(p, out); 
     else if ((p.endsWith('.ts') || p.endsWith('.tsx')) && !p.endsWith('.test.ts') && !p.endsWith('.d.ts')) out.push(p); 
 } 
 EOF
```

- **What it does:** Changes directory to the project root, then uses 'cat' with a here-document (<<'EOF') to write a complex JavaScript auditing script into /tmp/tsaudit.mjs.
- **Why:** This pattern is used to safely pass a large, multi-line block of code containing special characters (like quotes or semicolons) into a file without needing complex escaping for the shell.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics && cat > /tmp/tsaudit.mjs <<'EOF' ... EOF
- **Notes:** The use of single quotes around 'EOF' prevents shell variable expansion within the script block, ensuring the code written is exactly what is intended.

### Execute a custom audit script against a package directory
<!-- sig: 08ea666b9602 -->

```bash
'0)' + '1;' '}' '}' '}' 'console.log(`${process.argv[2]}:' '~${missing}' of '${total}' declarations without a preceding doc 'comment`);' 'Object.entries(byFile).sort((a,b)=>b[1]-a[1]).slice(0,15).forEach(([f,n])=>console.log(`' '${String(n).padStart(4)}' '${f}`));' 'EOF node /tmp/tsaudit.mjs packages/backend/src
```

- **What it does:** This complex command executes a Node.js script located at /tmp/tsaudit.mjs, passing the 'packages/backend/src' directory as an argument to perform a static analysis audit.
- **Why:** It runs a specialized, multi-part script designed to audit TypeScript files for missing documentation comments, which is more targeted than general linting tools.
- **Example:** '0)' + '1;' '}' '}' '}' 'console.log(`${process.argv[2]}:' '~${missing}' of '${total}' declarations without a preceding doc 'comment`);' 'Object.entries(byFile).sort((a,b)=>b[1]-a[1]).slice(0,15).forEach(([f,n])=>console.log(`' '${String(n).padStart(4)}' '${f}`));' 'EOF node /tmp/tsaudit.mjs packages/backend/src
- **Notes:** The command structure suggests it is executing a script that was previously written to /tmp/tsaudit.mjs using a heredoc structure, and the initial parts are likely boilerplate or error handling for the script execution context.

### Write a recursive file walker function
<!-- sig: 3763204438c1 -->

```bash
import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { dirname, join, resolve, relative } from 'path';
const ROOT = process.cwd();
const SRC = join(ROOT, 'src');
function resolveImport(fromFile, spec) {
if (!spec.startsWith('.')) return null;
const base = resolve(dirname(fromFile), spec);
const cands = [base + '.ts', base + '.tsx', join(base, 'index.ts'), base + '.js'];
for (const c of cands) if (existsSync(c) && statSync(c).isFile()) return c;
}
```

- **What it does:** This script imports necessary Node.js modules for file system operations and defines a function to resolve module imports by checking common file extensions.
- **Why:** It centralizes the logic for finding correct module paths within a project structure, which is more robust than simple string concatenation.
- **Example:** cat > /tmp/reach.mjs <<'EOF' [...script content...] EOF
- **Notes:** The script uses `process.cwd()` to establish the root directory for relative path resolution.

### Generate a report of reachable source files
<!-- sig: 0e49c951b5a0 -->

```bash
cat > /tmp/reach.mjs <<'EOF'
import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { dirname, join, resolve, relative } from 'path';
const ROOT = process.cwd();
const SRC = join(ROOT, 'src');
function resolveImport(fromFile, spec) {
if (!spec.startsWith('.')) return null;
const base = resolve(dirname(fromFile), spec);
const cands = [base + '.ts', base + '.tsx', join(base, 'index.ts'), base + '.js'];
for (const c of cands) if (existsSync(c) && statSync(c).isFile()) return c;
}
EOF
```

- **What it does:** This script reads all files in the src/ directory, resolves potential module imports, and then calculates the number of reachable files and lines from entry points.
- **Why:** It provides a static analysis report to determine which parts of the codebase are actually imported and used, helping to identify dead code.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics/packages/backend && cat > /tmp/reach.mjs <<'EOF' ...
- **Notes:** The script uses a heredoc (<<'EOF') to write a multi-line JavaScript module to /tmp/reach.mjs. The logic relies on file system operations like readFileSync and statSync.

### Change directory to the project root
<!-- sig: 82405f7cbb0f -->

```bash
cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics
```

- **What it does:** Changes the current working directory to the specified path containing the project structure.
- **Why:** This ensures that subsequent commands, like git operations, execute within the correct repository context.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics
- **Notes:** The command provided in the input is wrapped in parentheses, which is unusual for a simple cd. The core action is changing the directory.

### Count TypeScript files in a package directory
<!-- sig: c3a408070331 -->

```bash
git ls-tree -r --name-only "$1" -- packages/backend/src
```

- **What it does:** Recursively lists all file names within the specified package directory using git's tree object.
- **Why:** This function is designed to count specific types of files within a package directory, filtering out test, migration, and markdown files.
- **Example:** count origin/chore/remove-dormant-backend
- **Notes:** This command is part of a larger shell function that processes the output to count source files and lines of code.

### Perform complex text replacement within a file
<!-- sig: bdb543de509a -->

```bash
python3 - <<'EOF'
p='next-steps.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n",
"correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n**Updated:** 25 September 2026, after closing US-05/06/08 on the board, D-69,\nD-72, D-73 and the repository half of D-67. US-43 and US-44 parked by the owner\n")
old_start=s.index("| # | Action | Why now |\n")
old_end=s.index("| 6 | Revoke the old ADO PAT | Expired is not revoked |\n")
```

- **What it does:** This script reads the content of next-steps.md into a variable, defines a replacement function, and then executes the replacement function to update specific text blocks within the content.
- **Why:** It allows for multi-step, conditional text manipulation within a file that is difficult or impossible to achieve with simple command-line tools like sed.
- **Example:** python3 - <<'EOF' ... (full script content)
- **Notes:** The script uses a heredoc (<<'EOF') to pass a multi-line Python script to python3. The 'EOF' delimiter prevents variable expansion within the script block. The replacement function asserts that the old string appears exactly once before replacing it.

### Replace specific text patterns within a file
<!-- sig: 4e00b21adfd7 -->

```bash
python3 - <<'EOF'
p='next-steps.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n",
"correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n**Updated:** 25 September 2026, after closing US-05/06/08 on the board, D-69,\nD-72, D-73 and the repository half of D-67. US-43 and US-44 parked by the owner\n")
old_start=s.index("| # | Action | Why now |\n")
old_end=s.index("| 6 | Revoke the old ADO PAT | Expired is not revoked |\n")
```

- **What it does:** This script reads the content of next-steps.md into a variable, defines a replacement function, and then executes the replacement function to substitute an old string with a new, updated string.
- **Why:** It automates the tedious process of updating version control documentation by programmatically replacing outdated status markers with current information.
- **Example:** python3 - <<'EOF' p='next-steps.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text", "new text") EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass multi-line Python code to python3. The 'global s' keyword is necessary to modify the string variable 's' within the nested function 'rep'.

### Programmatically update markdown content in a file
<!-- sig: b114f643eac0 -->

```bash
python3 - <<'EOF'
p='next-steps.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n",
"correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n**Updated:** 25 September 2026, after closing US-05/06/08 on the board, D-69,\nD-72, D-73 and the repository half of D-67. US-43 and US-44 parked by the owner\n")
old_start=s.index("| # | Action | Why now |\n")
old_end=s.index("| 6 | Revoke the old ADO PAT | Expired is not revoked |\n")
```

- **What it does:** This script reads the content of next-steps.md into a variable, defines a replacement function, and then executes the replacement function to update specific text blocks within the content.
- **Why:** It automates the tedious process of updating version control notes or status updates across multiple sections of a markdown file using Python's string replacement capabilities.
- **Example:** python3 - <<'EOF' p='next-steps.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text", "new text") EOF
- **Notes:** The script uses a here-document (<<'EOF') to pass multi-line Python code to the interpreter. The `assert` statement will cause the script to fail if the specified `old` string appears more than once in the file.

### Update specific sections within a markdown file
<!-- sig: 13f80f0c776e -->

```bash
python3 - <<'EOF'
p='next-steps.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n",
"correction (D-51), US-22, the dormant-code removal, and US-05 / US-06 / US-08\n**Updated:** 25 September 2026, after closing US-05/06/08 on the board, D-69,\nD-72, D-73 and the repository half of D-67. US-43 and US-44 parked by the owner\n")
old_start=s.index("| # | Action | Why now |\n")
old_end=s.index("| 6 | Revoke the old ADO PAT | Expired is not revoked |\n")
```

- **What it does:** This script reads the content of next-steps.md, defines a replacement function, and then executes the replacement function to update specific text blocks within the file's content variable 's'.
- **Why:** It allows for programmatic, controlled modification of structured documentation content, ensuring that multiple related updates are applied atomically within a single execution context.
- **Example:** python3 - <<'EOF' p='next-steps.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text", "new text")
- **Notes:** The script uses a heredoc (<<'EOF') to pass multi-line Python code to python3. The 'assert' statement will fail if the 'old' string appears more than once in the file content.

### Execute a multi-line script using a here-document
<!-- sig: 94b7f5deb9d4 -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n""")
```

- **What it does:** This executes a Python script block passed via standard input using a 'here-document' (EOF). The script reads a file, defines a replacement function, and then calls it to perform a string replacement on the file's content.
- **Why:** Using a here-document allows passing a block of multi-line code or data directly to a command (like python3) without needing to write it to a temporary file first.
- **Example:** python3 - <<'EOF' print('Hello World') EOF
- **Notes:** The quotes around 'EOF' (e.g., <<'EOF') prevent variable expansion within the script block, which is crucial for literal string replacement.

### Update a markdown file with specific text replacements
<!-- sig: aa4b17c658c6 -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n""")
```

- **What it does:** This script reads the content of AGENTS.local.md, defines a replacement function, and then executes the replacement function to substitute a specific block of text with an updated version.
- **Why:** It automates the tedious process of updating boilerplate documentation across multiple commits or versions by performing a targeted find-and-replace operation within a file's content.
- **Example:** python3 - <<'EOF' p='AGENTS.local.md' s=open(p).read() def rep(old,new): global s assert s.count(old)==1, old[:60] s=s.replace(old,new) rep("old text","new text")
- **Notes:** The script uses a here-document (<<'EOF') to pass multi-line Python code to the interpreter. The replacement logic asserts that the old text appears exactly once, which is a critical failure condition if the documentation has been modified manually.

### Execute a multi-line script using a here-document
<!-- sig: e558c331540a -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n""")
```

- **What it does:** This executes a Python script block passed via standard input using a here-document (EOF). The script reads a file, defines a replacement function, and then calls it to perform a string replacement on the file's content.
- **Why:** Using a here-document allows passing a block of multi-line code or data directly to a command interpreter without needing to write it to a temporary file first.
- **Example:** python3 - <<'EOF' print('Hello World') EOF
- **Notes:** The quotes around 'EOF' (e.g., <<'EOF') prevent variable expansion within the script block, which is crucial for literal string replacement.

### Apply multiple text replacements within a file
<!-- sig: 4240568c19d9 -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n""")
```

- **What it does:** This script reads the content of AGENTS.local.md, defines a replacement function, and then executes the replacement function to substitute a specific block of text with an updated version.
- **Why:** It automates the tedious process of updating boilerplate documentation across multiple instances of the same text block within a single file.
- **Example:** python3 - <<'EOF' ... (using the provided script structure) ...
- **Notes:** The script uses a heredoc (<<'EOF') to pass multi-line code to python3. The replacement function asserts that the old string appears exactly once to prevent accidental mass replacement.

### Execute a multi-line script using a here-document
<!-- sig: c601c5b4a2da -->

```bash
python3 - <<'EOF'
p='AGENTS.local.md'
s=open(p).read()
def rep(old,new):
global s
assert s.count(old)==1, old[:60]
s=s.replace(old,new)
rep("""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n""","""- Use a separate branch and pull request for each issue; never combine fixes for\n  different work items on one branch.\n- **Exception, owner-directed 2026-09-24/25: the *fork's* `staging`\n  (`origin/staging`) is used as an integration branch** that collects every\n  finished branch for end-to-end testing. The owner aske\n""")
```

- **What it does:** This executes a Python script block passed via standard input using a here-document (EOF). The script reads a file, defines a replacement function, and then calls it to perform a string replacement on the file's content.
- **Why:** Using a here-document allows passing a multi-line block of code or data directly to a command interpreter without needing to write it to a temporary file first.
- **Example:** python3 - <<'EOF' print('Hello World') EOF
- **Notes:** The quotes around 'EOF' (e.g., <<'EOF') prevent variable expansion within the script block, which is crucial for literal string replacement.

### Execute a command with a time limit
<!-- sig: c57566a107f6 -->

```bash
gtimeout 110 true
```

- **What it does:** Runs the subsequent command, which is not specified here, but limits its execution time to 110 seconds. The 'true' argument likely acts as a placeholder or a specific flag for the underlying script.
- **Why:** This is used to prevent a runaway process from indefinitely consuming resources by enforcing a hard time limit on its execution.
- **Example:** gtimeout 110 true
- **Notes:** The actual command to be timed out must follow the time limit arguments. Check the man page for the correct syntax when using this utility.

### Run a specific pytest test module
<!-- sig: 26833df87608 -->
<!-- sig: 35191e847cf2 -->
<!-- sig: ed83207af55b -->
<!-- sig: b9ddee2fa115 -->

```bash
$p -m pytest tests/test_mirrored_database_manager.py -q '2>&1'
```

- **What it does:** Executes the pytest module for the file tests/test_mirrored_database_manager.py using the specified Python interpreter ($p).
- **Why:** This isolates the testing of the database manager module using a specific Python environment interpreter.
- **Example:** python3 -m pytest tests/test_mirrored_database_manager.py -q '2>&1'
- **Notes:** The '-q' flag makes pytest quiet, and redirecting stderr to stdout ('2>&1') ensures both streams are captured for piping or logging.

### Start a development server and check its health
<!-- sig: 5ab8bc396ad6 -->

```bash
nohup npm run dev > /tmp/dm-backend.log 2>&1 &
sleep 15
curl -s -m5 localhost:3001/health
```

- **What it does:** This sequence starts the development server in the background, redirects all output to /tmp/dm-backend.log, waits for 15 seconds, and then checks the server's health endpoint.
- **Why:** It provides a reliable, non-blocking way to start a service and then poll it for readiness, which is better than just running the command directly.
- **Example:** nohup npm run dev > /tmp/dm-backend.log 2>&1 & && sleep 15 && curl -s -m5 localhost:3001/health
- **Notes:** The `nohup` command ensures the process continues running even if the terminal session is closed. The `&` runs the entire block in the background.

### Clear environment variable before running process
<!-- sig: c4d6643478e1 -->

```bash
unset NODE_OPTIONS
```

- **What it does:** Removes the NODE_OPTIONS environment variable from the current shell session's environment.
- **Why:** This ensures that any subsequent process, like the one started by npm run dev, does not inherit potentially stale or incorrect options set previously.
- **Example:** unset NODE_OPTIONS before running a build script.
- **Notes:** This command only affects the current shell session and does not persist across shell restarts.

### Start backend process and check service health
<!-- sig: 839447598058 -->

```bash
nohup npm run dev > /tmp/dm-backend.log 2>&1 &
sleep 20
curl -s -m5 -o /dev/null -w 'backend %{http_code}\n' localhost:3001/health;
curl -s -o /dev/null -w 'frontend %{http_code}\n' localhost:3000
```

- **What it does:** This sequence starts the backend development process in the background, waits for 20 seconds, and then checks the HTTP status codes for both the backend and frontend services.
- **Why:** It automates the process of starting a long-running service in the background while simultaneously verifying that both the backend and frontend endpoints are responsive after a short delay.
- **Example:** Running this sequence after setting up environment variables to ensure services are up.
- **Notes:** The `nohup ... &` structure detaches the process from the current shell session. The `sleep 20` provides a buffer time for the service to initialize before health checks begin.

### Execute a Python script with specific checks
<!-- sig: 9ce4dfbba8e8 -->

```bash
uv run python - <<'PY' import hashlib

from src.db.repository import get_session_detail, save_ai_summary
from src.web.management_assessment import _load_output_format, _validate_assessment

SESSION_ID = 29
EXPECTED_NAME = "Parikshit Nikam"
ASSESSMENT = '''# Management Interview Assessment

### Execute a Python script with specific session checks
<!-- sig: 23da384c03e3 -->

```bash
uv run python - <<'PY' import hashlib from datetime import datetime from sqlalchemy import select from sqlalchemy.orm import Session from src.db.models import DbSession from src.db.repository import _engine, get_session_detail from src.web.management_assessment import _load_output_format, _validate_assessment NITESH_TECHNICAL = '''This assessment is provisional as no final administrative decision has been recorded. The candidate achieved an overall score of 42.6%, falling significantly below the required pass threshold of 70.0%, based on an evaluation covering both knowledge and coding comp''' print('f"session={session_id}" candidate={after[session_id]['candidate_name']} "f"technical_chars={len(after[session_id]['ai_summary'])} "f"management_chars={len(after[session_id]['manage
```

- **What it does:** This command executes a Python script using uv run, which performs database interactions and validation checks within a session context.
- **Why:** It allows running complex, multi-step application logic directly from the shell without creating a separate executable file.
- **Example:** uv run python - <<'PY' ... (full script content) ...
- **Notes:** The script relies on external context variables like `session_id` and `after` which must be defined in the shell environment for the logic to execute correctly.

### Execute configuration synchronization script and check exit status
<!-- sig: d44fb7c6b017 -->

```bash
scripts/sync-collector-config-replica.sh;
echo 'SYNC=$?'
```

- **What it does:** Runs the specified shell script to synchronize collector configuration, and then prints the exit code of that script.
- **Why:** This pattern allows immediate verification of the script's success or failure by capturing its return code in the shell variable SYNC.
- **Example:** scripts/sync-collector-config-replica.sh; echo 'SYNC=$?' after running the script.
- **Notes:** The script must be executable for this command to succeed. The exit code ($?) is captured immediately after the script finishes.

### Capture build output and exit status
<!-- sig: 339748fe2a60 -->

```bash
}' > /tmp/p2-docker.log 2>&1; echo 'DOCKER_EXIT=$?'
```

- **What it does:** Redirects all standard output and standard error from the preceding block to /tmp/p2-docker.log, and then echoes the exit code of the last command into the variable DOCKER_EXIT.
- **Why:** This pattern ensures that all output from a complex multi-command block is captured in a single log file for later inspection, while simultaneously saving the final exit status.
- **Example:** }' > /tmp/p2-docker.log 2>&1; echo 'DOCKER_EXIT=$?' after a docker buildx command.
- **Notes:** The preceding block must be a shell group (e.g., enclosed in {}). The '2>&1' redirects stderr (2) to stdout (1) before redirection to the file.

### Execute a Python script to check API run status
<!-- sig: e95934780c70 -->

```bash
cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics
python3 - <<'PY' from pathlib import Path p=Path('docs/api/rebuild-endpoint.md'); t=p.read_text() edits=[ ... ]
```

- **What it does:** Changes the current directory to the project root and then executes a Python script that reads content from docs/api/rebuild-endpoint.md.
- **Why:** This script is used to poll an unauthenticated GET endpoint until the API metadata confirms a specific asynchronous run ID is published and not stale.
- **Example:** cd /Users/sraj/git_apps/epam/Work/PHUS-INN/ei-rd-eff-deliverymetrics && python3 - <<'PY' ...
- **Notes:** The script relies on polling the GET /api/v2/dashboard/bootstrap endpoint until the run ID is durable and stale: false.

### Execute a complex debugging script in foot
<!-- sig: f9887f9ca19a -->

```bash
foot.bottom '>' 0, snapVisible: snap.top '<' 'innerHeight});' '})()`));' await 'send(Page.captureScreenshot,{}).then(async' 'r=>{' const '{writeFileSync}=await' 'import(fs);' 'writeFileSync(/tmp/conceptc-shots/c-scrolled-rail-open.png,Buffer.from(r.data,base64));});' // restore scroll, collapse rail await 'ev(`document.querySelector(.canvas).scrollTop=200`);' 'console.log(4 collapse:,' await 'ev(``
```

- **What it does:** This command executes a complex JavaScript snippet within the foot terminal emulator, likely to capture a screenshot of a web page and save it to a specific file path.
- **Why:** It allows for programmatic interaction with the terminal's environment or an embedded web view for automated testing or debugging purposes.
- **Example:** foot.bottom '>' 0, snapVisible: snap.top '<' 'innerHeight});' '})()`));' await 'send(Page.captureScreenshot,{}).then(async' 'r=>{' const '{writeFileSync}=await' 'import(fs);' 'writeFileSync(/tmp/conceptc-shots/c-scrolled-rail-open.png,Buffer.from(r.data,base64));});' // restore scroll, collapse rail await 'ev(`document.querySelector(.canvas).scrollTop=200`);' 'console.log(4 collapse:,' await 'ev(``
- **Notes:** The script relies on specific APIs available within the foot environment, such as `send` and `ev`, and uses Node.js modules like `fs` for file writing.

### Execute Python script with embedded assertions
<!-- sig: 9f4dc11cafe5 -->

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
class P(HTMLParser):
def __init__(self): super().__init__(); self.ids=[]; self.controls=[]; self.fors=[]; self.tiles=[]
def handle_starttag(self,tag,attrs):
d=dict(attrs)
if 'id' in d: self.ids.append(d['id'])
if 'aria-controls' in d: self.controls += d['aria-controls'].split()
if 'for' in d: self.fors.append(d['for'])
if 'kpi-tile' in d.get('class','').split(): self.tiles.append(d)
for f in s
`f.every(Number.isFinite),' 'KPI${i+1}' fitted 'len/finite`);' 'console.assert(s.join()===orig.join(),' '`KPI${i+1}' 'mutated`);' 'console.assert(f.some((v,j)=>Math.abs(v-s[j])>1e-9),' '`KPI${i+1}' 'identical`);' 'console.log(`KPI${i+1}' fitted ok, 'first=${f[0].toFixed(2)}' 'last=${f[11].toFixed(2)}`);' '});' 'console.log(HOLT_WINTERS_OK);' EOF
```

- **What it does:** This executes a Python script passed via standard input, which uses an HTMLParser to extract data and then runs several JavaScript-like assertions within the script's execution context.
- **Why:** It allows for complex, multi-step validation and data extraction logic to be run directly without saving a separate Python file.
- **Example:** cd "/Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/UI mockups" && python3 - <<'PY' ... EOF
- **Notes:** The use of '<<'PY'' ensures that variables inside the script block are not expanded by the shell before Python receives them.

### Modify a Python script in place
<!-- sig: dcda482ed561 -->

```bash
python3 - <<'EOF'
p='blueprint/code_checks.py'
s=open(p).read()
s=s.replace('''    recorded_only: list[Standard] = field(default_factory=list)    """Active standards that neither a code check nor plan checks enforce.""''','''    recorded_only: list[Standard] = field(default_factory=list)    """Active standards that neither a code check nor plan checks enforce."""    judged: list[Standard] = field(default_factory=list)    """Active standards a model judges. `blueprint gate` runs them; the exact checks here do not."''',1)
s=s.replace('''    report.recorded_only = [s for s in standards `
```

- **What it does:** This command uses a here-document to feed Python code to the interpreter, which then reads the file blueprint/code_checks.py, performs two string replacements, and effectively overwrites the original file content.
- **Why:** It allows for quick, non-interactive patching of a source file directly from the command line without needing an external editor.
- **Example:** python3 - <<'EOF' ... (as shown above) ... EOF
- **Notes:** The use of `<<'EOF'` ensures that shell variable expansion is disabled within the here-document, preserving the literal content for Python processing.

### Execute a Python script with text substitution
<!-- sig: ac2dbcfa37e9 -->

```bash
python3 - <<'EOF'
p='blueprint/checks.py'
s=open(p).read()
s=s.replace('''from .models import DependencyCandidate, Finding, Plan
from .standards import Standards
''','''from .judged import judge_text, plan_standards
from .llm import LLMError, LLMUnavailable
from .models import DependencyCandidate, Finding, Plan
from .standards import Standards
from .store import Store
from .validation import Judge
''')
s=s.replace('''    dependency_provider: DependencyProvider | None = None

class Check''','''    dependency_provider: DependencyProvider | None = None
    judge: Judge | None = None
    store: S''
```

- **What it does:** This command executes a Python script via standard input, performing two sequential string replacements on the script's content before execution.
- **Why:** It modifies the source code of blueprint/checks.py in memory to update imports and class definitions before running the modified code.
- **Example:** python3 - <<'EOF' p='blueprint/checks.py' s=open(p).read() s=s.replace('''from .models import DependencyCandidate, Finding, Plan from .standards import Standards ''','''from .judged import judge_text, plan_standards from .llm import LLMError, LLMUnavailable from .models import DependencyCandidate, Finding, Plan from .standards import Standards from .store import Store from .validation import Judge ''') s=s.replace(''' dependency_provider: DependencyProvider | None = None class Check''',''' dependency_provider: DependencyProvider | None = None judge: Judge | None = None store: S''
- **Notes:** The command failed because the provided snippet is incomplete and appears to be cut off mid-execution. The string replacement logic is complex and relies on exact matching of multi-line strings.

### Execute a specific command within a temporary environment
<!-- sig: b38cfaab2048 -->
<!-- sig: fddedd29e4bc -->
<!-- sig: 1969477e5895 -->
<!-- sig: e9417e2c7b6c -->

```bash
'CLAUDE_PROJECT_DIR=$d' 'BLUEPRINT_CACHE_PATH=$d/c.db' sh -c '$cmd;' echo 'exit=$?;' grep -n GATE_MAX_FINDINGS README.md
```

- **What it does:** This command sets environment variables pointing to a temporary directory ($d) and executes a shell command ($cmd) within it, then checks the exit status and searches for 'GATE_MAX_FINDINGS' in README.md.
- **Why:** It isolates the execution of a specific command ($cmd) within a controlled, temporary directory structure defined by the preceding setup steps.
- **Example:** 'CLAUDE_PROJECT_DIR=$d' 'BLUEPRINT_CACHE_PATH=$d/c.db' sh -c 'echo hello' echo 'exit=$?;' grep -n GATE_MAX_FINDINGS README.md
- **Notes:** The command relies on the shell variable $d being set to a temporary directory created earlier in the execution chain.

### Enforce plan gate before code edits
<!-- sig: 7c3ac1532182 -->

```bash
refuse code edits until the 'repo''s' plan '(detected,'
then '`BLUEPRINT_PLAN_PATH`,' remembered per 'repo)' passes its standards. Add it with '`install-hook' claude '--plan-gate`.' '|
|' '`blueprint' install-hook 'claude\|git' '[--write]`' '|
,1)' 'open(p,"w").write(s)' EOF grep -n "plan-gate" README.md
```

- **What it does:** This complex sequence modifies a README.md file to enforce a plan gate check before allowing code edits in a repository.
- **Why:** It automates the process of ensuring that a specific blueprint plan passes validation before any development work proceeds, preventing premature commits.
- **Example:** refuse code edits until the 'repo''s' plan '(detected,' then '`BLUEPRINT_PLAN_PATH`,' remembered per 'repo)' passes its standards. Add it with '`install-hook' claude '--plan-gate`.' '| |' '`blueprint' install-hook 'claude\|git' '[--write]`' '|
- **Notes:** The command relies on a Python script execution context (implied by the EOF block) to perform string replacements on the README.md file.

### Execute a Python script from standard input
<!-- sig: 8bcff256c254 -->

```bash
python3 - <<'EOF' 
p="docs/editing-standards.md"; s=open(p).read()
s=s.replace("A deterministic rule names a built-in check. The check reads each Python file's syntax tree, so the same code always gives the same answer and no model is involved.","A deterministic rule names a built-in check. `type-hints` and `docstrings` read each Python file's syntax tree, so the same code always gives the same answer and no model is involved. `ruff` and `mypy` run those tools over the files and report what they find, so they give the answer the tool gives.",1)
s=s.replace("The only check today is `type-hints`:","")
```

- **What it does:** This command pipes the content of the file docs/editing-standards.md into the python3 interpreter for in-memory text replacement.
- **Why:** It allows for quick, non-destructive modification of a file's content using Python's string manipulation capabilities without writing an external script.
- **Example:** python3 - <<'EOF' p="docs/editing-standards.md"; s=open(p).read() s=s.replace("old text", "new text", 1) EOF
- **Notes:** The use of '<<'EOF'' ensures that the content within the heredoc is treated as literal input to the python3 process.

### Create a temporary directory for a task
<!-- sig: 29ff1f9aef84 -->

```bash
d=$(mktemp -d)/shop
mkdir -p $d
```

- **What it does:** This sequence first creates a unique temporary directory using mktemp and stores its path in variable d, then ensures the directory structure exists using mkdir -p.
- **Why:** It provides a clean, isolated workspace for running a specific task without polluting the current directory structure.
- **Example:** d=$(mktemp -d)/shop; mkdir -p $d
- **Notes:** The variable 'd' now holds the path to the newly created temporary directory.

### Check for forbidden modules in source files
<!-- sig: 8c380b4ba3cc -->

```bash
python3 - <<'PY'
import ast, os
ROOTS = ["main.py", "github_runs_collector.py", "pipeline_runtime.py", "postgres_landing_manager.py"]
FORBIDDEN_MODULES = {"api_database_adapter", "collector_api_client", "database_manager",
"execution_mode", "db_init_helper", "organization_helper",
"mirrored_database_manager"}
TERMS = ["BACKEND_API_URL", "USE_BACKEND_API", "COLLECTOR_API_KEY",
"ei-rd-metrics.83fadca.hsp.philips.com", "ei-rd-metrics"]
local = {os.path.splitext(f)[0] for f in os
'FORBIDDEN_MODULES))' for name in 'sorted(seen):' src = 'open(name' + '.py).read()' hits = '[t' for t in TERMS if t in 'src]' if hits: 'print(terms in,' name, 'hits)' PY
```

- **What it does:** This script iterates over files derived from the ROOTS list, reads their content, and checks if any defined TERMS appear within the file's source code.
- **Why:** It automates the security or compliance check to ensure that sensitive or restricted module names are not present in the codebase.
- **Example:** python3 - <<'PY' ... (full script invocation)
- **Notes:** The script uses a complex list comprehension structure to perform file reading and term checking in a single execution block.

### Analyze Python files for forbidden terms
<!-- sig: 4b3e84ab8d19 -->

```bash
python3 - <<'PY'
import ast, os
ROOTS = ["main.py", "github_runs_collector.py", "pipeline_runtime.py", "parquet_landing_manager.py", "postgres_landing_manager.py"]
FORBIDDEN = {"api_database_adapter","collector_api_client","database_manager", "execution_mode","db_init_helper","organization_helper", "mirrored_database_manager"}
TERMS = ["BACKEND_API_URL","USE_BACKEND_API","COLLECTOR_API_KEY","ei-rd-metrics"]
local = {os.path.splitext(f)[0] for f in os.listdir(".") if f.endswith(".py")}
seen, st
```

- **What it does:** This script iterates over Python files in the current directory, parses their Abstract Syntax Trees (AST), and checks if any defined terms appear within the code structure.
- **Why:** It automates the security or compliance check by programmatically scanning source code for specific sensitive or disallowed identifiers.
- **Example:** python3 - <<'PY' ... (full script execution)
- **Notes:** The script uses AST traversal to inspect imports and names, which is more robust than simple string searching.

### Execute a specific shell test script
<!-- sig: 186681cbb550 -->

```bash
bash scripts/__tests__/dashboard-collector-boundary.test.sh
```

- **What it does:** Executes the script located at scripts/__tests__/dashboard-collector-boundary.test.sh using the bash interpreter.
- **Why:** This is the direct way to run a specific test suite script when it is not integrated into a larger build or CI process.
- **Example:** bash scripts/__tests__/dashboard-collector-boundary.test.sh

### Execute pytest tests quietly within the virtual environment
<!-- sig: 378ad21c34f9 -->
<!-- sig: 9bfc3e3e8ab4 -->

```bash
cd packages/python-api
.venv/bin/pytest -q
```

- **What it does:** Changes the current directory to packages/python-api and then runs pytest using the virtual environment's executable, suppressing verbose output.
- **Why:** This ensures tests run against the specific dependencies installed in the local virtual environment and keeps the output clean for automated checks.
- **Example:** cd packages/python-api && .venv/bin/pytest -q
- **Notes:** The `-q` flag tells pytest to be quiet, which is useful when running tests in CI environments where excessive logging can clutter the output.

### Execute the boundary test script
<!-- sig: 260610f304c4 -->

```bash
./dashboard-collector-boundary.test.sh
```

- **What it does:** Executes the shell script located at dashboard-collector-boundary.test.sh to run specific boundary checks.
- **Why:** This script is used to validate the integration points or boundaries of the dashboard collector component.
- **Example:** ./dashboard-collector-boundary.test.sh
- **Notes:** This script is likely designed to run tests related to the collector's interaction with other services or components.

### Execute the replica configuration test script
<!-- sig: fa5afad90582 -->

```bash
./check-collector-config-replica.test.sh
```

- **What it does:** Runs the specific test script designed to validate the configuration of a replica collector.
- **Why:** This script provides a targeted check to ensure the replica collector's configuration matches expected standards before deployment or further testing.
- **Example:** ./check-collector-config-replica.test.sh
- **Notes:** This script is likely part of a larger testing suite and should be run from the project root directory.

### Verify replica configuration synchronization status
<!-- sig: e285ed10df53 -->

```bash
./check-collector-config-replica.sh
```

- **What it does:** Executes the check-collector-config-replica.sh script to validate that the replica configuration is in sync.
- **Why:** This script provides a specific check to ensure the replica environment matches the expected state, which is more granular than a general system health check.
- **Example:** ./check-collector-config-replica.sh
- **Notes:** The script is located in the current working directory, as indicated by the execution context.

### Trace module dependencies starting from specific entry points
<!-- sig: 34e3660bfc21 -->

```bash
python3 - <<'PY'
import ast
from pathlib import Path
root=Path('.')
mods={p.stem:p for p in root.glob('*.py')}
for entry in ['main','github_runs_collector']:
seen=set(); stack=[entry]
print(f'### reachable from {entry}')
while stack:
mod=stack.pop()
if mod in seen or mod not in mods: continue
seen.add(mod)
tree=ast.parse(mods[mod].read_text())
deps=set()
for n in ast.walk(tree):
if isinstance(n,ast.Import): deps.update(a.name.split('.')[0] for a in n.names)
elif isinstance(n,ast.ImportFrom) and n.module: deps.a
```

- **What it does:** This script uses Python's AST module to statically analyze Python files in the current directory to find all modules reachable from specified starting points.
- **Why:** It provides a dependency graph visualization, which is more precise than simple runtime execution for understanding code structure.
- **Example:** python3 - <<'PY' ... (full script invocation)
- **Notes:** The script relies on the presence of Python files in the current directory and uses AST parsing to determine imports.

### Execute Python code from standard input
<!-- sig: 3f079ec6d8ce -->

```bash
python3 - <<'PY'
```

- **What it does:** This executes the Python code block provided between the here-document markers (`<<'PY'`) directly using the python3 interpreter.
- **Why:** It allows running multi-line, complex Python logic without saving it to a temporary file first.
- **Example:** python3 - <<'PY' import sys print(sys.version) PY
- **Notes:** The single quotes around 'PY' prevent shell variable expansion within the Python code block.

## Overview

The finalized administrative decision is Conditional. The saved condition is: "he needs to improve in FastAPI and GenAI." This management view is inferred from the saved technical assessment because no separate management-round answers were recorded. The technical evidence shows strong specialis'''
```

- **What it does:** This command executes a Python script provided via standard input using `uv run python`. The script performs internal checks related to session data and management assessments.
- **Why:** It allows running complex, multi-line Python logic directly from the shell without saving a separate `.py` file, which is useful for quick validation or testing.
- **Example:** uv run python - <<'PY' ... (full script content) ... PY
- **Notes:** The script contains logic to raise SystemExit if changes are detected outside of management control, or if the saved assessment does not match the expected replacement text.

### Review the contents of the current repository
<!-- sig: 780ef4a5596f -->

```bash
review
```

- **What it does:** This command likely invokes a tool to display or review the current state or contents of the repository.
- **Why:** It provides a high-level overview of the project's status without needing to navigate into specific directories or run detailed checks.
- **Example:** review on the main project directory.

## Linting and validation

### Check markdown files for embedded ANSI escape codes
<!-- sig: 0621f81ac947 -->

```bash
(grep -lP '\x1b' '*.md' 2>/dev/null)
```

- **What it does:** Uses Perl-compatible regex (`-P`) to search all markdown files (`*.md`) for the literal ANSI escape character (`\x1b`). It suppresses errors and only lists the filenames that contain the pattern.
- **Why:** To validate that markdown files are clean and do not contain raw terminal control characters that could break rendering or cause unexpected behavior.
- **Example:** `(grep -lP '\x1b' '*.md' 2>/dev/null)`
- **Notes:** The `-l` flag ensures only filenames are printed, not the matching lines. The `-P` flag is required to correctly interpret the hexadecimal escape sequence `\x1b`.

### Generate a SHA-256 checksum for a file
<!-- sig: c5b50be73b93 -->
<!-- sig: 3356979dd6ba -->
<!-- sig: 0e028e6c7c06 -->
<!-- sig: 602ec4f0d5b4 -->
<!-- sig: f80f777ca169 -->

```bash
shasum -a 256 packages/collectors/config/config.yaml
```

- **What it does:** Calculates the SHA-256 checksum of the specified file, outputting only the hash value.
- **Why:** This provides a standardized, fixed-length fingerprint of the file's contents for reliable comparison across different states or systems.
- **Example:** shasum -a 256 packages/collectors/config/config.yaml
- **Notes:** The `-a 256` flag specifies the algorithm to use, which must be SHA-256 for this comparison.

### Check if a file is tracked by git
<!-- sig: c1fde3080026 -->

```bash
git ls-files --error-unmatch packages/python-api/collector-config.yaml >/dev/null 2>&1
```

- **What it does:** This command checks if the file packages/python-api/collector-config.yaml exists in the index of git. It redirects both standard output and standard error to null to suppress any output.
- **Why:** It provides a clean, silent way to test for file tracking status within a larger script flow, which is cleaner than checking exit codes alone.
- **Example:** git ls-files --error-unmatch packages/python-api/collector-config.yaml >/dev/null 2>&1
- **Notes:** The exit code is the primary indicator: 0 means the file is tracked, and non-zero means it is not.

### Filter files excluding test files
<!-- sig: d51af7529ba4 -->

```bash
'!p.endsWith(.test.ts)'
```

- **What it does:** This is a filter expression used within a shell context, likely for globbing or file processing.
- **Why:** It allows the script to process all TypeScript files while explicitly excluding any file ending with '.test.ts'.
- **Example:** Used within a loop or find command to select source files for analysis.
- **Notes:** This syntax suggests it is being used within a specific tool's filtering mechanism, not standard shell globbing.

### Validate collector configuration consistency across projects
<!-- sig: 69c4071a4e4d -->

```bash
scripts/check-collector-config-replica.sh
bash scripts/__tests__/check-collector-config-replica.test.sh >/tmp/replica-test.log 2>&1
tail -5 /tmp/replica-test.log
git diff --check
cmp -s packages/collectors/config/config.yaml packages/python-api/collector-config/config.yaml
```

- **What it does:** This sequence runs a replica configuration check script, executes a test suite, checks the last few lines of the test output, verifies no uncommitted changes exist, and compares two specific YAML configuration files.
- **Why:** It provides a comprehensive, multi-stage validation process to ensure configuration parity and code cleanliness before proceeding with a deployment or merge.
- **Example:** scripts/check-collector-config-replica.sh; bash scripts/__tests__/check-collector-config-replica.test.sh >/tmp/replica-test.log 2>&1; git diff --check; cmp -s packages/collectors/config/config.yaml packages/python-api/collector-config/config.yaml
- **Notes:** The script relies on the exit codes of each preceding command to set environment variables (CHECK, TEST, DIFFCLEAN, CMP) for subsequent logging or inspection.

### Check configuration files for specific tooling names
<!-- sig: 9a64b6eefb2c -->

```bash
(ls pyproject.toml setup.cfg .flake8 2>/dev/null; grep -nE 'ruff|flake8|black' pyproject.toml 2>/dev/null)
```

- **What it does:** This command first lists specific configuration files, suppressing errors, and then searches pyproject.toml for lines containing 'ruff', 'flake8', or 'black'.
- **Why:** It quickly verifies the presence of configuration files and checks if the project is configured to use specific static analysis tools.
- **Example:** (ls pyproject.toml setup.cfg .flake8 2>/dev/null; grep -nE 'ruff|flake8|black' pyproject.toml 2>/dev/null)
- **Notes:** The initial `ls` command is wrapped in parentheses and redirects stderr to null to prevent listing errors from cluttering the output.

### Validate edited standards against repository using local model
<!-- sig: 44cd5e3daad0 -->

```bash
check
```

- **What it does:** The `check` binary reads a plain-text profile of the repository and uses a local model to evaluate standards one rule at a time.
- **Why:** This allows developers to verify if a proposed standard rule is applicable to the current codebase without sending data externally.
- **Example:** check after editing standards in the terminal UI and saving them.
- **Notes:** The local model used is determined by the `BLUEPRINT_OLLAMA_MODEL` environment variable, defaulting to `gemma4:latest`. Nothing leaves the local machine during this check.

### Check code against defined standards
<!-- sig: 5ecd3198fd30 -->

```bash
violations 'check-code' prints per 'rule;'
violations 'check-code' --all prints every one
```

- **What it does:** This command checks code against defined standards, reporting violations either per specific rule or listing every single violation found.
- **Why:** It provides granular control over the reporting level, allowing developers to see only specific rule failures or get a complete overview of all issues.
- **Example:** violations 'check-code' prints per 'rule;' on the project repository.
- **Notes:** The `--all` flag ensures every violation is reported, regardless of the specific rule being checked.

### Replace blueprint cache documentation in README
<!-- sig: 034f04601609 -->

```bash
cat > /tmp/edit_readme.py <<'EOF'
p = "README.md"
s = open(p).read()
s = s.replace('''| `blueprint cache [--clear [--only NAMESPACE]]` |''', '''| `blueprint check-code [repo] [--standards FILE] [--all]` | Check the repo's Python code against the standards that name a code check (`check: type-hints`). Lists each violation with file and line. Exit 1 if a rule of severity `error` is broken, 2 if a rule names a check that does not exist. See [Enforcing rules in code](#enforcing-rules-in-code). |`\n`| `blueprint cache [--clear [--only NAMESPACE]]` |''', 1)
old_a = s.index("Limits, so nothing is over`
```

- **What it does:** This sequence uses a here-document to overwrite README.md with modified content, specifically replacing a reference to `blueprint cache` with a reference to `blueprint check-code`.
- **Why:** It updates documentation to reflect the correct command usage for code standard enforcement, replacing an outdated command reference.
- **Example:** cat > /tmp/edit_readme.py <<'EOF' ... (content shown above) ... EOF
- **Notes:** The replacement string is complex due to escaping quotes within the here-document structure.

### Apply a specific rule judgment to a document
<!-- sig: e7b8d9c026bf -->

```bash
Judged rule '(judge:' 'true')'
```

- **What it does:** This syntax instructs the judging mechanism to evaluate the document against a specific rule, setting the judgment to true.
- **Why:** It allows for targeted, automated validation of specific sections or rules within a document during a build or check process.
- **Example:** Judged rule '(judge:' 'true')' within a markdown file.
- **Notes:** This appears to be a custom directive used within a document processing framework, likely related to automated documentation checks.

### Validate code structure against naming conventions
<!-- sig: 51163f0f32a9 -->

```bash
python3 - <<'EOF'
p="tests/test_code_checks.py"; s=open(p).read()
s=s.replace('''    assert set(option_properties()) == {"parameters", "returns", "forbid_any"}
    assert option_properties()["returns"]["type"] == "boolean"
    assert set(CHECKS) == {"type-hints"}''','''    assert set(option_properties()) == {"parameters", "returns", "forbid_any", "functions", "classes", "modules", "public_only", "select", "strict"}
    assert option_properties()["returns"]["type"] == "boolean"
    assert option_properties()["select"]["type"] == "string", "every option is a plain scalar a model can fill in"
```

- **What it does:** This script reads a test file, performs a string replacement on its content, and executes the modified content using the Python interpreter.
- **Why:** It enforces a specific, more comprehensive set of assertions regarding option properties within the test file, likely to improve code quality checks.
- **Example:** python3 - <<'EOF' p="tests/test_code_checks.py"; s=open(p).read() s=s.replace(''' assert set(option_properties()) == {"parameters", "returns", "forbid_any"} assert option_properties()["returns"]["type"] == "boolean" assert set(CHECKS) == {"type-hints"}''',''' assert set(option_properties()) == {"parameters", "returns", "forbid_any", "functions", "classes", "modules", "public_only", "select", "strict"} assert option_properties()["returns"]["type"] == "boolean" assert option_properties()["select"]["type"] == "string", "every option is a plain scalar a model can fill in"" EOF
- **Notes:** The command uses a here-document (<<'EOF') to feed the modified script content directly to python3 for execution.

### Check for removed references in scans
<!-- sig: 64503e5976ab -->

```bash
static removed-reference scans
```

- **What it does:** The static tool checks the codebase for references that have been marked for removal during a scan process.
- **Why:** This ensures that code or dependencies slated for removal are correctly identified and accounted for across the project.
- **Example:** static removed-reference scans on the current repository state.

### Record test results into markdown file
<!-- sig: 531013abcbcb -->

```bash
'**PASS**' '—' '`dashboard-collector-boundary:` all checks 'passed`'
```

- **What it does:** This command outputs a formatted success message indicating that the dashboard-collector-boundary checks passed.
- **Why:** It is used to append the specific test result line into the test.md file within the pipeline documentation.
- **Example:** '**PASS**' '—' '`dashboard-collector-boundary:` all checks 'passed`'
- **Notes:** This snippet is part of a larger 'cat <<' block used to inject structured test results into a markdown file.

### Run static analysis on the codebase
<!-- sig: 82b8677466f4 -->

```bash
ran 'once;' flagged 3 blank-line-at-EOF issues from block deletions '—' '**fixed**;' binary then unavailable in shell for re-check, remaining formatting manually inspected '(block' deletions 'only)'
```

- **What it does:** Executes the 'ran' binary to check for specific formatting issues, such as blank lines at the end of files, after some fixes were applied.
- **Why:** This tool is used to enforce code style and structural consistency across the project files.
- **Example:** ran 'once;' flagged 3 blank-line-at-EOF issues from block deletions '—' '**fixed**;' binary then unavailable in shell for re-check, remaining formatting manually inspected '(block' deletions 'only)'
- **Notes:** The binary is noted as unavailable in the shell for re-checking, requiring manual inspection of remaining formatting issues.

## Comparing files

### Check if two configuration files differ
<!-- sig: c239937316f7 -->
<!-- sig: 749dfeac313d -->
<!-- sig: dd3e06020f7c -->
<!-- sig: 3b1dbe0336e1 -->
<!-- sig: b5ef1cc6b105 -->

```bash
diff -q /tmp/replica.yaml ../ei-rd-eff-collectors/config/config.yaml
```

- **What it does:** Quietly compares the contents of the file /tmp/replica.yaml against the file ../ei-rd-eff-collectors/config/config.yaml.
- **Why:** This is used to quickly determine if a temporary or generated configuration file matches a known good source file without printing the actual differences.
- **Example:** diff -q /tmp/replica.yaml ../ei-rd-eff-collectors/config/config.yaml
- **Notes:** The -q flag suppresses all differences output, returning only a non-zero exit status if the files differ.

### Verify if two files are byte-for-byte identical
<!-- sig: 0e803ebd5bb5 -->
<!-- sig: 57d445f7edc5 -->

```bash
cmp -s collector-dashboard-contract.md /tmp/dash-contract/docs/architecture/collector-dashboard-contract.md
```

- **What it does:** Compares two files byte by byte; the '-s' flag suppresses the standard output, meaning it only returns an exit code indicating success or failure.
- **Why:** This provides a silent, programmatic check to confirm that the contents of the source file match the contents of the destination file exactly.
- **Example:** cmp -s collector-dashboard-contract.md /tmp/dash-contract/docs/architecture/collector-dashboard-contract.md
- **Notes:** The command succeeds (exit code 0) if the files are identical, and fails (non-zero exit code) if any byte differs.

### Find files that diverged between two branches
<!-- sig: 411e83e4e563 -->
<!-- sig: 0f5f92525a12 -->

```bash
B=$(git merge-base origin/staging upstream/staging);
echo 'merge-base: $(git rev-parse --short $B);'
comm -12 '<(git diff --name-only '$B' upstream/staging' <(git diff --name-only '$B' origin/staging))'
```

- **What it does:** Determines the common ancestor commit between two branches, then lists files that have changed differently on either branch since that common point.
- **Why:** This sequence isolates files that have been modified independently on both the upstream/staging and origin/staging branches since they last shared a common commit.
- **Example:** Running this after fetching remote changes to see what files are unique to each branch's history.
- **Notes:** The command relies on `git merge-base` to find the common ancestor commit hash, which is then used as a reference point for `git diff`.

### Find files unique to the upstream staging branch
<!-- sig: 63746fa50621 -->

```bash
sort) '<(git diff --name-only $B origin/staging
```

- **What it does:** This command uses process substitution to feed the list of files changed between the merge-base ($B) and the origin/staging branch into the sort utility.
- **Why:** It isolates the file names that are present in the diff against origin/staging but not in the upstream/staging diff, which is necessary for calculating overlaps.
- **Example:** sort) '<(git diff --name-only $B origin/staging on a file list derived from a merge-base calculation.
- **Notes:** The syntax uses process substitution (<(...)) which is a bash feature. The variable $B must be set to the common ancestor commit hash beforehand.

## Branching

### Switch to a specific feature branch
<!-- sig: 39fb17700f0e -->
<!-- sig: 6764e0c11f50 -->
<!-- sig: b4eb8f84a821 -->
<!-- sig: b72ab7caa8f4 -->
<!-- sig: 953bec6d1724 -->
<!-- sig: 07ffff3dc282 -->
<!-- sig: b269d8c5161b -->
<!-- sig: 240334766ad5 -->
<!-- sig: 3bf911364e66 -->
<!-- sig: b8322b7ec341 -->
<!-- sig: 36aedbc5454a -->
<!-- sig: ac52f14a9e80 -->
<!-- sig: 29806af047be -->
<!-- sig: 8de4e63cd3a4 -->
<!-- sig: 1efb35a29a53 -->
<!-- sig: ac53c284d44e -->
<!-- sig: 624634b76c8b -->
<!-- sig: e12f0b112596 -->
<!-- sig: 452d68528fb0 -->
<!-- sig: bec44f843438 -->
<!-- sig: 03eae0bdd9cc -->
<!-- sig: 196adfb54274 -->

```bash
set -e;
f=packages/frontend/src/services/__tests__/python-api.test.ts;
OLD=$(git rev-parse feat/remove-dead-kpis-path-4546812);
git switch -q feat/remove-dead-kpis-path-4546812
```

- **What it does:** This sequence sets error checking, defines a file variable, captures the current commit SHA, and then switches to the specified feature branch quietly.
- **Why:** It ensures that the subsequent operations happen only if the previous steps succeeded, and it prepares the environment by moving to the correct branch state.
- **Example:** set -e; f=packages/frontend/src/services/__tests__/python-api.test.ts; OLD=$(git rev-parse feat/remove-dead-kpis-path-4546812); git switch -q feat/remove-dead-kpis-path-4546812
- **Notes:** The `set -e` ensures the script exits immediately if any command fails. The variable `OLD` stores the SHA of the branch you are leaving.

## Images and media

### Convert a specific page range from a PDF to PNG images
<!-- sig: f9316ec7e13f -->
<!-- sig: d4be5159c0e7 -->

```bash
pdftoppm -png -r 50 -f 1 -l 1 pdf/known-issues-summary-2026-09-28.pdf /tmp/pdfthumb2/ki
```

- **What it does:** This command converts a specified page range from a PDF file into a series of PNG images. It uses a resolution of 50 DPI and targets only the first page.
- **Why:** It allows for the programmatic extraction of visual content from a PDF document for further image processing or inspection.
- **Example:** pdftoppm -png -r 50 -f 1 -l 1 pdf/known-issues-summary-2026-09-28.pdf /tmp/pdfthumb2/ki
- **Notes:** The output files will be named based on the input PDF name and the specified output directory structure.

## Binary

### Display the contents of a file in octal format
<!-- sig: 00d73133c243 -->

```bash
od -c
```

- **What it does:** The `od` command reads binary data and displays it in various formats, using the `-c` flag to show it in character representation.
- **Why:** It provides a detailed, human-readable view of raw binary data that standard tools might misinterpret or abstract away.
- **Example:** od -c <some_binary_file>
- **Notes:** This command is often piped into other tools like `head` to limit the output size for inspection.

### Capture a screenshot of a local HTML file
<!-- sig: 344d51b2be31 -->

```bash
if '[' -x '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' '];' then '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --headless --disable-gpu --hide-scrollbars --window-size=1600,1200 --screenshot=/tmp/concept-c.png file:///Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/UI%20mockups/concept-c-executive-insight.html '>/tmp/concept-c-chrome.log' '2>&1'
```

- **What it does:** This script checks if Google Chrome is executable, and if so, runs it in headless mode to render and capture a screenshot of a specified local HTML file.
- **Why:** It allows automated visual testing or documentation generation of web content without opening a visible browser window.
- **Example:** if '[' -x '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' '];' then '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --headless --disable-gpu --hide-scrollbars --window-size=1600,1200 --screenshot=/tmp/concept-c.png file:///Users/sraj/git_apps/epam/Work/PHUS-INN/devin-session-notes/UI%20mockups/concept-c-executive-insight.html '>/tmp/concept-c-chrome.log' '2>&1'
- **Notes:** The command redirects both standard output and standard error to /tmp/concept-c-chrome.log. The initial 'if' statement ensures the Chrome binary exists before execution.
## Viewing history

### View the last twenty commits in a readable format
<!-- sig: 48b676a6a96f -->
<!-- sig: 31fded609e41 -->

```bash
set 'GIT_NO_DEVTRACK=1&&' git log --oneline '-20&&' type README.md
```

- **What it does:** This command first sets an environment variable, then runs git log to display the last 20 commits on a single line, and finally types the content of README.md.
- **Why:** It combines viewing recent commit history with immediately displaying the contents of a key documentation file in one sequence.
- **Example:** set 'GIT_NO_DEVTRACK=1&&' git log --oneline '-20&&' type README.md to check recent changes and documentation simultaneously.
- **Notes:** The use of '&&' ensures the subsequent command only runs if the preceding one succeeds. The 'set' command is used here to conditionally set an environment variable for the git operation.

## Network inspection

### List processes listening on a specific port
<!-- sig: ebf9f087c112 -->
<!-- sig: 088be0b68957 -->
<!-- sig: 1f53457bd780 -->
<!-- sig: 28324e911510 -->
<!-- sig: ae8c1a3e59a5 -->

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

- **What it does:** Lists open files and network connections using lsof, specifically filtering for TCP connections listening on port 8000 and showing process IDs numerically.
- **Why:** This provides a direct, process-centric view of which application is occupying a specific network port, which is more detailed than netstat.
- **Example:** lsof -nP -iTCP:8000 -sTCP:LISTEN to check which process is using port 8000.
- **Notes:** The command failed because lsof requires root privileges (sudo) to see all processes' open files and network sockets.

## Process monitoring

### Check if a specific process is currently running
<!-- sig: 12600199bfc5 -->
<!-- sig: b0e4af03f137 -->

```bash
date '+%T;'
pgrep -f 'm main' '>/dev/null'
```

- **What it does:** The first part prints the current time, and the second part searches for processes containing 'm main' in their full command line, suppressing any output.
- **Why:** This pattern is used to timestamp the check and then conditionally execute subsequent commands based on the exit status of pgrep.
- **Example:** date '+%T;' pgrep -f 'm main' '>/dev/null' to see the time and confirm the process status.
- **Notes:** The use of '>/dev/null' redirects standard output, ensuring the command runs silently unless an error occurs.

## Process management

### Gracefully terminate a specific process
<!-- sig: 765f7a6fbd4b -->
<!-- sig: 786e5925b544 -->
<!-- sig: 94a4ab5d1928 -->

```bash
kill -TERM 21665
```

- **What it does:** Sends the TERM signal to the process ID 21665, requesting it to shut down cleanly.
- **Why:** Using TERM allows the process to catch the signal and perform necessary cleanup, unlike SIGKILL which forces an immediate termination.
- **Example:** kill -TERM 21665 to stop a background worker process gracefully.
- **Notes:** The process must be running for this command to affect it. If the process ignores SIGTERM, you may need to use SIGKILL (-9).
