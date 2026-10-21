"use strict";

// =====================================================
// 1. GET THE HTML ELEMENTS
// =====================================================

const algorithmSelect = document.getElementById("algorithm");
const arrayInput = document.getElementById("arrayInput");
const targetInput = document.getElementById("targetInput");
const targetGroup = document.getElementById("targetGroup");
const languageSelect = document.getElementById("language");

const barsContainer = document.getElementById("bars");
const visualTitle = document.getElementById("visualTitle");
const visualSubtitle = document.getElementById("visualSubtitle");
const stepMessage = document.getElementById("stepMessage");
const notice = document.getElementById("notice");

const pythonCode = document.getElementById("pythonCode");
const explanation = document.getElementById("explanation");

const comparisonsDisplay = document.getElementById("comparisons");
const swapsDisplay = document.getElementById("swaps");
const writesDisplay = document.getElementById("writes");
const elapsedDisplay = document.getElementById("elapsed");

const progressFill = document.getElementById("progressFill");
const stepCount = document.getElementById("stepCount");

const previousBtn = document.getElementById("previousBtn");
const playBtn = document.getElementById("playBtn");
const nextBtn = document.getElementById("nextBtn");
const resetBtn = document.getElementById("resetBtn");
const runBtn = document.getElementById("runBtn");
const randomBtn = document.getElementById("randomBtn");
const speedInput = document.getElementById("speedInput");
const speedValue = document.getElementById("speedValue");


// =====================================================
// 2. APPLICATION STATE
// =====================================================

// These variables remember where we are in the animation.

let steps = [];
let currentStep = 0;
let playTimer = null;
let startedAt = 0;
let finishedAt = 0;
let isPlaying = false;
let stepDelay = speedInput ? Number(speedInput.value) || 550 : 550;
let lastRawInput = arrayInput ? arrayInput.value : "";
let sortedSet = new Set();

const searchingAlgorithms = [
    "linear",
    "binary",
    "jump",
    "interpolation",
    "exponential"
];

const sortedSearchAlgorithms = [
    "binary",
    "jump",
    "interpolation",
    "exponential"
];


// =====================================================
// 3. ALGORITHM INFORMATION
// =====================================================

const algorithmInfo = {
    bubble: {
        name: "Bubble Sort",
        best: "O(n)",
        average: "O(n²)",
        worst: "O(n²)",
        space: "O(1)",
        subtitle: "Repeatedly compare neighboring values.",
        en: "Bubble Sort compares neighboring values and swaps them when they are in the wrong order. After each pass, a large value settles toward the end.",
        hi: "Bubble Sort mein paas-paas ke numbers compare hote hain. Agar order galat ho, toh swap karte hain. Har pass mein bada number end ki taraf jaata hai."
    },
    selection: {
        name: "Selection Sort",
        best: "O(n²)",
        average: "O(n²)",
        worst: "O(n²)",
        space: "O(1)",
        subtitle: "Find the smallest remaining value.",
        en: "Selection Sort finds the smallest value in the unsorted part and places it at the next position.",
        hi: "Selection Sort unsorted part mein sabse chhota number dhoondta hai aur usko next correct position par rakhta hai."
    },
    insertion: {
        name: "Insertion Sort",
        best: "O(n)",
        average: "O(n²)",
        worst: "O(n²)",
        space: "O(1)",
        subtitle: "Insert each value into its correct position.",
        en: "Insertion Sort grows a sorted section from left to right. Each new value moves left until it reaches its correct position.",
        hi: "Insertion Sort left side par sorted section banata hai. Har naya number left move karta hai jab tak uski correct position nahi milti."
    },
    merge: {
        name: "Merge Sort",
        best: "O(n log n)",
        average: "O(n log n)",
        worst: "O(n log n)",
        space: "O(n)",
        subtitle: "Divide the array, then merge sorted parts.",
        en: "Merge Sort divides the array into smaller parts, sorts those parts, and merges them back together in order.",
        hi: "Merge Sort array ko chhote parts mein divide karta hai, unhe sort karta hai, phir sorted parts ko merge karta hai."
    },
    quick: {
        name: "Quick Sort",
        best: "O(n log n)",
        average: "O(n log n)",
        worst: "O(n²)",
        space: "O(log n)",
        subtitle: "Partition the array around a pivot.",
        en: "Quick Sort chooses a pivot and partitions values around it. It then sorts the smaller partitions recursively.",
        hi: "Quick Sort ek pivot choose karta hai. Chhote numbers ek side aur bade numbers doosri side aate hain, phir dono parts sort hote hain."
    },
    linear: {
        name: "Linear Search",
        best: "O(1)",
        average: "O(n)",
        worst: "O(n)",
        space: "O(1)",
        subtitle: "Check values one by one.",
        en: "Linear Search checks each value from left to right until it finds the target or reaches the end.",
        hi: "Linear Search har number ko left se right check karta hai jab tak target mil na jaaye ya array khatam na ho."
    },
    binary: {
        name: "Binary Search",
        best: "O(1)",
        average: "O(log n)",
        worst: "O(log n)",
        space: "O(1)",
        subtitle: "Repeatedly eliminate half the search range.",
        en: "Binary Search checks the middle value. Because the array is sorted, it can discard half of the remaining search range each time.",
        hi: "Binary Search middle number check karta hai. Sorted array mein har step par aadha search range hata sakte hain."
    },
    jump: {
        name: "Jump Search",
        best: "O(1)",
        average: "O(√n)",
        worst: "O(√n)",
        space: "O(1)",
        subtitle: "Jump ahead in blocks, then search locally.",
        en: "Jump Search skips through blocks of a sorted array, then checks individual values in the block that may contain the target.",
        hi: "Jump Search sorted array mein blocks skip karta hai. Possible block milne par uske numbers ek-ek karke check karta hai."
    },
    interpolation: {
        name: "Interpolation Search",
        best: "O(1)",
        average: "O(log log n)*",
        worst: "O(n)",
        space: "O(1)",
        subtitle: "Estimate where the target may be.",
        en: "Interpolation Search estimates the target's likely position using the values at the ends of the sorted range. Its average bound assumes roughly uniform data.",
        hi: "Interpolation Search end values dekh kar target ki likely position estimate karta hai. Average performance tab achhi hoti hai jab values roughly evenly distributed hon."
    },
    exponential: {
        name: "Exponential Search",
        best: "O(1)",
        average: "O(log n)",
        worst: "O(log n)",
        space: "O(1)",
        subtitle: "Expand the range exponentially, then use binary search.",
        en: "Exponential Search checks positions 1, 2, 4, 8 and so on to find a range, then performs Binary Search inside that range.",
        hi: "Exponential Search pehle 1, 2, 4, 8 jaise positions check karke range dhoondta hai, phir us range mein Binary Search karta hai."
    }
};


