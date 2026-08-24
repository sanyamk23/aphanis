// Test the browser-based cleaning logic
const fs = require('fs');
const path = require('path');

// Inline the cleaner logic
const ZERO_WIDTH_CHARS = ['​','‌','‍','‎','‏','‪','‫','‬','‭','‮','⁠','⁡','⁢','⁣','⁤','⁦','⁧','⁨','⁩','﻿','￼'];
const PUNCT = {'“':'"','”':'"','‘':"'",'’':"'",'—':' - ','–':'-','…':'...'};
const SWAPS = {
  'delve':'explore','delving':'exploring','delves':'explores','testament':'proof','testaments':'proofs',
  'spearhead':'lead','spearheaded':'led','spearheading':'leading','fostering':'building','foster':'encourage',
  'crucial':'important','pivotal':'key','paramount':'essential','multifaceted':'complex','underscores':'highlights',
  'underscore':'highlight','seamlessly':'smoothly','seamless':'smooth','game-changer':'breakthrough',
  'tapestry':'blend','beacon':'symbol','nestled':'situated','unwavering':'steady','realm':'area',
  'resonate':'align','harness':'use','leverage':'use','paradigm shift':'fundamental change','shed light':'explain',
  'interplay':'interaction','indispensable':'vital','vibrant':'lively','synergy':'collaboration','embark':'begin',
  'meticulous':'thorough','meticulously':'carefully','notably':'specifically','importantly':'note that',
  'consequently':'thus','invaluable':'helpful','transformative':'major','landscape':'environment',
  'cornerstone':'foundation','linchpin':'core','synergistic':'combined','underpin':'support','underpins':'supports',
  'in conclusion':'to summarize','furthermore':'also','moreover':'additionally','nevertheless':'however',
  'it is important to note that':'note that','it is worth noting that':'note that','it is crucial to':'remember to',
  'in summary':'overall','moving forward':'next','rich tapestry':'wide range','a myriad of':'many',
  'a wide array of':'many','boasts a':'has a','serves as a':'is a','takes center stage':'is central'
};
const FILLERS = {
  'in order to':'to','due to the fact that':'because','at this point in time':'now',
  'with regard to':'about','with respect to':'about','a large number of':'many',
  'takes into consideration':'considers','at the end of the day':'ultimately',
  'for the purpose of':'for'
};
const TRANSITIONS = {
  'furthermore,':'also,','moreover,':'also,','consequently,':'so,',
  'nevertheless,':'still,','to summarize,':'in short,','to sum up,':'in short,'
};
const CONTRACTIONS = {
  'cannot':"can't",'do not':"don't",'does not':"doesn't",'did not':"didn't",'will not':"won't",
  'would not':"wouldn't",'should not':"shouldn't",'could not':"couldn't",'is not':"isn't",
  'are not':"aren't",'was not':"wasn't",'were not':"weren't",'have not':"haven't",'has not':"hasn't",
  'had not':"hadn't",'it is':"it's",'that is':"that's",'there is':"there's",'what is':"what's",
  'here is':"here's",'we are':"we're",'you are':"you're",'they are':"they're",
  'we have':"we've",'you have':"you've",'they have':"they've",
  'we will':"we'll",'you will':"you'll",'they will':"they'll"
};

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function cleanText(input) {
  let r = input;
  for (const c of ZERO_WIDTH_CHARS) r = r.split(c).join('');
  for (const [k, v] of Object.entries(PUNCT)) r = r.split(k).join(v);
  r = r.replace(/[ \t]+/g, ' ').trim();
  return r;
}

function fullClean(input) {
  let r = cleanText(input);
  for (const [k, v] of Object.entries(SWAPS)) {
    r = r.replace(new RegExp('\\b' + escapeRegex(k) + '\\b', 'gi'), v);
  }
  for (const [k, v] of Object.entries(FILLERS)) {
    r = r.replace(new RegExp('\\b' + escapeRegex(k) + '\\b', 'gi'), v);
  }
  for (const [k, v] of Object.entries(TRANSITIONS)) {
    r = r.replace(new RegExp(escapeRegex(k), 'gi'), v);
  }
  for (const [k, v] of Object.entries(CONTRACTIONS)) {
    r = r.replace(new RegExp('\\b' + escapeRegex(k) + '\\b', 'gi'), v);
  }
  r = r.replace(/[ \t]+/g, ' ').trim();
  return r;
}

// Test with AI-heavy text
const testInput = 'In conclusion, this paradigm shift—delving into the realm of testaments—underscores the crucial importance of leveraging multifaceted solutions. Furthermore, it is important to note that we cannot fail to realize that due to the fact that we are embarking on this journey, we must not be swayed by the vibrant tapestry of possibilities that the game-changer presents.';
console.log('=== INPUT ===');
console.log(testInput);
console.log('\n=== OUTPUT ===');
const output = fullClean(testInput);
console.log(output);

// Checks
const hasEmDash = output.includes('—');
const hasFurthemore = /\bfurhtermore\b/i.test(output);
const hasParadigm = /\bparadigm\b/i.test(output);
const hasTestament = /\btestament\b/i.test(output);
const hasCrucial = /\bcrucial\b/i.test(output);

console.log('\n=== AI MARKER CHECK ===');
console.log('Em-dash present:', hasEmDash, hasEmDash ? '❌ FAIL' : '✅ PASS');
console.log('furthermore present:', hasFurthemore, hasFurthemore ? '❌ FAIL' : '✅ PASS');
console.log('paradigm present:', hasParadigm, hasParadigm ? '❌ FAIL' : '✅ PASS');
console.log('testament present:', hasTestament, hasTestament ? '❌ FAIL' : '✅ PASS');
console.log('crucial present:', hasCrucial, hasCrucial ? '❌ FAIL' : '✅ PASS');
