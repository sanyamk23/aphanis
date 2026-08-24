// Untrace AI Browser Extension - Popup Logic
// Runs entirely in the browser, no external dependencies.

const ZERO_WIDTH_CHARS = [
  '​', '‌', '‍', '‎', '‏',
  '‪', '‫', '‬', '‭', '‮',
  '⁠', '⁡', '⁢', '⁣', '⁤',
  '⁦', '⁧', '⁨', '⁩',
  '﻿', '￼',
];

const PUNCTUATION_REPLACEMENTS = {
  '“': '"', '”': '"',
  '‘': "'", '’': "'",
  '—': ' - ', '–': '-',
  '…': '...'
};

const AI_VOCAB_SWAPS = {
  'delve': 'explore', 'delving': 'exploring', 'delves': 'explores',
  'testament': 'proof', 'testaments': 'proofs',
  'spearhead': 'lead', 'spearheaded': 'led', 'spearheading': 'leading',
  'fostering': 'building', 'foster': 'encourage',
  'crucial': 'important', 'pivotal': 'key', 'paramount': 'essential',
  'multifaceted': 'complex', 'underscores': 'highlights', 'underscore': 'highlight',
  'seamlessly': 'smoothly', 'seamless': 'smooth',
  'game-changer': 'breakthrough', 'tapestry': 'blend', 'beacon': 'symbol',
  'nestled': 'situated', 'unwavering': 'steady',
  'realm': 'area', 'resonate': 'align', 'harness': 'use',
  'leverage': 'use', 'paradigm shift': 'fundamental change',
  'shed light': 'explain', 'interplay': 'interaction',
  'indispensable': 'vital', 'vibrant': 'lively',
  'synergy': 'collaboration', 'embark': 'begin',
  'meticulous': 'thorough', 'meticulously': 'carefully',
  'notably': 'specifically', 'importantly': 'note that',
  'consequently': 'thus', 'invaluable': 'helpful',
  'transformative': 'major', 'landscape': 'environment',
  'cornerstone': 'foundation', 'linchpin': 'core',
  'synergistic': 'combined', 'underpin': 'support', 'underpins': 'supports',
  'in conclusion': 'to summarize',
  'furthermore': 'also', 'moreover': 'additionally',
  'nevertheless': 'however',
  'it is important to note that': 'note that',
  'it is worth noting that': 'note that',
  'it is crucial to': 'remember to',
  'in summary': 'overall', 'moving forward': 'next',
  'rich tapestry': 'wide range', 'a myriad of': 'many',
  'a wide array of': 'many', 'boasts a': 'has a', 'serves as a': 'is a',
  'takes center stage': 'is central',
  // Expanded
  'in today\'s digital landscape': 'today,',
  'in today\'s modern world': 'today,',
  'in today\'s fast-paced world': 'today,',
  'in today\'s ever-evolving digital landscape': 'today,',
  'in the modern era': 'today,',
  'in today\'s digital age': 'today,',
  'in the contemporary landscape': 'today,',
  'in the current landscape': 'today,',
  'in the ever-evolving landscape': 'today,',
  'in recent years': 'lately,',
  'in recent times': 'recently,',
  'prior to this': 'before',
  'prior to that': 'before',
  'as a result': 'so,',
  'as a consequence': 'so,',
  'has the ability to': 'can',
  'possesses the ability to': 'can',
  'has the capability of': 'can',
  'have the capability of': 'can',
  'has the potential to': 'could',
  'plays a crucial role in': 'helps',
  'plays a pivotal role in': 'helps',
  'serves as a cornerstone of': 'is part of',
  'serves as a linchpin of': 'is part of',
  'brings to bear': 'adds',
  'brings to the table': 'adds',
  'delving into': 'exploring',
  'delving deeper into': 'exploring',
  'in the realm of': 'in the area of',
  'in the domain of': 'in the area of',
  'harnesses the power of': 'uses',
  'leverages the power of': 'uses',
  'utilizes': 'uses',
  'executes the': 'does the',
  'executes this': 'does this',
  'conducts a comprehensive analysis': 'analyzes',
  'conducts a thorough analysis': 'analyzes',
  'iterates through': 'goes through each',
  'computes the results of': 'calculates',
  'ensures that': 'makes sure',
  'facilitates the process of': 'helps',
  'optimizes for': 'improves',
  'reminiscent of': 'like',
  'heralds a new era of': 'starts a new era of',
  'marks a significant shift in': 'changes how',
  'represents a paradigm shift in': 'fundamentally changes',
  'underscores the importance of': 'shows how important',
  'highlights the significance of': 'shows how important',
  'imperative that': 'important that',
  'in essence': 'basically,',
  'as such': 'therefore,',
  'to that end': 'for that purpose,',
  'in the final analysis': 'in the end,',
  'when all is said and done': 'in the end,',
  'needless to say': '',
  'all things being equal': '',
  'as a general rule': '',
  'notably': 'especially',
  'indeed': 'actually',
  'resulting in': 'causing',
  'provides a comprehensive': 'gives a',
  'provides a thorough': 'gives a',
  'provides a detailed': 'gives a',
  'provides a complete': 'gives a',
  'provides a robust': 'gives a',
  'demonstrates the': 'shows the',
  'showcases the': 'shows the',
  'illustrates the': 'shows the',
  'exemplifies the': 'shows the',
  'epitomizes the': 'represents the',
  'sheds light on the': 'explains the',
  'is a testament to': 'proves',
  'is a stark reminder of': 'reminds us of',
  'is a vivid illustration of': 'illustrates',
  'is a prime example of': 'exemplifies',
  'paves the way for': 'enables',
  'ushering in a new era of': 'starting a new era of',
  'safe guard against': 'prevent',
  'preserving the integrity of': 'keeping',
  'ensuring the integrity of': 'keeping',
  'maintaining the integrity of': 'keeping',
  'the bottom line is that': 'in short,',
  'in the event that': 'if',
  'has a tendency to': 'tends to',
  'in a position to': 'able to',
  'make a decision': 'decide',
  'come to a conclusion': 'conclude',
  'provide assistance to': 'help',
  // ── Overconfident hedging & redundant qualifiers ──
  'it is safe to assume that': '',
  'it is worth noting that': 'note that',
  'it is important to know that': 'note that',
  'it is critical to recognize that': 'remember that',
  'it is essential to recognize that': 'remember that',
  'it goes without saying': '',
  'it stands to reason that': '',
  'as mentioned earlier': 'as said before',
  'as mentioned above': 'as said before',
  'as noted above': 'as said before',
  'as noted earlier': 'as said before',
  'as noted previously': 'as said before',
  'as previously stated': 'as said before',
  'as referenced above': 'as said before',
  'as referenced earlier': 'as said before',
  'it is safe to say that': 'note that',
  'it is fair to say that': 'note that',
  'it is clear that': '',
  'it should be noted that': '',
  'it bears mentioning that': '',
  'to be fair': '',
  'as a matter of fact': 'in fact',
  'it is important to understand that': 'remember that',
  'in a broader context': '',
  'in a wider context': '',
  'in the grand scheme of things': '',
  'in today\'s fast-paced digital landscape': 'today,',
  'in today\'s fast-paced business landscape': 'today,',
  'in today\'s fast-paced tech landscape': 'today,',
  'in today\'s fast-paced digital environment': 'today,',
  'in an increasingly digital world': 'currently,',
  'in an increasingly interconnected world': 'currently,',
  'in an increasingly complex world': 'currently,',
  'in an increasingly global landscape': 'currently,',
  'against the backdrop of': 'amid',
  'in the backdrop of': 'amid',
  'in the wake of the': 'after',
  'in the wake of recent': 'after',
  'in the light of the': 'after',
  'in the light of recent': 'after',
  'in today\'s day and age': 'today,',
  'with a view to': 'to',
  'for the purpose of doing': 'to',
  'serves as an indication of': 'shows',
  'serves as an indicator of': 'shows',
  'acts as an indication of': 'shows',
  'acts as an indicator of': 'shows',
  'plays an integral role in': 'helps',
  'plays an essential role in': 'helps',
  'plays a vital role in': 'helps',
  'plays a key role in': 'helps',
  'is under no uncertain terms': '',
  'is nothing short of': 'is',
  'is at the forefront of': 'leads in',
  'is at the cutting edge of': 'leads in',
  'is at the vanguard of': 'leads in',
  'is at the leading edge of': 'leads in',
  'is a pioneer in': 'leads in',
  'is a trailblazer in': 'leads in',
  'is a groundbreaker in': 'leads in',
  'ushering in a new era of': 'starting a new era of',
  'heralding a new era of': 'starting a new era of',
  'signifies a fundamental shift': 'changes how',
  'signifies a major shift': 'changes how',
  'signifies a significant shift': 'changes how',
  'signifies a profound shift': 'changes how',
  'opens up new possibilities for': 'creates new possibilities for',
  'opens new possibilities for': 'creates new possibilities for',
  'opens novel possibilities for': 'creates new possibilities for',
  'opens innovative possibilities for': 'creates new possibilities for',
  'opens exciting possibilities for': 'creates new possibilities for',
  'opens up avenues for': 'creates paths for',
  'opens new horizons for': 'creates new paths for',
  'insomuch as': 'since',
  'notwithstanding': 'but',
};