// =====================================================
// 4. PYTHON CODE FOR THE CODE PANEL
// =====================================================

const pythonExamples = {
    bubble: `def bubble_sort(arr):
    n = len(arr)

    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = (
                    arr[j + 1], arr[j]
                )

    return arr`,

    selection: `def selection_sort(arr):
    n = len(arr)

    for i in range(n):
        smallest = i

        for j in range(i + 1, n):
            if arr[j] < arr[smallest]:
                smallest = j

        arr[i], arr[smallest] = (
            arr[smallest], arr[i]
        )

    return arr`,

    insertion: `def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr`,

    merge: `def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result`,

    quick: `def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]
    smaller = [x for x in arr[:-1] if x <= pivot]
    larger = [x for x in arr[:-1] if x > pivot]

    return (
        quick_sort(smaller)
        + [pivot]
        + quick_sort(larger)
    )`,

    linear: `def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i

    return -1`,

    binary: `def binary_search(arr, target):
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1`,

    jump: `import math

def jump_search(arr, target):
    n = len(arr)
    step = int(math.sqrt(n))
    start = 0
    end = step

    while start < n and arr[min(end, n) - 1] < target:
        start = end
        end += step

        if start >= n:
            return -1

    for i in range(start, min(end, n)):
        if arr[i] == target:
            return i

    return -1`,

    interpolation: `def interpolation_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        if target < arr[low] or target > arr[high]:
            return -1

        if arr[low] == arr[high]:
            return low if arr[low] == target else -1

        pos = low + int(
            (target - arr[low]) * (high - low)
            / (arr[high] - arr[low])
        )

        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1`,

    exponential: `def binary_search_range(arr, target, low, high):
    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

def exponential_search(arr, target):
    n = len(arr)

    if n == 0:
        return -1
    if arr[0] == target:
        return 0

    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2

    return binary_search_range(
        arr, target, bound // 2, min(bound, n - 1)
    )`
};


// =====================================================
// 5. COMPLEXITY AND CODE DISPLAY
// =====================================================

function updateAlgorithmInfo() {
    const name = algorithmSelect.value;
    const info = algorithmInfo[name];

    visualTitle.textContent = info.name;
    visualSubtitle.textContent = info.subtitle;

    document.getElementById("bestCase").textContent = info.best;
    document.getElementById("averageCase").textContent = info.average;
    document.getElementById("worstCase").textContent = info.worst;
    document.getElementById("spaceCase").textContent = info.space;

    renderCodePanel(name, steps[currentStep] ? steps[currentStep].line : 1);

    targetGroup.style.display = searchingAlgorithms.includes(name)
        ? "flex"
        : "none";

    const activeStep = steps[currentStep];
    const stepPrefix = activeStep ? `${languageSelect.value === "hi" ? activeStep.hi : activeStep.en} — ` : "";
    explanation.textContent = stepPrefix + (languageSelect.value === "hi" ? info.hi : info.en);
    if (false) explanation.textContent = languageSelect.value === "hi"
        ? info.hi
        : info.en;
}


// =====================================================
// 6. READ AND VALIDATE USER INPUT
// =====================================================

