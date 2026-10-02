const assert = require('assert');
assert.ok([16, 18, 20, 22, 24].includes(Number(process.versions.node.split('.')[0])));
console.log('Node fixture passed:', process.version);