// ── AI uncertainty / hedge word removal ──
const HEDGE_WORDS = {
  'very ': '', 'somewhat': '', 'rather ': '', 'quite ': '', 'pretty ': '',
  'really ': '', 'extremely': 'very', 'incredibly': 'very', 'absolutely': 'really'
};
  'in order to': 'to',
  'due to the fact that': 'because',
  'at this point in time': 'now',
  'with regard to': 'about',
  'with respect to': 'about',
  'a large number of': 'many',
  'takes into consideration': 'considers',
  'at the end of the day': 'ultimately',
  'for the purpose of': 'for',
  // Expanded
  'in light of the fact that': 'since',
  'a majority of': 'most',
  'has the capability of': 'can',
  'have the capability of': 'can',
  'serves to improve': 'improves',
  'serves to enhance': 'enhances',
  'plays a crucial role in': 'helps',
  'plays a pivotal role in': 'helps',
  'it is worth noting that': 'note that',
  'it is essential to': 'remember to',
  'it is important to note that': 'note that',
  'not to mention': 'and',
  'it is safe to assume that': '',
  'it is worth mentioning that': 'note that',
  'all things considered': 'overall',
  'in the final analysis': 'in the end,',
  'when all is said and done': 'in the end,',
  'at the conclusion': 'finally,',
  'as a general rule': '',
  'the bottom line is that': 'in short,',
};