function getArrayFromInput() {
    const raw = arrayInput.value.trim();

    if (!raw) {
        return [];
    }

    const parts = raw.split(",");

    if (parts.length > 40) {
        throw new Error("Please use 40 numbers or fewer.");
    }

    const numbers = parts.map(part => part.trim());

    if (numbers.some(part => part === "" || !Number.isFinite(Number(part)))) {
        throw new Error("Use valid numbers separated by commas.");
    }

    return numbers.map(Number);
}


// =====================================================
// 7. CREATE AND SAVE ANIMATION STEPS
// =====================================================

let workingArray = [];
let comparisons = 0;
let swaps = 0;
let writes = 0;

const codeLineMap = {
    "bubble.init": 1, "bubble.outer_loop": 4, "bubble.compare": 6, "bubble.swap": 7, "bubble.done": 11,
    "selection.init": 1, "selection.outer_loop": 4, "selection.compare": 8, "selection.swap": 11, "selection.done": 15,
    "insertion.init": 1, "insertion.pick_key": 3, "insertion.compare": 6, "insertion.shift": 7, "insertion.insert": 10, "insertion.done": 12,
    "merge.init": 1, "merge.divide": 5, "merge.compare": 13, "merge.write": 14, "merge.copy_left": 20, "merge.copy_right": 21, "merge.done": 22,
    "quick.init": 1, "quick.choose_pivot": 5, "quick.compare": 6, "quick.swap": 7, "quick.pivot_placed": 9, "quick.done": 12,
    "linear.init": 1, "linear.compare": 3, "linear.found": 4, "linear.not_found": 6,
    "binary.init": 1, "binary.mid": 6, "binary.found": 9, "binary.go_right": 11, "binary.go_left": 13, "binary.not_found": 15,
    "jump.init": 3, "jump.block_found": 9, "jump.jump_advance": 10, "jump.scan_compare": 17, "jump.found": 18, "jump.not_found": 20,
    "interpolation.init": 1, "interpolation.estimate": 12, "interpolation.found": 18, "interpolation.go_right": 20, "interpolation.go_left": 22, "interpolation.not_found": 24,
    "exponential.init": 14, "exponential.empty": 18, "exponential.first_found": 20, "exponential.grow_check": 23, "exponential.grow_double": 24, "exponential.found": 6, "exponential.go_right": 8, "exponential.go_left": 10, "exponential.not_found": 12
};

