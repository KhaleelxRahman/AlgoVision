"""English + Hinglish learning content for the sorting algorithms.

Hinglish = Hindi written in Roman script, mixed with common English tech terms.
Every ``lines`` key must match a ``# @id`` tag in ``sorting.py`` (tests enforce
this in both directions).
"""

from __future__ import annotations

CONTENT = {
    "bubble-sort": {
        "summary": {
            "en": (
                "Bubble sort repeatedly compares neighbouring elements and swaps them "
                "when they are in the wrong order. After each pass the largest "
                "remaining value 'bubbles up' to its final position at the end."
            ),
            "hinglish": (
                "Bubble sort baar-baar paas-paas ke elements ko compare karta hai aur "
                "galat order mein hone par swap kar deta hai. Har pass ke baad bacha "
                "hua sabse bada value bubble ki tarah upar uth kar end mein apni sahi "
                "jagah le leta hai."
            ),
        },
        "when_to_use": {
            "en": [
                "Teaching: it is the simplest sort to visualise.",
                "Tiny or almost-sorted lists, thanks to the early-exit check.",
            ],
            "hinglish": [
                "Padhai ke liye: ise visualise karna sabse aasaan hai.",
                "Chhote ya lagbhag sorted lists ke liye, kyunki early-exit check hota hai.",
            ],
        },
        "how_it_works": {
            "en": [
                "Walk through the list comparing each pair of neighbours.",
                "Swap a pair if the left value is bigger than the right value.",
                "After one full pass the largest unsorted value sits at the end.",
                "Repeat on the shorter unsorted part until a pass makes no swaps.",
            ],
            "hinglish": [
                "List mein aage badho aur har paas-paas ki jodi ko compare karo.",
                "Agar left value right se badi hai to dono ko swap karo.",
                "Ek poore pass ke baad sabse bada unsorted value end mein pahunch jaata hai.",
                "Chhote hote unsorted hisse par tab tak repeat karo jab tak ek pass mein koi swap na ho.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best case O(n): on already sorted data one pass finds no swaps and "
                    "stops. Average and worst case O(n²): about n²/2 comparisons."
                ),
                "space": "O(1) extra space: only a few index variables and a flag.",
            },
            "hinglish": {
                "time": (
                    "Best case O(n): pehle se sorted data mein ek pass mein koi swap nahi "
                    "hota aur algorithm ruk jaata hai. Average aur worst case O(n²): "
                    "lagbhag n²/2 comparisons."
                ),
                "space": "O(1) extra space: sirf kuch index variables aur ek flag.",
            },
        },
        "lines": {
            "bubble.init": {
                "en": "Validate the input and make a working copy so the original list is never changed.",
                "hinglish": "Input validate karo aur ek copy banao taaki original list kabhi change na ho.",
            },
            "bubble.length": {
                "en": "Remember how many elements there are.",
                "hinglish": "Yaad rakho ki kitne elements hain.",
            },
            "bubble.outer_loop": {
                "en": "Each pass handles a shorter range: 'end' is the last index that is still unsorted.",
                "hinglish": "Har pass mein range chhoti hoti jaati hai: 'end' woh last index hai jo abhi unsorted hai.",
            },
            "bubble.reset_flag": {
                "en": "Assume this pass will make no swaps.",
                "hinglish": "Maan lo ki is pass mein koi swap nahi hoga.",
            },
            "bubble.inner_loop": {
                "en": "Visit every neighbouring pair (j, j + 1) in the unsorted range.",
                "hinglish": "Unsorted range ki har paas-paas wali jodi (j, j + 1) ko visit karo.",
            },
            "bubble.compare": {
                "en": "Compare the pair. Using '>' (not '>=') keeps equal values in their original order, so the sort is stable.",
                "hinglish": "Jodi ko compare karo. '>=' ki jagah '>' use karne se barabar values ka order same rehta hai, isliye sort stable hai.",
            },
            "bubble.swap": {
                "en": "Left value is bigger, so swap the two values.",
                "hinglish": "Left value badi hai, isliye dono values ko swap karo.",
            },
            "bubble.mark_swapped": {
                "en": "Record that a swap happened, so another pass is needed.",
                "hinglish": "Note karo ki swap hua, matlab ek aur pass chahiye.",
            },
            "bubble.check_swapped": {
                "en": "After the pass, check whether any swap happened.",
                "hinglish": "Pass ke baad check karo ki koi swap hua ya nahi.",
            },
            "bubble.early_exit": {
                "en": "No swaps means the list is already sorted, so stop early. This gives the O(n) best case.",
                "hinglish": "Koi swap nahi hua matlab list sorted hai, isliye jaldi ruk jao. Isi se O(n) best case milta hai.",
            },
            "bubble.return": {
                "en": "Return the sorted copy.",
                "hinglish": "Sorted copy return karo.",
            },
        },
    },
    "selection-sort": {
        "summary": {
            "en": (
                "Selection sort repeatedly finds the smallest value in the unsorted "
                "part and swaps it into the next position of the sorted part."
            ),
            "hinglish": (
                "Selection sort unsorted hisse mein se sabse chhota value dhoondta hai "
                "aur use sorted hisse ki agli position par swap kar deta hai."
            ),
        },
        "when_to_use": {
            "en": [
                "When writes are expensive: it makes at most n - 1 swaps.",
                "Teaching the idea of a growing sorted prefix.",
            ],
            "hinglish": [
                "Jab write karna mehenga ho: ismein zyada se zyada n - 1 swaps hote hain.",
                "Badhte hue sorted prefix ka concept samjhane ke liye.",
            ],
        },
        "how_it_works": {
            "en": [
                "Treat the start of the list as the sorted part (initially empty).",
                "Scan the unsorted part to find the index of its smallest value.",
                "Swap that smallest value into the first unsorted position.",
                "Grow the sorted part by one and repeat.",
            ],
            "hinglish": [
                "List ke shuru ko sorted hissa maano (pehle yeh khaali hai).",
                "Unsorted hisse ko scan karke sabse chhote value ka index dhoondo.",
                "Us sabse chhote value ko pehli unsorted position par swap karo.",
                "Sorted hisse ko ek se badhao aur repeat karo.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "O(n²) in every case: it always scans the whole unsorted part, even "
                    "if the data is already sorted."
                ),
                "space": "O(1) extra space: only index variables.",
            },
            "hinglish": {
                "time": (
                    "Har case mein O(n²): yeh hamesha poora unsorted hissa scan karta hai, "
                    "chahe data pehle se sorted ho."
                ),
                "space": "O(1) extra space: sirf index variables.",
            },
        },
        "lines": {
            "selection.init": {
                "en": "Validate the input and make a working copy so the original list is never changed.",
                "hinglish": "Input validate karo aur ek copy banao taaki original list kabhi change na ho.",
            },
            "selection.length": {
                "en": "Remember how many elements there are.",
                "hinglish": "Yaad rakho ki kitne elements hain.",
            },
            "selection.outer_loop": {
                "en": "Position i is the next slot of the sorted prefix. The last element is automatically correct, so stop at n - 2.",
                "hinglish": "Position i sorted prefix ki agli jagah hai. Last element apne aap sahi ho jaata hai, isliye n - 2 par ruk jaate hain.",
            },
            "selection.assume_min": {
                "en": "Assume the value at i is the smallest for now.",
                "hinglish": "Abhi ke liye maan lo ki i par jo value hai wahi sabse chhota hai.",
            },
            "selection.inner_loop": {
                "en": "Scan the rest of the unsorted part.",
                "hinglish": "Unsorted hisse ke baaki elements scan karo.",
            },
            "selection.compare": {
                "en": "Is this value smaller than the smallest found so far?",
                "hinglish": "Kya yeh value ab tak ke sabse chhote value se chhota hai?",
            },
            "selection.update_min": {
                "en": "Yes, remember this index as the new minimum.",
                "hinglish": "Haan, is index ko naye minimum ki tarah yaad rakho.",
            },
            "selection.check_swap": {
                "en": "Only swap when the minimum is not already in place.",
                "hinglish": "Swap tabhi karo jab minimum pehle se sahi jagah par na ho.",
            },
            "selection.swap": {
                "en": "Swap the minimum into position i. This long-distance swap is why selection sort is not stable.",
                "hinglish": "Minimum ko position i par swap karo. Yeh door ka swap hi wajah hai ki selection sort stable nahi hai.",
            },
            "selection.return": {
                "en": "Return the sorted copy.",
                "hinglish": "Sorted copy return karo.",
            },
        },
    },
    "insertion-sort": {
        "summary": {
            "en": (
                "Insertion sort builds the sorted list one element at a time, like "
                "sorting playing cards in your hand: take the next card and slide it "
                "left into its correct place."
            ),
            "hinglish": (
                "Insertion sort sorted list ek-ek element karke banata hai, bilkul taash "
                "ke patte hath mein sort karne ki tarah: agla patta lo aur use left mein "
                "sahi jagah tak khiskao."
            ),
        },
        "when_to_use": {
            "en": [
                "Small lists and nearly-sorted data (close to O(n)).",
                "As the finishing step inside faster hybrid sorts.",
            ],
            "hinglish": [
                "Chhote lists aur lagbhag sorted data ke liye (O(n) ke kareeb).",
                "Tez hybrid sorts ke andar aakhri step ke roop mein.",
            ],
        },
        "how_it_works": {
            "en": [
                "Treat the first element as a sorted part of size one.",
                "Take the next element as the 'key'.",
                "Shift every larger sorted value one slot to the right.",
                "Drop the key into the gap and repeat for the next element.",
            ],
            "hinglish": [
                "Pehle element ko size ek ka sorted hissa maano.",
                "Agle element ko 'key' ki tarah lo.",
                "Sorted hisse ke har bade value ko ek slot daayein khiskao.",
                "Key ko khaali jagah mein daalo aur agle element ke liye repeat karo.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best case O(n) on already sorted data (each key needs one "
                    "comparison). Average and worst case O(n²): a reverse-sorted list "
                    "shifts every earlier element."
                ),
                "space": "O(1) extra space: only the key and an index.",
            },
            "hinglish": {
                "time": (
                    "Best case O(n) pehle se sorted data par (har key ke liye ek hi "
                    "comparison). Average aur worst case O(n²): reverse-sorted list mein "
                    "har pichhla element khiskana padta hai."
                ),
                "space": "O(1) extra space: sirf key aur ek index.",
            },
        },
        "lines": {
            "insertion.init": {
                "en": "Validate the input and make a working copy so the original list is never changed.",
                "hinglish": "Input validate karo aur ek copy banao taaki original list kabhi change na ho.",
            },
            "insertion.outer_loop": {
                "en": "Start from index 1; everything to the left of i is already sorted.",
                "hinglish": "Index 1 se shuru karo; i ke left mein sab kuch pehle se sorted hai.",
            },
            "insertion.pick_key": {
                "en": "Pick the next value to insert. Saving it lets us overwrite its slot while shifting.",
                "hinglish": "Insert karne ke liye agla value uthao. Ise save karne se shifting ke dauraan uski jagah overwrite kar sakte hain.",
            },
            "insertion.start_scan": {
                "en": "Start scanning from the element just left of the key.",
                "hinglish": "Key ke theek left wale element se scan shuru karo.",
            },
            "insertion.shift_condition": {
                "en": "Keep going while there is a sorted value that is strictly greater than the key. Strictly greater keeps equal values in order (stable).",
                "hinglish": "Tab tak chalo jab tak koi sorted value key se strictly bada ho. Strictly bada rakhne se barabar values ka order bana rehta hai (stable).",
            },
            "insertion.shift": {
                "en": "Move that larger value one slot to the right.",
                "hinglish": "Us bade value ko ek slot daayein khiskao.",
            },
            "insertion.step_back": {
                "en": "Look one position further left.",
                "hinglish": "Ek position aur left mein dekho.",
            },
            "insertion.insert": {
                "en": "Place the key into the gap that the shifting created.",
                "hinglish": "Shifting se bani khaali jagah mein key ko rakh do.",
            },
            "insertion.return": {
                "en": "Return the sorted copy.",
                "hinglish": "Sorted copy return karo.",
            },
        },
    },
    "merge-sort": {
        "summary": {
            "en": (
                "Merge sort splits the list in half, sorts each half recursively, and "
                "merges the two sorted halves into one sorted list (divide and conquer)."
            ),
            "hinglish": (
                "Merge sort list ko beech se do hisson mein todta hai, har hisse ko "
                "recursively sort karta hai, phir do sorted hisson ko merge karke ek "
                "sorted list bana deta hai (divide and conquer)."
            ),
        },
        "when_to_use": {
            "en": [
                "When you need guaranteed O(n log n) time and a stable sort.",
                "Large lists where predictable performance matters.",
            ],
            "hinglish": [
                "Jab guaranteed O(n log n) time aur stable sort chahiye.",
                "Bade lists jahan predictable performance zaroori ho.",
            ],
        },
        "how_it_works": {
            "en": [
                "If the list has 0 or 1 elements it is already sorted.",
                "Split the list into a left half and a right half.",
                "Sort both halves recursively.",
                "Merge: repeatedly take the smaller front element of the two halves.",
            ],
            "hinglish": [
                "Agar list mein 0 ya 1 element hai to woh pehle se sorted hai.",
                "List ko left aur right do hisson mein baanto.",
                "Dono hisson ko recursively sort karo.",
                "Merge karo: dono hisson ke aage wale elements mein se chhota baar-baar lo.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "O(n log n) in every case: log n levels of splitting, and each "
                    "level merges n elements in total."
                ),
                "space": (
                    "O(n) auxiliary space for the merged lists, plus O(log n) for the "
                    "recursion stack."
                ),
            },
            "hinglish": {
                "time": (
                    "Har case mein O(n log n): log n levels par split hota hai aur har "
                    "level par kul n elements merge hote hain."
                ),
                "space": (
                    "Merged lists ke liye O(n) auxiliary space, aur recursion stack ke "
                    "liye O(log n)."
                ),
            },
        },
        "lines": {
            "merge.init": {
                "en": "Validate the input and make a working copy so the original list is never changed.",
                "hinglish": "Input validate karo aur ek copy banao taaki original list kabhi change na ho.",
            },
            "merge.def_helper": {
                "en": "Helper that sorts one (sub)list and returns a new sorted list.",
                "hinglish": "Helper jo ek (sub)list ko sort karke nayi sorted list return karta hai.",
            },
            "merge.base_check": {
                "en": "Base case: a list with 0 or 1 elements needs no sorting.",
                "hinglish": "Base case: 0 ya 1 element wali list ko sort karne ki zaroorat nahi.",
            },
            "merge.base_return": {
                "en": "Return it unchanged; this stops the recursion.",
                "hinglish": "Use bina badle return karo; yahin recursion ruk jaata hai.",
            },
            "merge.split": {
                "en": "Find the middle index to split the list.",
                "hinglish": "List todne ke liye beech ka index nikalo.",
            },
            "merge.sort_left": {
                "en": "Recursively sort the left half.",
                "hinglish": "Left hisse ko recursively sort karo.",
            },
            "merge.sort_right": {
                "en": "Recursively sort the right half.",
                "hinglish": "Right hisse ko recursively sort karo.",
            },
            "merge.merged_init": {
                "en": "Start an empty list that will hold the merged result.",
                "hinglish": "Ek khaali list shuru karo jismein merged result aayega.",
            },
            "merge.pointers": {
                "en": "i and j point at the front of the left and right halves.",
                "hinglish": "i aur j left aur right hisse ke aage wale element ko point karte hain.",
            },
            "merge.merge_loop": {
                "en": "Continue while both halves still have unmerged elements.",
                "hinglish": "Tab tak chalo jab tak dono hisson mein unmerged elements bache hain.",
            },
            "merge.compare": {
                "en": "Compare the two front elements. Using '<=' takes from the left on ties, which keeps the sort stable.",
                "hinglish": "Dono aage wale elements compare karo. '<=' se tie hone par left se lete hain, isse sort stable rehta hai.",
            },
            "merge.take_left": {
                "en": "The left front value is smaller or equal: append it to the result.",
                "hinglish": "Left ka aage wala value chhota ya barabar hai: use result mein jodo.",
            },
            "merge.advance_left": {
                "en": "Move the left pointer forward.",
                "hinglish": "Left pointer ko aage badhao.",
            },
            "merge.else_branch": {
                "en": "Otherwise the right front value is smaller.",
                "hinglish": "Warna right ka aage wala value chhota hai.",
            },
            "merge.take_right": {
                "en": "Append the right front value to the result.",
                "hinglish": "Right ke aage wale value ko result mein jodo.",
            },
            "merge.advance_right": {
                "en": "Move the right pointer forward.",
                "hinglish": "Right pointer ko aage badhao.",
            },
            "merge.leftover_left": {
                "en": "Copy any values left over in the left half (they are already sorted and larger than everything merged).",
                "hinglish": "Left hisse mein bache hue values copy karo (woh pehle se sorted hain aur merged sab values se bade hain).",
            },
            "merge.leftover_right": {
                "en": "Copy any values left over in the right half.",
                "hinglish": "Right hisse mein bache hue values copy karo.",
            },
            "merge.merge_return": {
                "en": "Return the merged sorted list for this subproblem.",
                "hinglish": "Is subproblem ki merged sorted list return karo.",
            },
            "merge.start": {
                "en": "Run the recursive sort on the whole copy and return the result.",
                "hinglish": "Poori copy par recursive sort chalao aur result return karo.",
            },
        },
    },
    "quick-sort": {
        "summary": {
            "en": (
                "Quick sort picks a pivot, rearranges the list so smaller values are "
                "left of the pivot and larger values are right of it, then sorts the "
                "two sides the same way."
            ),
            "hinglish": (
                "Quick sort ek pivot chunta hai, list ko aise arrange karta hai ki "
                "chhote values pivot ke left aur bade values right mein aa jaayein, "
                "phir dono taraf ko isi tarah sort karta hai."
            ),
        },
        "when_to_use": {
            "en": [
                "General-purpose in-memory sorting where average speed matters.",
                "When extra memory is limited (it sorts in place on its working copy).",
            ],
            "hinglish": [
                "General-purpose in-memory sorting jahan average speed zaroori ho.",
                "Jab extra memory kam ho (yeh apni working copy mein hi sort karta hai).",
            ],
        },
        "how_it_works": {
            "en": [
                "Choose the middle element as the pivot and move it to the end of the range.",
                "Scan the range, moving values smaller than the pivot to the front.",
                "Place the pivot right after those smaller values: it is now in its final position.",
                "Recurse on the smaller side and loop on the larger side to keep the stack shallow.",
            ],
            "hinglish": [
                "Beech ke element ko pivot chuno aur use range ke end mein le jao.",
                "Range scan karo aur pivot se chhote values ko aage ki taraf bhejo.",
                "Pivot ko un chhote values ke theek baad rakho: ab woh apni final position par hai.",
                "Chhote hisse par recursion karo aur bade hisse par loop chalao taaki stack gehra na ho.",
            ],
        },
        "complexity_notes": {
            "en": {
                "time": (
                    "Best and average case O(n log n) when pivots split the range "
                    "reasonably evenly. Worst case O(n²) when pivots are repeatedly "
                    "extreme (for example many equal values with Lomuto partitioning)."
                ),
                "space": (
                    "O(log n) auxiliary space for the call stack: recursing into the "
                    "smaller partition first bounds the depth by log2(n) even in the "
                    "worst case."
                ),
            },
            "hinglish": {
                "time": (
                    "Best aur average case O(n log n) jab pivot range ko lagbhag barabar "
                    "baantein. Worst case O(n²) jab pivot baar-baar extreme ho (jaise "
                    "bahut saare equal values aur Lomuto partitioning)."
                ),
                "space": (
                    "Call stack ke liye O(log n) auxiliary space: pehle chhote partition "
                    "mein recursion karne se depth worst case mein bhi log2(n) tak "
                    "seemit rehti hai."
                ),
            },
        },
        "lines": {
            "quick.init": {
                "en": "Validate the input and make a working copy so the original list is never changed.",
                "hinglish": "Input validate karo aur ek copy banao taaki original list kabhi change na ho.",
            },
            "quick.def_helper": {
                "en": "Helper that sorts arr[low..high] in place.",
                "hinglish": "Helper jo arr[low..high] ko wahin (in place) sort karta hai.",
            },
            "quick.loop": {
                "en": "Keep working while the range has at least two elements.",
                "hinglish": "Tab tak kaam karo jab tak range mein kam se kam do elements hain.",
            },
            "quick.choose_pivot": {
                "en": "Pick the middle index as the pivot. This avoids the classic slow case of already sorted input.",
                "hinglish": "Beech ke index ko pivot chuno. Isse pehle se sorted input wala classic slow case bachta hai.",
            },
            "quick.move_pivot": {
                "en": "Swap the pivot to the end of the range so the scan can ignore it.",
                "hinglish": "Pivot ko range ke end mein swap kar do taaki scan use ignore kar sake.",
            },
            "quick.pivot_value": {
                "en": "Remember the pivot value.",
                "hinglish": "Pivot ka value yaad rakho.",
            },
            "quick.boundary": {
                "en": "boundary marks where the 'smaller than pivot' region ends.",
                "hinglish": "boundary batata hai ki 'pivot se chhote' wala region kahan khatam hota hai.",
            },
            "quick.scan": {
                "en": "Scan every element except the pivot.",
                "hinglish": "Pivot ko chhodkar har element scan karo.",
            },
            "quick.compare": {
                "en": "Is this value smaller than the pivot?",
                "hinglish": "Kya yeh value pivot se chhota hai?",
            },
            "quick.swap_small": {
                "en": "Move it into the smaller-than-pivot region.",
                "hinglish": "Use pivot se chhote region mein le jao.",
            },
            "quick.advance_boundary": {
                "en": "Grow that region by one.",
                "hinglish": "Us region ko ek se badhao.",
            },
            "quick.place_pivot": {
                "en": "Put the pivot just after the smaller values. It is now in its final sorted position.",
                "hinglish": "Pivot ko chhote values ke theek baad rakho. Ab woh apni final sorted position par hai.",
            },
            "quick.pick_smaller": {
                "en": "Find which side of the pivot is smaller.",
                "hinglish": "Dekho pivot ki kaun si taraf chhoti hai.",
            },
            "quick.recurse_left": {
                "en": "Left side is smaller: sort it recursively.",
                "hinglish": "Left taraf chhoti hai: use recursively sort karo.",
            },
            "quick.continue_right": {
                "en": "Then continue the loop on the right side (no extra recursion).",
                "hinglish": "Phir right taraf par loop jaari rakho (extra recursion nahi).",
            },
            "quick.else_branch": {
                "en": "Otherwise the right side is the smaller one.",
                "hinglish": "Warna right taraf chhoti hai.",
            },
            "quick.recurse_right": {
                "en": "Sort the right side recursively.",
                "hinglish": "Right taraf ko recursively sort karo.",
            },
            "quick.continue_left": {
                "en": "Then continue the loop on the left side.",
                "hinglish": "Phir left taraf par loop jaari rakho.",
            },
            "quick.start": {
                "en": "Sort the whole copy, from the first index to the last.",
                "hinglish": "Poori copy ko pehle index se aakhri index tak sort karo.",
            },
            "quick.return": {
                "en": "Return the sorted copy.",
                "hinglish": "Sorted copy return karo.",
            },
        },
    },
}