const TRANSITIONS = {
  'furthermore,': 'also,',
  'moreover,': 'also,',
  'consequently,': 'so,',
  'nevertheless,': 'still,',
  'to summarize,': 'in short,',
  'to sum up,': 'in short,',
  // Expanded
  'nonetheless,': 'still,',
  'in conclusion,': 'overall,',
  'as a matter of fact,': 'in fact,',
  'as a result,': 'so,',
  'as a consequence,': 'so,',
  'to that end,': 'for that purpose,',
  'in light of this,': 'given this,',
  'in view of this,': 'given this,',
  'as a consequence,': 'so,',
  'in light of this,': 'given this,',
  'in view of this,': 'given this,',
  'to that end,': 'for that purpose,',
  'as such,': 'therefore,',
  'it follows that': 'so',
};


const CONTRACTIONS = {
  'cannot': "can't", 'do not': "don't", 'does not': "doesn't",
  'did not': "didn't", 'will not': "won't", 'would not': "wouldn't",
  'should not': "shouldn't", 'could not': "couldn't",
  'is not': "isn't", 'are not': "aren't",
  'was not': "wasn't", 'were not': "weren't",
  'have not': "haven't", 'has not': "hasn't", 'had not': "hadn't",
  'it is': "it's", 'that is': "that's", 'there is': "there's",
  'what is': "what's", 'here is': "here's", 'we are': "we're",
  'you are': "you're", 'they are': "they're",
  'we have': "we've", 'you have': "you've",
  'they have': "they've", 'we will': "we'll",
  'you will': "you'll", 'they will': "they'll",
  // Expanded
  'we would': "we'd", 'you would': "you'd", 'they would': "they'd",
  'who is': "who's", 'when is': "when's", 'where is': "where's",
  'how is': "how's", 'why is': "why's",
};


function stripZeroWidth(text) {
  let result = text;
  for (const c of ZERO_WIDTH_CHARS) {
    result = result.split(c).join('');
  }
  return result;
}

function replaceSmart(text, map) {
  let result = text;
  for (const [pattern, replacement] of Object.entries(map)) {
    const regex = new RegExp(escapeRegex(pattern), 'gi');
    result = result.replace(regex, () => {
      // Preserve case
      if (result[regex.lastIndex ? regex.lastIndex - pattern.length : 0] && result[regex.lastIndex ? regex.lastIndex - pattern.length : 0].match(/[A-Z]/)) {
        return replacement.charAt(0).toUpperCase() + replacement.slice(1);
      }
      return replacement;
    });
  }
  return result;
}