function renderCodePanel(algo, activeLine = 1) {
    const source = pythonExamples[algo] || "";
    const lines = source.split(/\r?\n/);
    pythonCode.replaceChildren();
    let activeEl = null;

    lines.forEach((text, idx) => {
        const lineNo = idx + 1;
        const row = document.createElement("div");
        row.className = lineNo === activeLine ? "code-line active" : "code-line";
        row.dataset.line = String(lineNo);

        const numSpan = document.createElement("span");
        numSpan.className = "code-line-num";
        numSpan.textContent = String(lineNo);

        const textSpan = document.createElement("span");
        textSpan.className = "code-line-text";
        textSpan.textContent = text;

        row.append(numSpan, textSpan);
        pythonCode.appendChild(row);
        if (lineNo === activeLine) activeEl = row;
    });

    if (activeEl && typeof activeEl.scrollIntoView === "function") {
        activeEl.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
}

function inferStepMeta(algo, message) {
    let suffix = "init";
    if (message.startsWith("Starting array:")) suffix = "init";
    else if (message.startsWith("Sorting complete!")) suffix = "done";
    else if (message.startsWith("Found 0") || (algo === "exponential" && message.includes("at index 0!"))) suffix = "first_found";
    else if (message.startsWith("Found ")) suffix = "found";
    else if (message.includes("was not found")) suffix = "not_found";
    else if (message.startsWith("The array is empty")) suffix = "empty";
    else if (algo === "bubble") {
        if (message.startsWith("Compare ")) suffix = "compare";
        else if (message.includes("swap them")) suffix = "swap";
        else if (message.startsWith("No swaps")) suffix = "done";
        else suffix = "outer_loop";
    } else if (algo === "selection") {
        if (message.startsWith("Compare ")) suffix = "compare";
        else if (message.startsWith("Place ")) suffix = "swap";
        else suffix = "outer_loop";
    } else if (algo === "insertion") {
        if (message.startsWith("Take ")) suffix = "pick_key";
        else if (message.startsWith("Compare ") || message.startsWith("Check ")) suffix = "compare";
        else if (message.startsWith("Shift ")) suffix = "shift";
        else suffix = "insert";
    } else if (algo === "merge") {
        if (message.startsWith("Divide ")) suffix = "divide";
        else if (message.startsWith("Compare ")) suffix = "compare";
        else if (message.startsWith("Merge ")) suffix = "write";
        else if (message.includes("remaining left")) suffix = "copy_left";
        else suffix = "copy_right";
    } else if (algo === "quick") {
        if (message.startsWith("Choose ")) suffix = "choose_pivot";
        else if (message.startsWith("Compare ")) suffix = "compare";
        else if (message.startsWith("Move ")) suffix = "swap";
        else suffix = "pivot_placed";
    } else if (algo === "linear") {
        suffix = "compare";
    } else if (algo === "binary") {
        suffix = message.includes("right half") ? "go_right" : "go_left";
    } else if (algo === "jump") {
        if (message.startsWith("The target may be")) suffix = "block_found";
        else if (message.startsWith("Jump past")) suffix = "jump_advance";
        else suffix = "scan_compare";
    } else if (algo === "interpolation") {
        suffix = message.includes("Move right") ? "go_right" : "go_left";
    } else if (algo === "exponential") {
        if (message.startsWith("The target is within")) suffix = "grow_check";
        else if (message.startsWith("Expand ")) suffix = "grow_double";
        else suffix = message.includes("right half") ? "go_right" : "go_left";
    }

    const lineId = `${algo}.${suffix}`;
    const line = codeLineMap[lineId] || 1;
    const hi = message
        .replace(/^Starting array: (.*)$/, "Shuruaati array: $1")
        .replace(/^Sorting complete! The array is in ascending order\.$/, "Sorting poori hui! Array ab ascending order mein hai.")
        .replace(/^Compare the current minimum (.+) with (.+)\.$/, "Current minimum $1 ko $2 ke saath compare karein.")
        .replace(/^Compare left value (.+) and right value (.+)\.$/, "Left value $1 aur right value $2 ko compare karein.")
        .replace(/^Compare sorted value (.+) at index (.+) with key (.+)\.$/, "Index $2 ki sorted value $1 ko key $3 se compare karein.")
        .replace(/^Compare (.+) with pivot (.+)\.$/, "$1 ko pivot $2 se compare karein.")
        .replace(/^Compare (.+) and (.+)\.$/, "$1 aur $2 ko compare karein.")
        .replace(/^The values are in the wrong order, so swap them\.$/, "Values galat order mein hain, isliye inhe swap karein.")
        .replace(/^No swaps needed in this pass\. Remaining elements are sorted\.$/, "Is pass mein koi swap nahi hua. Baaki elements pehle se sorted hain.")
        .replace(/^Value (.+) at index (.+) is now in its sorted position\.$/, "Index $2 par value $1 ab apni final sorted position par hai.")
        .replace(/^Place (.+) into sorted position (.+)\.$/, "Sabse chhoti value $1 ko sorted position $2 par rakhein.")
        .replace(/^(.+) is already the smallest remaining value at index (.+)\.$/, "Index $2 par $1 pehle se hi sabse chhoti bachi hui value hai.")
        .replace(/^Take key (.+) at index (.+) and find its place in sorted prefix \[0\.\.(.+)\]\.$/, "Index $2 se key $1 lein aur sorted prefix [0..$3] mein iski sahi jagah dhoondein.")
        .replace(/^Shift (.+) right from index (.+) to (.+) to make room for key (.+)\.$/, "Key $4 ke liye jagah banane ko $1 ko index $2 se $3 par right shift karein.")
        .replace(/^Insert key (.+) at sorted index (.+)\.$/, "Key $1 ko sorted index $2 par insert karein.")
        .replace(/^Divide the section from index (.+) to (.+)\.$/, "Index $1 se $2 tak ke section ko divide karein.")
        .replace(/^Merge the smaller available value at index (.+)\.$/, "Chhoti value ko merge karke index $1 par likhein.")
        .replace(/^Copy the remaining left value to index (.+)\.$/, "Bachi hui left value ko index $1 par copy karein.")
        .replace(/^Copy the remaining right value to index (.+)\.$/, "Bachi hui right value ko index $1 par copy karein.")
        .replace(/^Choose (.+) as the pivot\.$/, "$1 ko pivot chunein.")
        .replace(/^Move a value smaller than or equal to the pivot to the left\.$/, "Pivot se chhoti ya barabar value ko left side swap karein.")
        .replace(/^Place pivot (.+) into its correct position\.$/, "Pivot $1 ko uski sahi sorted position par rakhein.")
        .replace(/^Pivot (.+) at index (.+) is now in its sorted position\.$/, "Index $2 par pivot $1 ab apni sahi sorted position par hai.")
        .replace(/^Found (.+) at index (.+)!$/, "Target $1 index $2 par mil gaya!")
        .replace(/^Index (.+): (.+) is not the target\.$/, "Index $1 par $2 target nahi hai, aage check karein.")
        .replace(/^Target (.+) was not found.*$/, "Target $1 array mein nahi mila.")
        .replace(/^(.+) is too small\. Search the right half\.$/, "$1 target se chhota hai. Right half mein search karein.")
        .replace(/^(.+) is too large\. Search the left half\.$/, "$1 target se bada hai. Left half mein search karein.")
        .replace(/^The target may be in this block\. Check individual values\.$/, "Target is block mein ho sakta hai. Ab ek-ek value check karein.")
        .replace(/^Jump past the block ending at (.+)\.$/, "$1 par khatam hone wale block ke aage jump karein.")
        .replace(/^Check (.+) at index (.+)\.$/, "Index $2 par value $1 check karein.")
        .replace(/^Estimated position (.+) is too small\. Move right\.$/, "Estimated position $1 chhoti hai. Right move karein.")
        .replace(/^Estimated position (.+) is too large\. Move left\.$/, "Estimated position $1 badi hai. Left move karein.")
        .replace(/^The array is empty\.$/, "Array khaali hai.")
        .replace(/^The target is within the range ending at index (.+)\.$/, "Target index $1 tak ke range ke andar hai.")
        .replace(/^Expand the search range to index (.+)\.$/, "Search range ko double karke index $1 tak badhayein.")
        .replace(/^Check (.+)\. Search the right half\.$/, "$1 check kiya. Ab right half mein search karein.")
        .replace(/^Check (.+)\. Search the left half\.$/, "$1 check kiya. Ab left half mein search karein.");

    return { lineId, line, en: message, hi };
}

function saveStep(message, active = [], sorted = [], found = []) {
    for (const idx of sorted) sortedSet.add(idx);
    const meta = inferStepMeta(algorithmSelect.value, message);
    steps.push({
        array: [...workingArray],
        comparisons,
        swaps,
        writes,
        message,
        active: [...active],
        en: meta.en,
        hi: meta.hi,
        lineId: meta.lineId,
        line: meta.line,
        sorted: [...sortedSet].sort((a, b) => a - b),
        found: [...found]
    });
}

function compare(i, j, message) {
    comparisons++;
    saveStep(message, [i, j]);
}

function swap(i, j, message) {
    [workingArray[i], workingArray[j]] =
        [workingArray[j], workingArray[i]];

    swaps++;
    writes += 2;

    saveStep(message, [i, j]);
}


// =====================================================
// 8. BUBBLE SORT
// =====================================================

function bubbleSort() {
    const n = workingArray.length;

    for (let i = 0; i < n; i++) {
        let changed = false;

        for (let j = 0; j < n - i - 1; j++) {
            compare(j, j + 1,
                `Compare ${workingArray[j]} and ${workingArray[j + 1]}.`);

            if (workingArray[j] > workingArray[j + 1]) {
                swap(j, j + 1, "The values are in the wrong order, so swap them.");
                changed = true;
            }
        }

        sortedSet.add(n - 1 - i);
        if (!changed) {
            for (let k = 0; k < n - 1 - i; k++) sortedSet.add(k);
            saveStep("No swaps needed in this pass. Remaining elements are sorted.", [], [n - 1 - i]);
            break;
        }
        saveStep(`Value ${workingArray[n - 1 - i]} at index ${n - 1 - i} is now in its sorted position.`, [], [n - 1 - i]);
    }
}


// =====================================================
// 9. SELECTION SORT
// =====================================================

function selectionSort() {
    const n = workingArray.length;

    for (let i = 0; i < n - 1; i++) {
        let smallest = i;

        for (let j = i + 1; j < n; j++) {
            compare(smallest, j,
                `Compare the current minimum ${workingArray[smallest]} with ${workingArray[j]}.`);

            if (workingArray[j] < workingArray[smallest]) {
                smallest = j;
            }
        }

        if (smallest !== i) {
            const minVal = workingArray[smallest];
            sortedSet.add(i);
            swap(i, smallest, `Place ${minVal} into sorted position ${i}.`);
        } else {
            sortedSet.add(i);
            saveStep(`${workingArray[i]} is already the smallest remaining value at index ${i}.`, [i], [i]);
        }
    }
}


// =====================================================
// 10. INSERTION SORT
// =====================================================

function insertionSort() {
    if (workingArray.length > 0) sortedSet.add(0);
    for (let i = 1; i < workingArray.length; i++) {
        const key = workingArray[i];
        let j = i - 1;

        saveStep(`Take key ${key} at index ${i} and find its place in sorted prefix [0..${i - 1}].`, [i]);

        while (j >= 0) {
            compare(j, j + 1,
                `Compare sorted value ${workingArray[j]} at index ${j} with key ${key}.`);

            if (workingArray[j] <= key) break;

            workingArray[j + 1] = workingArray[j];
            writes++;

            saveStep(`Shift ${workingArray[j]} right from index ${j} to ${j + 1} to make room for key ${key}.`, [j, j + 1]);
            j--;
        }

        workingArray[j + 1] = key;
        writes++;

        sortedSet.add(i);
        saveStep(`Insert key ${key} at sorted index ${j + 1}.`, [j + 1], [i]);
    }
}


// =====================================================
// 11. MERGE SORT
// =====================================================

function mergeSort() {
    function divide(left, right) {
        if (left >= right) return;

        const mid = Math.floor((left + right) / 2);

        saveStep(`Divide the section from index ${left} to ${right}.`,
            [left, mid, right]);

        divide(left, mid);
        divide(mid + 1, right);

        const leftPart = workingArray.slice(left, mid + 1);
        const rightPart = workingArray.slice(mid + 1, right + 1);

        let i = 0;
        let j = 0;
        let k = left;

        while (i < leftPart.length && j < rightPart.length) {
            comparisons++;

            saveStep(`Compare left value ${leftPart[i]} and right value ${rightPart[j]}.`, [left + i, mid + 1 + j]);
            if (leftPart[i] <= rightPart[j]) {
                workingArray[k] = leftPart[i++];
            } else {
                workingArray[k] = rightPart[j++];
            }

            writes++;
            if (k === right) { for (let idx = left; idx <= right; idx++) sortedSet.add(idx); }
            saveStep(`Merge the smaller available value at index ${k}.`, [k]);
            k++;
        }

        while (i < leftPart.length) {
            workingArray[k] = leftPart[i++];
            writes++;
            if (k === right) { for (let idx = left; idx <= right; idx++) sortedSet.add(idx); }
            saveStep(`Copy the remaining left value to index ${k}.`, [k]);
            k++;
        }

        while (j < rightPart.length) {
            workingArray[k] = rightPart[j++];
            writes++;
            if (k === right) { for (let idx = left; idx <= right; idx++) sortedSet.add(idx); }
            saveStep(`Copy the remaining right value to index ${k}.`, [k]);
            k++;
        }
    }

    divide(0, workingArray.length - 1);
}


// =====================================================
// 12. QUICK SORT
// =====================================================

function quickSort() {
    function partition(low, high) {
        const pivot = workingArray[high];

        saveStep(`Choose ${pivot} as the pivot.`, [high]);

        let i = low;

        for (let j = low; j < high; j++) {
            compare(j, high,
                `Compare ${workingArray[j]} with pivot ${pivot}.`);

            if (workingArray[j] <= pivot) {
                if (i !== j) {
                    swap(i, j, "Move a value smaller than or equal to the pivot to the left.");
                }
                i++;
            }
        }

        if (i !== high) {
            sortedSet.add(i);
            swap(i, high, `Place pivot ${pivot} into its correct position.`);
        } else {
            sortedSet.add(i);
            saveStep(`Pivot ${pivot} at index ${i} is now in its sorted position.`, [i], [i]);
        }

        return i;
    }

    function sort(low, high) {
        if (low >= high) {
            if (low === high && low >= 0 && low < workingArray.length) sortedSet.add(low);
            return;
        }

        const pivotIndex = partition(low, high);
        sort(low, pivotIndex - 1);
        sort(pivotIndex + 1, high);
    }

    sort(0, workingArray.length - 1);
}


// =====================================================
// 13. LINEAR SEARCH
// =====================================================

function linearSearch(target) {
    for (let i = 0; i < workingArray.length; i++) {
        comparisons++;

        if (workingArray[i] === target) {
            saveStep(`Found ${target} at index ${i}!`, [i], [], [i]);
            return;
        }

        saveStep(`Index ${i}: ${workingArray[i]} is not the target.`, [i]);
    }

    saveStep(`Target ${target} was not found in the array.`);
}


// =====================================================
// 14. BINARY SEARCH
// =====================================================

function binarySearch(target) {
    let left = 0;
    let right = workingArray.length - 1;

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        comparisons++;

        if (workingArray[mid] === target) {
            saveStep(`Found ${target} at index ${mid}!`, [mid], [], [mid]);
            return;
        }

        if (workingArray[mid] < target) {
            saveStep(`${workingArray[mid]} is too small. Search the right half.`, [mid]);
            left = mid + 1;
        } else {
            saveStep(`${workingArray[mid]} is too large. Search the left half.`, [mid]);
            right = mid - 1;
        }
    }

    saveStep(`Target ${target} was not found.`);
}


