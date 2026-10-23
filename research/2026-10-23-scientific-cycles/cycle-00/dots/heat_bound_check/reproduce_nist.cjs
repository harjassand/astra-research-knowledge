// Node adapter for the exact functions.exec JavaScript source preserved alongside this file.
// The adapter only supplies the original environment's output/store helpers.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const values = new Map();
const context = {text: value => console.log(JSON.stringify(value)), store: (key,value) => values.set(key,value)};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'nist_shomate.original.js'),'utf8'),context);
