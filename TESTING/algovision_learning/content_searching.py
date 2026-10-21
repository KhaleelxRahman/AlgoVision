"""English + Hinglish learning content for the searching algorithms.

Hinglish = Hindi written in Roman script, mixed with common English tech terms.
Every ``lines`` key must match a ``# @id`` tag in ``searching.py`` (tests enforce
this in both directions).
"""

from __future__ import annotations

_VALIDATE_SORTED_EN = (
    "Validate the input. The sorted-order check is one O(n) pass that runs before the "
    "search itself; pass validate_sorted=False to skip it."
)
_VALIDATE_SORTED_HI = (
    "Input validate karo. Sorted-order check ek O(n) pass hai jo search se pehle chalta "
    "hai; ise skip karne ke liye validate_sorted=False do."
)

CONTENT = {
    "linear-search": {
        "summary": {
            "en": (
                "Linear search checks the elements one by one from the start until it "
                "finds the target or reaches the end. It works on unsorted data."
            ),
            "hinglish": (
                "Linear search shuru se ek-ek element check karta hai jab tak target mil "
                "na jaaye ya list khatam na ho jaaye. Yeh unsorted data par bhi kaam karta hai."
            ),
        },
        "when_to_use": {
            "en": [
                "Unsorted data, where no faster general method exists.",
                "Very small lists, or when you search only once.",
            ],
            "hinglish": [
                "Unsorted data ke liye, jahan koi aur tez general method nahi hai.",
                "Bahut chhote lists ke liye, ya jab sirf ek baar search karna ho.",
            ],
        },
        "how_it_works": {
            "en": [
                "Start at index 0.",
                "Compare the current element with the target.",
                "If they match, return the index immediately.",
                "If the end is reached without a match, return -1.",
            ],
            "hinglish": [
                "Index 0 se shuru karo.",
                "Maujooda element ko target se compare karo.",
                "Agar match ho jaaye to turant index return karo.",
                "Agar match ke bina list khatam ho jaaye to -1 return karo.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best case O(1): the target is the first element. Average and worst "
                    "case O(n): the target is somewhere in the middle, last, or missing."
                ),
                "space": "O(1) extra space.",
            },
            "hinglish": {
                "time": (
                    "Best case O(1): target pehla element hai. Average aur worst case "
                    "O(n): target beech mein, aakhir mein, ya list mein hai hi nahi."
                ),
                "space": "O(1) extra space.",
            },
        },
        "lines": {
            "linear.init": {
                "en": "Validate the list and the target. No sorting is required.",
                "hinglish": "List aur target validate karo. Sorting ki zaroorat nahi hai.",
            },
            "linear.loop": {
                "en": "Visit each index from left to right.",
                "hinglish": "Left se right har index ko visit karo.",
            },
            "linear.compare": {
                "en": "Does this element equal the target?",
                "hinglish": "Kya yeh element target ke barabar hai?",
            },
            "linear.found": {
                "en": "Match found: return its index. With duplicates this is the first occurrence.",
                "hinglish": "Match mil gaya: uska index return karo. Duplicates hone par yeh pehli occurrence hoti hai.",
            },
            "linear.not_found": {
                "en": "Every element was checked and none matched: return -1.",
                "hinglish": "Har element check ho gaya aur koi match nahi mila: -1 return karo.",
            },
        },
    },
    "binary-search": {
        "summary": {
            "en": (
                "Binary search needs sorted data. It looks at the middle element and "
                "discards half of the remaining range each step."
            ),
            "hinglish": (
                "Binary search ko sorted data chahiye. Yeh beech ka element dekhta hai "
                "aur har step mein bachi hui range ka aadha hissa hata deta hai."
            ),
        },
        "when_to_use": {
            "en": [
                "Large sorted lists that are searched many times.",
                "Whenever random access by index is cheap.",
            ],
            "hinglish": [
                "Bade sorted lists jinhe baar-baar search karna ho.",
                "Jab index se random access sasta ho.",
            ],
        },
        "how_it_works": {
            "en": [
                "Keep a range [low, high] that could contain the target.",
                "Look at the middle element.",
                "If it equals the target, return its index.",
                "If it is smaller than the target, search the right half; otherwise the left half.",
                "If the range becomes empty, return -1.",
            ],
            "hinglish": [
                "Ek range [low, high] rakho jismein target ho sakta hai.",
                "Beech ka element dekho.",
                "Agar woh target ke barabar hai to uska index return karo.",
                "Agar woh target se chhota hai to right half mein dhoondo, warna left half mein.",
                "Agar range khaali ho jaaye to -1 return karo.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best case O(1): the first middle element matches. Average and worst "
                    "case O(log n): the range halves every step. Requires sorted input; "
                    "the optional validation pass is O(n)."
                ),
                "space": "O(1) extra space: this version is iterative.",
            },
            "hinglish": {
                "time": (
                    "Best case O(1): pehla middle element hi match ho jaaye. Average aur "
                    "worst case O(log n): har step mein range aadhi ho jaati hai. Sorted "
                    "input zaroori hai; optional validation pass O(n) ka hai."
                ),
                "space": "O(1) extra space: yeh version iterative hai.",
            },
        },
        "lines": {
            "binary.init": {"en": _VALIDATE_SORTED_EN, "hinglish": _VALIDATE_SORTED_HI},
            "binary.set_low": {
                "en": "low is the first index of the range still to search.",
                "hinglish": "low us range ka pehla index hai jise abhi search karna hai.",
            },
            "binary.set_high": {
                "en": "high is the last index of the range. For an empty list this is -1.",
                "hinglish": "high us range ka aakhri index hai. Khaali list ke liye yeh -1 hota hai.",
            },
            "binary.loop": {
                "en": "Repeat while the range [low, high] is not empty.",
                "hinglish": "Jab tak range [low, high] khaali nahi hai, repeat karo.",
            },
            "binary.mid": {
                "en": "Pick the middle index of the range.",
                "hinglish": "Range ka beech wala index chuno.",
            },
            "binary.compare_equal": {
                "en": "Is the middle element the target?",
                "hinglish": "Kya beech ka element hi target hai?",
            },
            "binary.found": {
                "en": "Found it: return the index (with duplicates, any matching index may be returned).",
                "hinglish": "Mil gaya: index return karo (duplicates mein koi bhi matching index return ho sakta hai).",
            },
            "binary.compare_less": {
                "en": "Is the middle element smaller than the target?",
                "hinglish": "Kya beech ka element target se chhota hai?",
            },
            "binary.go_right": {
                "en": "Yes: the target can only be to the right, so discard the left half including mid.",
                "hinglish": "Haan: target sirf right mein ho sakta hai, isliye mid samet left half hata do.",
            },
            "binary.else_branch": {
                "en": "Otherwise the middle element is larger than the target.",
                "hinglish": "Warna beech ka element target se bada hai.",
            },
            "binary.go_left": {
                "en": "The target can only be to the left, so discard the right half including mid.",
                "hinglish": "Target sirf left mein ho sakta hai, isliye mid samet right half hata do.",
            },
            "binary.not_found": {
                "en": "The range is empty and nothing matched: return -1.",
                "hinglish": "Range khaali ho gayi aur kuch match nahi hua: -1 return karo.",
            },
        },
    },
    "jump-search": {
        "summary": {
            "en": (
                "Jump search needs sorted data. It jumps ahead in blocks of about "
                "sqrt(n) elements to find the block that could hold the target, then "
                "scans that block linearly."
            ),
            "hinglish": (
                "Jump search ko sorted data chahiye. Yeh lagbhag sqrt(n) elements ke "
                "blocks mein aage koodta hai taaki woh block mile jismein target ho sakta "
                "hai, phir us block ko linearly scan karta hai."
            ),
        },
        "when_to_use": {
            "en": [
                "Sorted data where jumping forward is cheap but stepping backwards a long way is costly.",
                "As a simple middle ground between linear and binary search.",
            ],
            "hinglish": [
                "Sorted data jahan aage koodna sasta ho par bahut peeche jaana mehenga ho.",
                "Linear aur binary search ke beech ke simple vikalp ke roop mein.",
            ],
        },
        "how_it_works": {
            "en": [
                "Choose a block size of about sqrt(n).",
                "Jump block by block while the last element of the block is smaller than the target.",
                "Now the target can only be inside the current block.",
                "Scan that block linearly; return the index or -1.",
            ],
            "hinglish": [
                "Lagbhag sqrt(n) ka block size chuno.",
                "Jab tak block ka aakhri element target se chhota hai, block-block aage koodo.",
                "Ab target sirf maujooda block ke andar ho sakta hai.",
                "Us block ko linearly scan karo; index ya -1 return karo.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best case O(1): the target is the first element of the first block. "
                    "Average and worst case O(sqrt(n)): about sqrt(n) jumps plus up to "
                    "sqrt(n) steps in one block. Requires sorted input."
                ),
                "space": "O(1) extra space.",
            },
            "hinglish": {
                "time": (
                    "Best case O(1): target pehle block ka pehla element hai. Average aur "
                    "worst case O(sqrt(n)): lagbhag sqrt(n) jumps aur ek block mein "
                    "zyada se zyada sqrt(n) steps. Sorted input zaroori hai."
                ),
                "space": "O(1) extra space.",
            },
        },
        "lines": {
            "jump.init": {"en": _VALIDATE_SORTED_EN, "hinglish": _VALIDATE_SORTED_HI},
            "jump.length": {
                "en": "Remember how many elements there are.",
                "hinglish": "Yaad rakho ki kitne elements hain.",
            },
            "jump.block_size": {
                "en": "Block size is the integer square root of n, which balances the number of jumps against the scan length.",
                "hinglish": "Block size n ka integer square root hai, jisse jumps aur scan ki lambai ka santulan bana rehta hai.",
            },
            "jump.prev": {
                "en": "prev is where the current block starts.",
                "hinglish": "prev woh jagah hai jahan maujooda block shuru hota hai.",
            },
            "jump.curr": {
                "en": "curr is where the next block starts (one past the end of the current block).",
                "hinglish": "curr woh jagah hai jahan agla block shuru hota hai (maujooda block ke end ke ek aage).",
            },
            "jump.jump_loop": {
                "en": "If the last element of the current block is still smaller than the target, the target is not in this block.",
                "hinglish": "Agar maujooda block ka aakhri element abhi bhi target se chhota hai, to target is block mein nahi hai.",
            },
            "jump.advance_prev": {
                "en": "Move the block start to the next block.",
                "hinglish": "Block ka start agle block par le jao.",
            },
            "jump.advance_curr": {
                "en": "Move the block end forward by one block size.",
                "hinglish": "Block ka end ek block size aage badhao.",
            },
            "jump.scan": {
                "en": "Scan the candidate block linearly (the last block may be shorter).",
                "hinglish": "Candidate block ko linearly scan karo (aakhri block chhota ho sakta hai).",
            },
            "jump.compare": {
                "en": "Does this element equal the target?",
                "hinglish": "Kya yeh element target ke barabar hai?",
            },
            "jump.found": {
                "en": "Found it: return the index.",
                "hinglish": "Mil gaya: index return karo.",
            },
            "jump.not_found": {
                "en": "The candidate block did not contain the target (or we jumped past the end): return -1.",
                "hinglish": "Candidate block mein target nahi mila (ya hum end ke aage nikal gaye): -1 return karo.",
            },
        },
    },
    "interpolation-search": {
        "summary": {
            "en": (
                "Interpolation search needs sorted data. Instead of always probing the "
                "middle, it estimates where the target should be from its value, like "
                "looking near the end of a dictionary for 'zebra'."
            ),
            "hinglish": (
                "Interpolation search ko sorted data chahiye. Yeh hamesha beech ko dekhne "
                "ki jagah target ki value se andaza lagata hai ki woh kahan hona chahiye, "
                "jaise dictionary mein 'zebra' ke liye end ke paas dekhna."
            ),
        },
        "when_to_use": {
            "en": [
                "Sorted data with values spread fairly evenly (for example ids or timestamps).",
                "Not suitable for heavily skewed values, where it can degrade to O(n).",
            ],
            "hinglish": [
                "Sorted data jiske values lagbhag barabar failay hon (jaise ids ya timestamps).",
                "Bahut skewed values ke liye theek nahi, wahan yeh O(n) tak gir sakta hai.",
            ],
        },
        "how_it_works": {
            "en": [
                "Only continue while the target lies between the values at low and high.",
                "Estimate the position by proportion: how far the target is between the two end values.",
                "Compare the probed element with the target.",
                "Shrink the range to the right or left of the probe and repeat.",
            ],
            "hinglish": [
                "Tab tak aage badho jab tak target low aur high ke values ke beech mein hai.",
                "Anupaat se position ka andaza lagao: target dono end values ke beech kitna aage hai.",
                "Probe kiye gaye element ko target se compare karo.",
                "Range ko probe ke right ya left tak chhota karo aur repeat karo.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best case O(1): the first probe hits. Average case O(log log n) "
                    "assumes sorted data with roughly uniformly distributed values. "
                    "Worst case O(n) for skewed data. Requires sorted input."
                ),
                "space": "O(1) extra space.",
            },
            "hinglish": {
                "time": (
                    "Best case O(1): pehla probe hi sahi lage. Average case O(log log n) "
                    "tab maana jaata hai jab data sorted ho aur values lagbhag uniform "
                    "failay hon. Skewed data mein worst case O(n). Sorted input zaroori hai."
                ),
                "space": "O(1) extra space.",
            },
        },
        "lines": {
            "interpolation.init": {"en": _VALIDATE_SORTED_EN, "hinglish": _VALIDATE_SORTED_HI},
            "interpolation.set_low": {
                "en": "low is the first index of the range still to search.",
                "hinglish": "low us range ka pehla index hai jise abhi search karna hai.",
            },
            "interpolation.set_high": {
                "en": "high is the last index of the range. For an empty list this is -1.",
                "hinglish": "high us range ka aakhri index hai. Khaali list ke liye yeh -1 hota hai.",
            },
            "interpolation.loop": {
                "en": "Continue only while the target lies between arr[low] and arr[high]; outside that span it cannot be present (this also makes an empty range safe).",
                "hinglish": "Tab tak chalo jab tak target arr[low] aur arr[high] ke beech mein hai; us span ke bahar woh ho hi nahi sakta (isse khaali range bhi safe rehti hai).",
            },
            "interpolation.flat_check": {
                "en": "If both ends have the same value the formula would divide by zero.",
                "hinglish": "Agar dono end ka value same hai to formula zero se divide karega.",
            },
            "interpolation.flat_found": {
                "en": "The loop condition already guarantees the target equals that value, so low is a match.",
                "hinglish": "Loop condition pehle se guarantee karti hai ki target usi value ke barabar hai, isliye low match hai.",
            },
            "interpolation.estimate": {
                "en": "Estimate the index: start at low and move forward by the fraction (target - arr[low]) / (arr[high] - arr[low]) of the range width.",
                "hinglish": "Index ka andaza lagao: low se shuru karo aur range ki chaudai ka fraction (target - arr[low]) / (arr[high] - arr[low]) aage badho.",
            },
            "interpolation.compare_equal": {
                "en": "Is the probed element the target?",
                "hinglish": "Kya probe kiya gaya element target hai?",
            },
            "interpolation.found": {
                "en": "Found it: return the index.",
                "hinglish": "Mil gaya: index return karo.",
            },
            "interpolation.compare_less": {
                "en": "Is the probed element smaller than the target?",
                "hinglish": "Kya probe kiya gaya element target se chhota hai?",
            },
            "interpolation.go_right": {
                "en": "Yes: continue to the right of the probe.",
                "hinglish": "Haan: probe ke right mein aage badho.",
            },
            "interpolation.else_branch": {
                "en": "Otherwise the probed element is larger than the target.",
                "hinglish": "Warna probe kiya gaya element target se bada hai.",
            },
            "interpolation.go_left": {
                "en": "Continue to the left of the probe.",
                "hinglish": "Probe ke left mein aage badho.",
            },
            "interpolation.not_found": {
                "en": "The target is outside the remaining range or the range is empty: return -1.",
                "hinglish": "Target bachi hui range ke bahar hai ya range khaali hai: -1 return karo.",
            },
        },
    },
    "exponential-search": {
        "summary": {
            "en": (
                "Exponential search needs sorted data. It doubles an upper bound "
                "(1, 2, 4, 8, ...) until it passes the target, then runs binary "
                "search inside that bounded range."
            ),
            "hinglish": (
                "Exponential search ko sorted data chahiye. Yeh ek upper bound ko double "
                "karta jaata hai (1, 2, 4, 8, ...) jab tak woh target ko paar na kar le, "
                "phir us bounded range ke andar binary search chalata hai."
            ),
        },
        "when_to_use": {
            "en": [
                "Sorted data when the target is likely near the beginning.",
                "Very large or unbounded sorted sequences, where the end is not known up front.",
            ],
            "hinglish": [
                "Sorted data jab target ke shuru ke paas hone ki sambhavna ho.",
                "Bahut bade ya unbounded sorted sequences jahan end pehle se pata nahi hota.",
            ],
        },
        "how_it_works": {
            "en": [
                "If the list is empty return -1; if the first element matches return 0.",
                "Double the bound while it is inside the list and its element is not larger than the target.",
                "The target must now lie between bound / 2 and the bound (limited to the last index).",
                "Run binary search in that range.",
            ],
            "hinglish": [
                "Agar list khaali hai to -1 return karo; agar pehla element match kare to 0 return karo.",
                "Jab tak bound list ke andar hai aur uska element target se bada nahi hai, bound ko double karo.",
                "Ab target bound / 2 aur bound ke beech hona chahiye (last index tak seemit).",
                "Us range mein binary search chalao.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best case O(1): the target is the first element. Average and worst "
                    "case O(log n): about log2(i) doublings plus a binary search over "
                    "about i elements, where i is the target's index. Requires sorted input."
                ),
                "space": "O(1) extra space: both phases are iterative.",
            },
            "hinglish": {
                "time": (
                    "Best case O(1): target pehla element hai. Average aur worst case "
                    "O(log n): lagbhag log2(i) baar double karna aur lagbhag i elements "
                    "par binary search, jahan i target ka index hai. Sorted input zaroori hai."
                ),
                "space": "O(1) extra space: dono phases iterative hain.",
            },
        },
        "lines": {
            "exponential.init": {"en": _VALIDATE_SORTED_EN, "hinglish": _VALIDATE_SORTED_HI},
            "exponential.length": {
                "en": "Remember how many elements there are.",
                "hinglish": "Yaad rakho ki kitne elements hain.",
            },
            "exponential.empty_check": {
                "en": "An empty list cannot contain the target.",
                "hinglish": "Khaali list mein target ho hi nahi sakta.",
            },
            "exponential.empty_return": {
                "en": "Return -1 straight away.",
                "hinglish": "Seedha -1 return karo.",
            },
            "exponential.check_first": {
                "en": "Check index 0 first; the doubling phase starts at index 1.",
                "hinglish": "Pehle index 0 check karo; doubling phase index 1 se shuru hota hai.",
            },
            "exponential.first_found": {
                "en": "The first element matched: return 0 (the O(1) best case).",
                "hinglish": "Pehla element match ho gaya: 0 return karo (O(1) best case).",
            },
            "exponential.bound_init": {
                "en": "Start the upper bound at index 1.",
                "hinglish": "Upper bound ko index 1 se shuru karo.",
            },
            "exponential.grow_loop": {
                "en": "Keep doubling while the bound is inside the list and its value is not above the target.",
                "hinglish": "Jab tak bound list ke andar hai aur uski value target se upar nahi hai, double karte raho.",
            },
            "exponential.double": {
                "en": "Double the bound: 1, 2, 4, 8, ...",
                "hinglish": "Bound ko double karo: 1, 2, 4, 8, ...",
            },
            "exponential.range_low": {
                "en": "The previous bound (bound / 2) held a value not above the target, so the search range starts there.",
                "hinglish": "Pichhla bound (bound / 2) target se upar nahi tha, isliye search range wahin se shuru hoti hai.",
            },
            "exponential.range_high": {
                "en": "The range ends at the bound, but never beyond the last index.",
                "hinglish": "Range bound par khatam hoti hai, par last index se aage kabhi nahi.",
            },
            "exponential.bsearch_loop": {
                "en": "Binary search phase: repeat while the range is not empty.",
                "hinglish": "Binary search phase: jab tak range khaali nahi hai, repeat karo.",
            },
            "exponential.mid": {
                "en": "Pick the middle index of the range.",
                "hinglish": "Range ka beech wala index chuno.",
            },
            "exponential.compare_equal": {
                "en": "Is the middle element the target?",
                "hinglish": "Kya beech ka element hi target hai?",
            },
            "exponential.found": {
                "en": "Found it: return the index.",
                "hinglish": "Mil gaya: index return karo.",
            },
            "exponential.compare_less": {
                "en": "Is the middle element smaller than the target?",
                "hinglish": "Kya beech ka element target se chhota hai?",
            },
            "exponential.go_right": {
                "en": "Yes: discard the left half including mid.",
                "hinglish": "Haan: mid samet left half hata do.",
            },
            "exponential.else_branch": {
                "en": "Otherwise the middle element is larger than the target.",
                "hinglish": "Warna beech ka element target se bada hai.",
            },
            "exponential.go_left": {
                "en": "Discard the right half including mid.",
                "hinglish": "Mid samet right half hata do.",
            },
            "exponential.not_found": {
                "en": "The range is empty and nothing matched: return -1.",
                "hinglish": "Range khaali ho gayi aur kuch match nahi hua: -1 return karo.",
            },
        },
    },
}