// =====================================================
// 15. JUMP SEARCH
// =====================================================

function jumpSearch(target) {
    const n = workingArray.length;
    const jump = Math.max(1, Math.floor(Math.sqrt(n)));
    let start = 0;
    let end = jump;

    while (start < n) {
        const last = Math.min(end, n) - 1;
        comparisons++;

        if (workingArray[last] >= target) {
            saveStep(`The target may be in this block. Check individual values.`, [last]);
            break;
        }

        saveStep(`Jump past the block ending at ${workingArray[last]}.`, [last]);

        start = end;
        end += jump;
    }

    if (start >= n) {
        saveStep(`Target ${target} was not found.`);
        return;
    }

    for (let i = start; i < Math.min(end, n); i++) {
        comparisons++;

        if (workingArray[i] === target) {
            saveStep(`Found ${target} at index ${i}!`, [i], [], [i]);
            return;
        }

        saveStep(`Check ${workingArray[i]} at index ${i}.`, [i]);

        if (workingArray[i] > target) break;
    }

    saveStep(`Target ${target} was not found.`);
}


// =====================================================
// 16. INTERPOLATION SEARCH
// =====================================================

function interpolationSearch(target) {
    let low = 0;
    let high = workingArray.length - 1;

    while (
        low <= high &&
        target >= workingArray[low] &&
        target <= workingArray[high]
    ) {
        if (workingArray[low] === workingArray[high]) {
            comparisons++;

            if (workingArray[low] === target) {
                saveStep(`Found ${target} at index ${low}!`, [low], [], [low]);
            } else {
                saveStep(`Target ${target} was not found.`);
            }
            return;
        }

        const position = low + Math.floor(
            ((target - workingArray[low]) * (high - low)) /
            (workingArray[high] - workingArray[low])
        );

        comparisons++;

        if (workingArray[position] === target) {
            saveStep(`Found ${target} at index ${position}!`, [position], [], [position]);
            return;
        }

        if (workingArray[position] < target) {
            saveStep(`Estimated position ${position} is too small. Move right.`, [position]);
            low = position + 1;
        } else {
            saveStep(`Estimated position ${position} is too large. Move left.`, [position]);
            high = position - 1;
        }
    }

    saveStep(`Target ${target} was not found.`);
}