function escapeRegex(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function applyContractions(text) {
  let result = text;
  for (const [pattern, replacement] of Object.entries(CONTRACTIONS)) {
    const regex = new RegExp('\\b' + escapeRegex(pattern) + '\\b', 'gi');
    result = result.replace(regex, replacement);
  }
  return result;
}

function cleanTextOnly(text) {
  let result = stripZeroWidth(text);
  result = result.replace(/["]/g, '"').replace(/[']/g, "'");
  result = result.replace(/ — /g, ' - ').replace(/–/g, '-').replace(/…/g, '...');
  result = result.replace(/[ \t]+/g, ' ');
  return result.trim();
}

function perturbStats(text) {
  let result = text;
  const entries = Object.entries(AI_VOCAB_SWAPS).sort((a,b)=>b[0].length-a[0].length);
  for (const [pattern, replacement] of entries) {
    const regex = new RegExp('\\b' + escapeRegex(pattern) + '\\b', 'gi');
    result = result.replace(regex, replacement);
  }
  return result;
}

function removeFillers(text) {
  let result = text;
  const fillerEntries = Object.entries(FILLER_PHRASES).sort((a,b)=>b[0].length-a[0].length);
  for (const [pattern, replacement] of fillerEntries) {
    const regex = new RegExp('\\b' + escapeRegex(pattern) + '\\b', 'gi');
    result = result.replace(regex, replacement);
  }
  const transitionEntries = Object.entries(TRANSITIONS).sort((a,b)=>b[0].length-a[0].length);
  for (const [pattern, replacement] of transitionEntries) {
    const regex = new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    result = result.replace(regex, replacement);
  }
  // Apply hedge word removal
  const hedgeEntries = Object.entries(HEDGE_WORDS).sort((a,b)=>b[0].length-a[0].length);
  for (const [pattern, replacement] of hedgeEntries) {
    const regex = new RegExp('\\b' + escapeRegex(pattern) + '\\b', 'gi');
    result = result.replace(regex, replacement);
  }
  return result;
}

function applyContractions(text) {
  let result = text;
  const entries = Object.entries(CONTRACTIONS).sort((a,b)=>b[0].length-a[0].length);
  for (const [pattern, replacement] of entries) {
    const regex = new RegExp('\\b' + escapeRegex(pattern) + '\\b', 'gi');
    result = result.replace(regex, replacement);
  }
  return result;
}

function fullSanitize(text) {
  let result = cleanTextOnly(text);
  result = perturbStats(result);
  result = removeFillers(result);
  result = applyContractions(result);
  result = result.replace(/[ \t]+/g, ' ');
  return result.trim();
}

// ---- UI ----
function updateStatus(msg) {
  document.getElementById('status').textContent = msg;
}

function cleanText() {
  const input = document.getElementById('pasteArea').value;
  if (!input.trim()) { updateStatus('⚠️ Please paste text first'); return; }
  const result = cleanTextOnly(input);
  document.getElementById('result').value = result;
  updateStatus('✅ Removed zero-width chars, smart quotes, em-dashes');
}

function humanizeText() {
  const input = document.getElementById('pasteArea').value;
  if (!input.trim()) { updateStatus('⚠️ Please paste text first'); return; }
  const result = fullSanitize(input);
  document.getElementById('result').value = result;
  updateStatus('✨ Full humanization applied');
}

function sanitizeAll() {
  const input = document.getElementById('pasteArea').value;
  if (!input.trim()) { updateStatus('⚠️ Please paste text first'); return; }
  const result = fullSanitize(input);
  document.getElementById('result').value = result;
  updateStatus('🛡️ Full sanitize: watermarks, clichés, fillers, contractions, em-dashes');
}

// Auto-copy result when clicked
document.getElementById('result').addEventListener('click', function() {
  this.select();
  document.execCommand('copy');
});

// Load clipboard content on open
chrome.runtime.sendMessage({action: 'getClipboard'}, (response) => {
  if (response && response.text) {
    document.getElementById('pasteArea').value = response.text;
    updateStatus('📋 Loaded from clipboard');
  }
});