// =====================================================
// 17. EXPONENTIAL SEARCH
// =====================================================

function exponentialSearch(target) {
    const n = workingArray.length;

    if (n === 0) {
        saveStep("The array is empty.");
        return;
    }

    comparisons++;

    if (workingArray[0] === target) {
        saveStep(`Found ${target} at index 0!`, [0], [], [0]);
        return;
    }

    let bound = 1;

    while (bound < n) {
        comparisons++;

        if (workingArray[bound] >= target) {
            saveStep(`The target is within the range ending at index ${bound}.`, [bound]);
            break;
        }

        saveStep(`Expand the search range to index ${bound * 2}.`, [bound]);
        bound *= 2;
    }

    let left = Math.floor(bound / 2);
    let right = Math.min(bound, n - 1);

    while (left <= right) {
        const mid = Math.floor((left + right) / 2);
        comparisons++;

        if (workingArray[mid] === target) {
            saveStep(`Found ${target} at index ${mid}!`, [mid], [], [mid]);
            return;
        }

        if (workingArray[mid] < target) {
            saveStep(`Check ${workingArray[mid]}. Search the right half.`, [mid]);
            left = mid + 1;
        } else {
            saveStep(`Check ${workingArray[mid]}. Search the left half.`, [mid]);
            right = mid - 1;
        }
    }

    saveStep(`Target ${target} was not found.`);
}


// =====================================================
// 18. START A VISUALIZATION
// =====================================================

function runVisualization() {
    stopPlayback();

    try {
        workingArray = getArrayFromInput();
    } catch (error) {
        notice.textContent = error.message;
        return;
    }

    const algorithm = algorithmSelect.value;
    const isSearching = searchingAlgorithms.includes(algorithm);
    const target = Number(targetInput.value);

    if (isSearching && targetInput.value.trim() === "") {
        notice.textContent = "Please enter a search target.";
        return;
    }

    if (isSearching && !Number.isFinite(target)) {
        notice.textContent = "Please enter a valid search target.";
        return;
    }

    if (isSearching && sortedSearchAlgorithms.includes(algorithm)) {
        lastRawInput = arrayInput.value;
        workingArray.sort((a, b) => a - b);
        arrayInput.value = workingArray.join(", ");

        notice.textContent =
            "This algorithm requires sorted input. Your array was sorted before searching.";
    } else {
        notice.textContent = isSearching
            ? "Searching the array in its current order."
            : "Visualization ready. Use the playback controls to explore each step.";
    }

    steps = [];
    currentStep = 0;
    comparisons = 0;
    swaps = 0;
    writes = 0;

    sortedSet.clear();
    if (!isSearching || !sortedSearchAlgorithms.includes(algorithm)) {
        lastRawInput = arrayInput.value;
    }
    if (workingArray.length === 0) {
        notice.textContent = "Please enter some numbers. Showing empty array state.";
    }
    saveStep("Starting array: " + (workingArray.length ? workingArray.join(", ") : "(empty)"));

    startedAt = performance.now();
    finishedAt = 0;

    if (isSearching) {
        const searchFunctions = {
            linear: linearSearch,
            binary: binarySearch,
            jump: jumpSearch,
            interpolation: interpolationSearch,
            exponential: exponentialSearch
        };

        searchFunctions[algorithm](target);
    } else {
        const sortFunctions = {
            bubble: bubbleSort,
            selection: selectionSort,
            insertion: insertionSort,
            merge: mergeSort,
            quick: quickSort
        };

        sortFunctions[algorithm]();
        saveStep("Sorting complete! The array is in ascending order.",
            [], workingArray.map((_, i) => i));
    }

    finishedAt = performance.now();

    renderStep(0);
    updateAlgorithmInfo();

    if (steps.length > 1) {
        notice.textContent += ` ${steps.length - 1} recorded steps are ready to explore.`;
    }
}


// =====================================================
// 19. DISPLAY ONE STEP
// =====================================================

function renderStep(index) {
    if (!steps.length) return;

    currentStep = Math.max(0, Math.min(index, steps.length - 1));

    const step = steps[currentStep];
    const maxValue = Math.max(...step.array.map(Math.abs), 1);

    barsContainer.replaceChildren();

    step.array.forEach((value, i) => {
        const bar = document.createElement("div");
        bar.classList.add("bar");

        const height = Math.max(8, (Math.abs(value) / maxValue) * 190);
        bar.style.height = `${height}px`;

        if (step.active.includes(i)) {
            bar.classList.add("comparing");
        }

        if (step.sorted.includes(i) && !step.active.includes(i)) {
            bar.classList.add("sorted");
        }

        if (step.found.includes(i)) {
            bar.classList.remove("comparing");
            bar.classList.add("found");
        }

        const valueLabel = document.createElement("span");
        valueLabel.className = "bar-value";
        valueLabel.textContent = value;

        const indexLabel = document.createElement("span");
        indexLabel.className = "bar-index";
        indexLabel.textContent = i;

        bar.append(valueLabel, indexLabel);
        barsContainer.appendChild(bar);
    });

    comparisonsDisplay.textContent = step.comparisons;
    swapsDisplay.textContent = step.swaps;
    writesDisplay.textContent = step.writes;

    const isHi = languageSelect.value === "hi";
    const localizedMsg = (isHi ? step.hi : step.en) || step.message;
    stepMessage.textContent = localizedMsg;
    const info = algorithmInfo[algorithmSelect.value];
    explanation.textContent = `${localizedMsg} — ${isHi ? info.hi : info.en}`;
    renderCodePanel(algorithmSelect.value, step.line || 1);

    const percentage = steps.length <= 1
        ? 100
        : (currentStep / (steps.length - 1)) * 100;

    progressFill.style.width = `${percentage}%`;
    stepCount.textContent =
        `Step ${currentStep + 1} of ${steps.length}`;

    previousBtn.disabled = currentStep === 0;
    nextBtn.disabled = currentStep >= steps.length - 1;
    playBtn.disabled = steps.length <= 1;
    resetBtn.disabled = currentStep === 0 && !isPlaying && arrayInput.value === lastRawInput;

    const totalMs = Math.max(0.05, finishedAt - startedAt);
    const ratio = steps.length <= 1 ? 0 : currentStep / (steps.length - 1);
    const elapsed = totalMs * ratio;
    elapsedDisplay.textContent = `${elapsed.toFixed(2)} ms`;
}


// =====================================================
// 20. PLAYBACK CONTROLS
// =====================================================

function stopPlayback() {
    if (playTimer !== null) {
        clearInterval(playTimer);
        playTimer = null;
    }

    isPlaying = false;
    playBtn.textContent = "▶ Play";
}

function playVisualization() {
    if (!steps.length || isPlaying) return;

    if (currentStep >= steps.length - 1) {
        renderStep(0);
    }

    isPlaying = true;
    playBtn.textContent = "Ⅱ Pause";

    playTimer = setInterval(() => {
        if (currentStep >= steps.length - 1) {
            stopPlayback();
            return;
        }

        renderStep(currentStep + 1);
    }, stepDelay);
}

playBtn.addEventListener("click", () => {
    if (isPlaying) {
        stopPlayback();
    } else {
        playVisualization();
    }
});

previousBtn.addEventListener("click", () => {
    stopPlayback();
    renderStep(currentStep - 1);
});

nextBtn.addEventListener("click", () => {
    stopPlayback();
    renderStep(currentStep + 1);
});

if (speedInput) {
    const onSpeedChange = () => {
        stepDelay = Math.max(100, Math.min(1200, Number(speedInput.value) || 550));
        if (speedValue) speedValue.textContent = `${stepDelay} ms`;
        if (isPlaying) {
            clearInterval(playTimer);
            playTimer = setInterval(() => {
                if (currentStep >= steps.length - 1) {
                    stopPlayback();
                    renderStep(currentStep);
                    return;
                }
                renderStep(currentStep + 1);
            }, stepDelay);
        }
    };
    speedInput.addEventListener("input", onSpeedChange);
    speedInput.addEventListener("change", onSpeedChange);
}

resetBtn.addEventListener("click", () => {
    if (lastRawInput && arrayInput.value !== lastRawInput) {
        arrayInput.value = lastRawInput;
    }
    notice.textContent = "Visualization reset to Step 1.";
    stopPlayback();
    renderStep(0);
});

runBtn.addEventListener("click", runVisualization);

randomBtn.addEventListener("click", () => {
    stopPlayback();

    const randomNumbers = Array.from(
        { length: 8 },
        () => Math.floor(Math.random() * 90) + 10
    );

    arrayInput.value = randomNumbers.join(", ");
    runVisualization();
});

algorithmSelect.addEventListener("change", () => {
    updateAlgorithmInfo();
    runVisualization();
});

languageSelect.addEventListener("change", () => {
    if (steps.length) renderStep(currentStep);
    updateAlgorithmInfo();
});


// =====================================================
// 21. INITIALIZE THE WEBSITE
// =====================================================

updateAlgorithmInfo();
runVisualization();